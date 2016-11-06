# gocd-pipeline-configurator
I've ported this to golang for easy install:
https://github.com/dennisgranath/gocd-plumber

Create GoCD pipelines from yaml code.

Since GoCD 1.5.3 it's possible to create pipelines using the pipeline config api. This is an initial effort to have something similiar to jenkins job builder for gocd. Please don't use it anywhere near a production server.

To try it out:

1. Clone this repo
2. Edit .config.ini file
3. pip install requests
4. run gocd-pipeline-configurator.sh

There's an example pipelines.yml in the examples/example1 dir. The example assumes that template 'build' already exists in GoCD. You can also checkout my other example using 'yaml templates' in the examples/template_example dir. In this example the resulting pipeline will be the merged result of the pipeline hash and the template hash.

## Development

### Docker
Using https://hub.docker.com/r/gocd/gocd-dev/ you can bring up a GoCD Server and Agent, in a docker container. Note that the docs refer to the deprecated boot2docker, not docker machine, but procedure is almost identical.

#### Start container (first time will download it)
* Random ports and name: ```docker run -tiP gocd/gocd-dev```
* Known port & name, without wait, daemonized: ```docker run -d -p 8153:8153 -e MSG_TIME=0 --name gocd gocd/gocd-dev```

#### Browse GoCD GUI
* Find out the ip: ```docker-machine ip default```
* Find out the port (server, ie GUI, is normally on 8153): ```docker port gocd```

#### Getting into the container
```docker exec -it gocd bash```
