# docker build -t edgar2data .
# docker run -it --entrypoint /bin/bash -p 80:80 edgar2data
docker run -d --name edgar2data -p 80:80 edgar2data
