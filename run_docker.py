#!/usr/bin/python3

import os
import sys

if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == 'build':
            os.system("docker build -t edgar2data .")
        elif sys.argv[1] == "push":
            os.system("docker push schorndorfer/edgar2data:0.1.0")
        elif sys.argv[1] == "shell":
            os.system("docker run -it --entrypoint /bin/bash -p 80:80 edgar2data")
        elif sys.argv[1] == "start":
            os.system("docker run -d --name edgar2data -p 80:80 edgar2data")

