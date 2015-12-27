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


def createPipeline(file_name):
    create_url = options[BASE_URL_OPTION_NAME] + "/go/api/admin/pipelines"
    file_path = options[PIPELINE_DIR_OPTION_NAME] + "/" + file_name
    yaml_data = yaml.load(open(file_path))
    json_data = json.dumps(yaml_data)
    headers = {'Accept': 'application/vnd.go.cd.v1+json', 'Content-Type': 'application/json'}
    response = requests.post(create_url, data=json_data, auth=(options['api_username'], options['api_password']), headers=headers)
    print response


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
        createPipeline(file_name)

if __name__ == "__main__":
   main(sys.argv[1:])
