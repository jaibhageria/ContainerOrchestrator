README FILE for CC Project

Project done by -
1) Jai Agarwal (01FB16ECS144)
2) Guruprasad M (01FB16ECS126)
3) Lokesh Kumar (01FB16ECS180)
4) Krishna Sidharth S (01FB16ECS180)

The Project contains an Acts folder which has the following files:
1)actsapp folder (contains the DockerFile to launch acts container and required api file and intial images which will be uploaded to the mongo database)
2)orchestrator folder contains :
  a) acts_specific_orchestrator.py (contains request forwarding only for acts container specific requests)
  b)generalised_orchestrator.py and settings.json (this file can be used to orchestrate any application, user can change required settings in settings.json file for the orchestrator file to use.)


How to run :
1) with terminal open in Acts folder, run command : docker-compose up -d
2) with terminal open in orchestrator folder, change required settings in settings.json file, or leave to default to run with acts containers
3) run the command: python3 generalised_orchestrator.py

To Stop:
1) Ctrl+C to exit and stop orchestrator.
2) docker container stop $(docker ps -q) : stops all running containers 


THANK YOU 