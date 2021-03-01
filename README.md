
# Spark + Jupyter notebooks

## Documentation

Jupyter deployment is based on official images, as described in the following webpages:

- https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-all-spark-notebook
- https://github.com/jupyter/docker-stacks/tree/master/all-spark-notebook

Client mode execution is described here:

- https://spark.apache.org/docs/latest/running-on-kubernetes.html#client-mode


## Deployment

### Image build

Executors image is built from official Dockerfiles

```
curl -sL https://apache.brunneis.com/spark/spark-3.0.2/spark-3.0.2-bin-hadoop2.7.tgz -O-
tar -xf spark-3.0.2-bin-hadoop2.7.tgz
cd spark-3.0.2-bin-hadoop2.7

bin/docker-image-tool.sh -r luismiguelsaez/spark -t 3.0.2-python -p kubernetes/dockerfiles/spark/bindings/python/Dockerfile build
bin/docker-image-tool.sh -r luismiguelsaez/spark -t 3.0.2-python -p kubernetes/dockerfiles/spark/bindings/python/Dockerfile push
```

### Kubernetes

```
kubectl apply -f k8s/jupyter/rbac.yml
kubectl apply -f k8s/jupyter/deployment.yml
```

### Connect to Jupyter console ( without ingress )

- Create tunnel against service

    ```
    kubectl port-forward service/jupyter-all-spark 8888
    ```

- Connect to Jupyter console, using the token defined in secrets

    http://localhost:8888/tree?token=9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08

- From here, we can create a Python notebook from ```notebooks/simple-notebook.py```
