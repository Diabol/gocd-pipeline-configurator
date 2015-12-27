#!/usr/bin/env python
import json, yaml, ConfigParser, os, json, requests, sys, getopt

CONFIG_SECTION = "default"
BASE_URL_OPTION_NAME  = "gocd_base_url"
PIPELINE_DIR_OPTION_NAME = "pipeline_dir"
options = {}

def parseConfigFile(path):
    config = ConfigParser.ConfigParser()

    config.read(path)
    for section in config.sections():
        if section == CONFIG_SECTION:
            for option in config.options(section):
                options[option] = config.get(section, option)

def getEtag(pipeline_name):
    get_url = options[BASE_URL_OPTION_NAME] + "/go/api/admin/pipelines/" + pipeline_name
    headers = {'Accept': 'application/vnd.go.cd.v1+json'}
    response = requests.get(get_url, auth=(options['api_username'], options['api_password']), headers=headers)
    if response.status_code == 200:
        return response.headers['etag']
    return None

def createOrEditPipeline(file_name):
    file_path = options[PIPELINE_DIR_OPTION_NAME] + "/" + file_name
    yaml_data = yaml.load(open(file_path))
    pipeline_name = yaml_data['pipeline']['name']
    etag = getEtag(pipeline_name)
    if  etag == None:
        createPipeline(file_path)
    else:
        editPipeline(file_path, pipeline_name, etag)

def editPipeline(file_path, pipeline_name, etag):
    yaml_data = yaml.load(open(file_path))
    json_data = json.dumps(yaml_data)
    edit_url = options[BASE_URL_OPTION_NAME] + "/go/api/admin/pipelines/" + pipeline_name
    headers = {'Accept': 'application/vnd.go.cd.v1+json', 'Content-Type': 'application/json', "If-Match": etag}
    response = requests.put(edit_url, data=json_data, auth=(options['api_username'], options['api_password']), headers=headers)


def createPipeline(file_path):
    yaml_data = yaml.load(open(file_path))
    json_data = json.dumps(yaml_data)
    headers = {'Accept': 'application/vnd.go.cd.v1+json', 'Content-Type': 'application/json'}
    response = requests.post(create_url, data=json_data, auth=(options['api_username'], options['api_password']), headers=headers)


def getDefaultConfig():
    working_dir_conf = os.getcwd() + "/.config.ini"
    if os.path.isfile(working_dir_conf):
        return working_dir_conf
    return None

#Main
def main(argv):
    configfile = getDefaultConfig()
    try:
      opts, args = getopt.getopt(argv,"hc:",["config="])
    except getopt.GetoptError:
      print 'gocd-pipeline-configurator.py -c <configfile>'
      sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print 'gocd-pipeline-configurator.py -c <configfile>'
            sys.exit()
        elif opt in ("-c", "--config"):
            configfile = arg

    if not os.path.isfile(configfile):
        print "This configfile does not exist: " + configfile
        sys.exit(1)

    parseConfigFile(configfile)
    for file_name in os.listdir(options['pipeline_dir']):
        createOrEditPipeline(file_name)

if __name__ == "__main__":
   main(sys.argv[1:])
