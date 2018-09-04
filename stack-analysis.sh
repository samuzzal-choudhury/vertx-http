
 
 echo "Generating effective POM.."
 mvn help:effective-pom -f  "/projects/vertx-http/epom.xml" -Doutput="/projectsvertx-http/pom.xml" &> /projects/vertx-http/outfile
 echo "Analyzing your application stack.."
 
 
curl -X POST    -F 'manifest=@/projects/vertx-http/pom.xml' 23.251.159.157:7000/stack-analysis 2> /projects/vertx-http/errorlog
