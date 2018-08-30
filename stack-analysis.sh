
 
 echo "Generating effective POM.."
 cp /projects/web-java-spring-project/pom.xml /projects/web-java-spring-project/epom.xml
 mvn help:effective-pom -f  "/projects/web-java-spring-project/epom.xml" -Doutput="/projects/web-java-spring-project/pom.xml" &> /projects/vertx-http/outfile
 echo "Analyzing your application stack.."
 
curl -X POST    -F 'manifest=@/projects/web-java-spring-project/pom.xml' 192.168.225.126:7000/stack-analysis 2> /projects/vertx-http/errorlog
