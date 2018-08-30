
 
 echo "Generating effective POM.."
 cp /projects/vertx-http/pom.xml /projects/vertx-http/epom.xml
 mvn help:effective-pom -f  "/projects/vertx-http/epom.xml" -Doutput="/projectsvertx-http/pom.xml" &> /projects/vertx-http/outfile
 echo "Analyzing your application stack.."
 
curl -X POST    -F 'manifest=@/projects/vertx-http/pom.xml' 192.168.225.126:7000/stack-analysis 2> /projects/vertx-http/errorlog
