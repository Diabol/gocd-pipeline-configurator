#!/usr/bin/env python
import json, yaml, ConfigParser, os, json, requests, sys, getopt


CONFIG_SECTION = "default"
BASE_URL_OPTION_NAME  = "gocd_base_url"
PIPELINE_DIR_OPTION_NAME = "pipeline_dir"
options = {}
templates = {}


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

def createOrEditPipeline(pipeline):
    pipeline_name = pipeline['pipeline']['name']
    etag = getEtag(pipeline_name)
    if  etag == None:
        createPipeline(pipeline)
    else:
        editPipeline(pipeline, etag)

def editPipeline(pipeline, etag):
    edit_url = options[BASE_URL_OPTION_NAME] + "/go/api/admin/pipelines/" + pipeline['pipeline']['name']
    if 'pipeline_template' in pipeline:
        if not pipeline['pipeline_template'] in templates:
            print "Error: No such template '" + pipeline['pipeline_template']+ "'. Skipping " + pipeline['pipeline']['name']
            return
        template = templates[pipeline['pipeline_template']]
        pipeline = merge(pipeline, template)
    json_data = json.dumps(pipeline)
    headers = {'Accept': 'application/vnd.go.cd.v1+json', 'Content-Type': 'application/json', "If-Match": etag}
    response = requests.put(edit_url, data=json_data, auth=(options['api_username'], options['api_password']), headers=headers)
    if not response.status_code == 200:
       print "Error: Could not edit pipeline " + pipeline['pipeline']['name'] + ": " + response.text

def createPipeline(pipeline):
    create_url = options[BASE_URL_OPTION_NAME] + "/go/api/admin/pipelines"
    if 'pipeline_template' in pipeline:
        if not pipeline['pipeline_template'] in templates:
            print "Error: No such template '" + pipeline['pipeline_template']+ "'. Skipping " + pipeline['pipeline']['name']
            return
        template = templates[pipeline['pipeline_template']]
        pipeline = merge(pipeline, template)

    json_data = json.dumps(pipeline)
    headers = {'Accept': 'application/vnd.go.cd.v1+json', 'Content-Type': 'application/json'}
    response = requests.post(create_url, data=json_data, auth=(options['api_username'], options['api_password']), headers=headers)
    if not response.status_code == 200:
       print "Error: Could not create pipeline " + pipeline['pipeline']['name'] + ": " + response.text

def createPipelines(filename):
    file_path = options[PIPELINE_DIR_OPTION_NAME] + "/" + filename
    yaml_data = yaml.load(open(file_path))

    if 'templates' in yaml_data:
        templates.update(yaml_data['templates'])
        print templates

    if 'pipelines' in yaml_data:
        pipelines = yaml_data['pipelines']
        for pipeline in pipelines:
            createOrEditPipeline(pipeline)

def getDefaultConfig():
    working_dir_conf = os.getcwd() + "/.config.ini"
    if os.path.isfile(working_dir_conf):
        return working_dir_conf
    return None

def merge(pipeline, template):
    if isinstance(pipeline,dict) and isinstance(template,dict):
        for k,v in template.iteritems():
            if k not in pipeline:
                pipeline[k] = v
            else:
                pipeline[k] = merge(pipeline[k],v)
    return pipeline

#Main
def main(argv):
    configfile = getDefaultConfig()
    try:
      opts, args = getopt.getopt(argv,"hc:d",["config=", "dry-run"])
    except getopt.GetoptError:
      print 'gocd-pipeline-configurator.py -c <configfile>'
      sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print 'gocd-pipeline-configurator.py -c <configfile>'
            sys.exit()
        elif opt in ("-c", "--config"):
            configfile = arg
        elif opt in ("-d", "--dry-run"):
            print "dry-run"

    if not os.path.isfile(configfile):
        print "This configfile does not exist: " + configfile
        sys.exit(1)

    parseConfigFile(configfile)
    for file_name in os.listdir(options['pipeline_dir']):
        createPipelines(file_name)

if __name__ == "__main__":
   main(sys.argv[1:])
