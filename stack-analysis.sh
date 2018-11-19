
#!/bin/bash
set -x

usage() {
    echo "Usage:"
    echo "$0 [-f <manifest filename with path>][-p <project directory>]"
    echo "Set environment variables THREESCALE_USER_KEY and THREESCALE_API_URL"
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

if [ -z "${f}" ] || [ -z "${p}" ]; then
    usage
    exit -1
fi

echo "Analyzing your application stack ..."

manifest=$(basename $f)
if [ "$manifest" == "pom.xml" ]
then
    mkdir -p ./target
    rm -rf ./target/*
    echo "Generating effective POM.."
    mvn help:effective-pom -f "$f" -Doutput="target/pom.xml"
    manifest='./target/pom.xml'
else
    manifest=$f
fi

manifest='@'$manifest
api_url=$THREESCALE_API_URL
output=`curl -s -X POST -F "manifest[]=$manifest" -F"filePath[]=$p"  $api_url?user_key=$THREESCALE_USER_KEY`
id=`echo $output|python -c "import sys, json; print(json.load(sys.stdin)['id'])"`

sleep 5

get_cmd="$api_url/$id?user_key=$THREESCALE_USER_KEY"
curl -s $get_cmd | sed 's/"//g' | sed 's/\\t/    /g' | sed 's/\\n/ \
/g'
