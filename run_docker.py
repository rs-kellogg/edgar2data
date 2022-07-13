#!/usr/bin/python3

import os
import sys
from rich import print

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == 'build':
            print("building docker image...")
            os.system("docker build -t edgar2data .")
        elif sys.argv[1] == "push":
            print("pushing docker image to dockerhub...")
            os.system("docker push schorndorfer/edgar2data:0.1.0")
        elif sys.argv[1] == "shell":
            print("starting shell")
            os.system("docker run -it --entrypoint /bin/bash -p 80:80 edgar2data")
        elif sys.argv[1] == "start":
            print("starting web service")
            os.system("docker run -d --name edgar2data -p 80:80 edgar2data")

