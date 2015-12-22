# gocd-pipeline-configurator
Create gocd pipelines from yaml code. 

Since gocd 1.5.3 it's possible to create pipelines using the pipeline config api. This is an initial effort to have something similiar to jenkins job builder for gocd. Please don't use it anywhere near a production server.

To try it out:

1. Clone this repo
2. Edit .config.ini file
3. run gocd-pipeline-configurator.sh

There's an example pipeline.yaml in the examples dir. The example assumes that template 'build' already exists in gocd.
