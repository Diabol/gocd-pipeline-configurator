#!/usr/bin/python
# import the standard JSON parser
import json, yaml, ConfigParser, os, json, requests
# import the REST library
from restful_lib import Connection

CONFIG_SECTION = "default"
BASE_URL_OPTION_NAME  = "gocd_base_url"
PIPELINE_DIR_OPTION_NAME = "pipeline_dir"

options = {}

def parseConfigFile():
    config = ConfigParser.ConfigParser()
    config.read('./.config.ini')
    for section in config.sections():
        if section == CONFIG_SECTION:
            for option in config.options(section):
                options[option] = config.get(section, option)


def createPipeline(file_name):
    create_url = options[BASE_URL_OPTION_NAME] + "/go/api/admin/pipelines"
    file_path = options[PIPELINE_DIR_OPTION_NAME] + "/" + file_name
    yaml_data = yaml.load(open(file_path))
    json_data = json.dumps(yaml_data)
    headers = {'Accept': 'application/vnd.go.cd.v1+json', 'Content-Type': 'application/json'}
    print requests.post(create_url, data=json_data, auth=(options['api_username'], options['api_password']), headers=headers)


#Main
parseConfigFile()
for file_name in os.listdir(options['pipeline_dir']):
    createPipeline(file_name)
