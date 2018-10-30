
#!/bin/bash

usage() {
    echo "Usage:"
    echo "$0 [-f <manifest filename with path>][-p <project directory>]"
    exit -1
}

while getopts ":f:p:" o; do
    case "${o}" in
        f)
            f=${OPTARG}
            ;;
        p)
            p=${OPTARG}
            ;;
        *)
            usage
            ;;
    esac
done

#if [ -z "${f}" ] || [ -z "${p}" ]; then
#    usage
#fi

f='/projects/vertx-http/pom.xml'
p='/home/sam'

echo "Analyzing your application stack ..."

manifest=$(basename $f)
if [ "$manifest" == "pom.xml" ]
then
    echo "Generating effective POM.."
    # mvn help:effective-pom -f  "/tmp/epom.xml" -Doutput="$f" &> /projects/vertx-http/outfile
    mkdir -p /tmp/target
    # cp -f /tmp/epom.xml /tmp/target/pom.xml
    manifest='./target/pom.xml'
else
    manifest=$f
fi

set -x

# Environment Variables to be used for user_key and api_url
user_key='250f7573417ff52aee50728f698ecd96'
api_url='https://friendly_system_service-2445582075730.production.gw.apicast.io:443/api/v1/stack-analyses/'

manifest='@'$manifest
output=`curl -s -X POST -F "manifest[]=$manifest" -F"filePath[]=$p"  $api_url?user_key=$THREESCALE_USER_KEY`
id=`echo $output|python -c "import sys, json; print(json.load(sys.stdin)['id'])"`

sleep 5

get_cmd="$api_url/$id?user_key=$THREESCALE_USER_KEY"
curl -s $get_cmd | sed 's/"//g' | sed 's/\\t/    /g' | sed 's/\\n/ \
/g'
