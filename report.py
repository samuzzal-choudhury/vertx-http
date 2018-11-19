import os
import codecs
import time
import datetime as dt
import json
from collections import namedtuple

# Response of stack-analyses presented in a report
with open('response.json') as f:
    json_stack_report = json.loads(f.read())

def generate_report(json_stack_report):
    response_to_client = "\nSummary of Application stack report generated at : "
    response_to_client += json_stack_report["finished_at"]

    response_to_client += "\n"
    response_to_client += "--------------------------------------------------------------------------------" 
    response_to_client += "\n\t"

    for result in json_stack_report['result']:
        response_to_client += "\nReport for {path}/{name}".format(path=result["manifest_file_path"], name=result["manifest_name"])

        response_to_client += "\n\n\t1) # of application dependencies : "
        response_to_client += str(result['user_stack_info'] ['analyzed_dependencies_count'])

        response_to_client += "\n"
        response_to_client += "\n\t"
        response_to_client += "2) Dependencies with Licenses : \n\t"
        deps = result['user_stack_info']['analyzed_dependencies']
        deps_with_licenses = 0
        for dep in deps:
            dependency_cve_display = ""
            for s in dep['security']:
                dependency_cve_display += "\nHas a CVE : "+ s['CVE'] + " with CVSS score : " + s['CVSS']

            dependency_version = dep['version']

            response_to_client += "\t -- " + "'" + dep['name'] + "' - " + dep['version']
            response_to_client += dependency_cve_display

            response_to_client += "\n Has  licenses : " + ','.join(dep['licenses'])
            response_to_client += "\n\t"

        response_to_client += "\n\t"

        license_conflict = result['user_stack_info']['stack_license_conflict']
        if license_conflict == 'false':
            response_to_client += "NO application stack level license conflcits been found"

        response_to_client += "3) Suggest adding these dependencies to your application stack: \n\t"

        companion_components = result['recommendation']['companion']
        for companion in companion_components:
            dependency_name = companion['name']
            version = companion['version']

            confidence = companion.get('cooccurrence_probability', 'NA')
            display_reason = companion.get('reason', 'NA')
            companion_dependency_license = ','.join(companion['licenses'])
            response_to_client += "\t--" + "'" + dependency_name + "'" + " with version: " + "'" + version + "'" + " has a license: " + "'" + companion_dependency_license + "'"  
            response_to_client += "'" + dependency_name + "'" + "\n\t"
            response_to_client += "\t\tReason: " + display_reason + "\n\t"
            response_to_client += "\t\tConfidence levels: " + str(confidence) + "%\n\t"
        response_to_client += "\n4) NO usage outlier application depedencies been found\n\t"
        response_to_client += "\n5) NO alternative  application depedencies been suggested\n\t"
        print (response_to_client)

generate_report(json_stack_report)
