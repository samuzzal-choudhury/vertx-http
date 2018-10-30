from flask import Flask, json, Response, request, make_response
import  requests
from http_status import Status
import os
import codecs
import time
import datetime as dt
import json
from collections import namedtuple

app = Flask(__name__)


@app.route('/stack-analysis', methods=['GET', 'POST'])
def hello():
    request.files['manifest'].save('/tmp/pom.xml')
    analyticsurl = "https://recommender.api.openshift.io/api/v1/stack-analyses"
    data = {'app' : 'aaaaa'}
    uploadfile = "/tmp/file"
    files = {'manifest[]' : open('/tmp/pom.xml', 'rb')}
    payload = {'filePath[]' : 'home/JohnDoe'}
    res = requests.post(analyticsurl, files=files, headers=header,  params=payload)
    json_response_for_trigger = json.loads(res.text)
    stack_analysis_id = json_response_for_trigger['id']

    time.sleep (20.0)

    retrieve_stack_report_url = "https://recommender.api.openshift.io/api/v1/stack-analyses/"
    retrieve_stack_report_url += stack_analysis_id
    stack_report_response = requests.get(retrieve_stack_report_url,  headers=header)
    json_stack_report = json.loads(stack_report_response.text)
    print (json.dumps(json_stack_report))
    
    response_to_client = "\nSummary of Application stack report generated at : "
    response_to_client += json_stack_report["finished_at"]

    response_to_client += "\n"
    response_to_client += "--------------------------------------------------------------------------------" 
    response_to_client += "\n\t"
   
    response_to_client += "1) # of application dependencies : "
    dependency_count = str(json_stack_report['result'] [0] ['user_stack_info'] ['analyzed_dependencies_count'])
    response_to_client += dependency_count
   
    response_to_client += "\n"
    response_to_client += "\n\t"
    response_to_client += "2) Dependencies with Licenses : \n\t"
    count = int(json_stack_report['result'] [0] ['user_stack_info'] ['analyzed_dependencies_count'])
    for index in range(count):
        dependency_cve_display = ""
        dependency_cve = ""
        dependency_cvss = ""
        dependency_name = str(json_stack_report['result'] [0] ['user_stack_info'] ['analyzed_dependencies'] [index] ['name'])
        if dependency_name.startswith("ch.qos.logback:logback"):
            dependency_cve= str(json_stack_report['result'] [0] ['user_stack_info'] ['analyzed_dependencies'] [index] ['security'] [0] ['CVE'])
            dependency_cvss= str(json_stack_report['result'] [0] ['user_stack_info'] ['analyzed_dependencies'] [index] ['security'] [0] ['CVSS'])
            dependency_cve_display = "Has a CVE : "+dependency_cve + " with CVSS score : "+dependency_cvss

        dependency_version = str(json_stack_report['result'] [0] ['user_stack_info'] ['analyzed_dependencies'] [index] ['version'])
        dependency_license_1 = str(json_stack_report['result'] [0] ['user_stack_info'] ['analyzed_dependencies'] [index] ['licenses'] [0])
        dependency_license_2 = str(json_stack_report['result'] [0] ['user_stack_info'] ['analyzed_dependencies'] [index] ['licenses'] [1])

        response_to_client += "\t -- " + "'" + dependency_name + "'"   
        if len(dependency_cve_display) > 0:
            response_to_client += "'" + dependency_cve_display + "'"   

        response_to_client += " with version: " + "'" + dependency_version + "'" + " has  licenses : " + "'" + dependency_license_1 + "'" + " , " + "'" + dependency_license_2 + "'"   
        response_to_client += "\n\t"
    
    response_to_client += "\n\t"

   
    license_conflict = str(json_stack_report['result'] [0] ['user_stack_info']  ['stack_license_conflict'])
    if license_conflict == 'false':
        response_to_client += "NO application stack level license conflcits been found"
    
    recommondation_count = 3
    response_to_client += "3) Suggest adding these dependencies to your application stack: \n\t"
    
    for rindex in range(recommondation_count):
        dependency_name = str(json_stack_report['result'] [0] ['recommendation']  ['companion'] [rindex] ['name'])
        version = str(json_stack_report['result'] [0] ['recommendation']  ['companion'] [rindex] ['version'])

        confidence = str(json_stack_report['result'] [0] ['recommendation']  ['companion'] [rindex] ['cooccurrence_probability']) 
        reason = str(json_stack_report['result'] [0] ['recommendation']  ['companion'] [rindex] ['reason']) 
        display_reason = reason.split('Do')[0]
        companion_dependency_license = str(json_stack_report['result'] [0] ['recommendation']  ['companion'] [rindex] ['licenses'] [0]) 
        response_to_client += "\t--" + "'" + dependency_name + "'" + " with version: " + "'" + version + "'" + " has a license: " + "'" + companion_dependency_license + "'"  
        response_to_client += "'" + dependency_name + "'" + "\n\t"
        response_to_client += "\t\tReason: " + display_reason + "\n\t"
        response_to_client += "\t\tConfidence levels: " + confidence + "%\n\t"
    response_to_client += "\n4) NO usage outlier application depedencies been found\n\t"
    response_to_client += "\n5) NO alternative  application depedencies been suggested\n\t"
    print (response_to_client)
    
    url = 'https://stack-analytics-report.openshift.io/#/analyze/00520cb3bbf34717824e7fa123940f62?api_data={ "access_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjBsTDB2WHM5WVJWcVpNb3d5dzh1TkxSX3lyMGlGYW96ZFFrOXJ6cTJPVlUiLCJ0eXAiOiJKV1QifQ.eyJhY3IiOiIwIiwiYWxsb3dlZC1vcmlnaW5zIjpbImh0dHBzOi8vYXV0aC5vcGVuc2hpZnQuaW8iLCJodHRwczovL29wZW5zaGlmdC5pbyJdLCJhcHByb3ZlZCI6dHJ1ZSwiYXVkIjoiZmFicmljOC1vbmxpbmUtcGxhdGZvcm0iLCJhdXRoX3RpbWUiOjE1MzUwMDQxNzcsImF6cCI6ImZhYnJpYzgtb25saW5lLXBsYXRmb3JtIiwiZW1haWwiOiJqYWt1bWFyQHJlZGhhdC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZXhwIjoxNTM3NTk2MTc3LCJmYW1pbHlfbmFtZSI6Ikt1bWFyIiwiZ2l2ZW5fbmFtZSI6ImphaXZhcmRoYW4iLCJpYXQiOjE1MzUwMDQxNzcsImlzcyI6Imh0dHBzOi8vc3NvLm9wZW5zaGlmdC5pby9hdXRoL3JlYWxtcy9mYWJyaWM4IiwianRpIjoiYTI5MDNjNjUtZDE1MS00YTMxLTkxMGMtMmRjY2ExODFkMGE4IiwibmFtZSI6ImphaXZhcmRoYW4gS3VtYXIiLCJuYmYiOjAsInByZWZlcnJlZF91c2VybmFtZSI6Impha3VtYXIiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX0sImJyb2tlciI6eyJyb2xlcyI6WyJyZWFkLXRva2VuIl19fSwic2Vzc2lvbl9zdGF0ZSI6ImNiMTk5NmZjLWY0ZmItNDJlMS04MTI4LTg2NjdlN2E5NDU5NSIsInN1YiI6ImMwNGRiYzQ2LWVjZmQtNDc4ZC1iM2E1LWQ5ODkzZDEyNjM4OCIsInR5cCI6IkJlYXJlciJ9.V9jxAztuTlfPTqbHFmRi307plL_0uPU42iUpPcTt-ahk5d50vVAT2rAb4Y5HicO69mpnySEtNOqDzBnLqEfzqtKvLgOC47ARqyj68HJVYyV-PDjucrR7fgdswY4QXCYy-NyBbjdJFSoi6DcuNwhE8jNpCHy_kEOyu93C5uIzAVnzxbZuxqJ_xKMzFhrZD99Gr1rMPQJSBum1XuW-mUYA3cbqkOAZsimAwl_UidVPHzkhLcAgH26jT2TDqAMFgpb9fGFWkX9ScuWDO_3c_M1v5j9Dtvia05Qaiwuyigk4Xxxeg-JMCdlfle6j8u96FmXeiwPbrKbxzLql25cqPcz9ng", "route_config": "api_url": "https://recommender.api.openshift.io/" } }'
    display_url = '<a href= '+ url + '> click here <\a>'
    return display_url
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000)
