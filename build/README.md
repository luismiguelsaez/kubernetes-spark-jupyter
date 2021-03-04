
## Package download
```
curl -sL https://ftp.cixug.es/apache/spark/spark-3.0.2/spark-3.0.2-bin-hadoop2.7.tgz | gunzip | tar -xf -
```

## Current Jupyter image python version
```
docker run --rm -it jupyter/all-spark-notebook:29edefbcb06a python -V | sed 's/Python //g'
3.8.8
```

## Build executor image with custom python bindings
```
spark-3.0.2-bin-hadoop2.7/bin/docker-image-tool.sh -t 3.0.2-py3.8.8 -p bindings/python/Dockerfile -b java_image_tag=11-jre-slim -b python_version=3.8.8 build
```

## Add image to kind cluster
```
kind load docker-image spark-py:3.0.2-py3.8.8 --name=jupyter-test
```
