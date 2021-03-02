
# Spark + Jupyter notebooks

## Documentation

Jupyter deployment is based on official images, as described in the following webpages:

- https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-all-spark-notebook
- https://github.com/jupyter/docker-stacks/tree/master/all-spark-notebook

Client mode execution is described here:

- https://spark.apache.org/docs/latest/running-on-kubernetes.html#client-mode

Available configuration parameters:

- https://spark.apache.org/docs/latest/configuration.html

## Deployment

### Create cluster ( https://kind.sigs.k8s.io/docs/user/ingress/#create-cluster )

```
cat <<EOF | kind create cluster --name=jupyter-test --config=-
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "ingress-ready=true"
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
    protocol: TCP
  - containerPort: 443
    hostPort: 443
    protocol: TCP
EOF
```

### Image build

Executors image is built from official Dockerfiles

```
curl -sL https://apache.brunneis.com/spark/spark-3.0.2/spark-3.0.2-bin-hadoop2.7.tgz -O-
tar -xf spark-3.0.2-bin-hadoop2.7.tgz

spark-3.0.2-bin-hadoop2.7/bin/docker-image-tool.sh -t 3.0.2 -p kubernetes/dockerfiles/spark/bindings/python/Dockerfile build
kind load docker-image spark-py:3.0.2 --name=jupyter-test
```

### Python3 fix

While launching Pyspark jobs from Jupyter, where python version is 3.x, we'll get version mismatch errors because executors image has python 2.x as default.

- Edit python bindings Dockerfile

```
vi kubernetes/dockerfiles/spark/bindings/python/Dockerfile
```
```
34     pip3 install --upgrade pip setuptools pyspark && \
45 RUN ln -f /usr/bin/python3 /usr/bin/python
46 RUN ln -f /usr/bin/python3 /usr/bin/python2
```

- Build fixed image

```
bin/docker-image-tool.sh -t 3.0.2-py3-fix -p kubernetes/dockerfiles/spark/bindings/python/Dockerfile build
```

- Add image to kind cluster

```
kind load docker-image spark-py:3.0.2-py3-fix --name=jupyter-test
```

* Even with the fixes applied, launched python jobs will give us the following error on executors

```
Exception: Python in worker has different version 3.7 than that in driver 3.8, PySpark cannot run with different minor versions. Please check environment variables PYSPARK_PYTHON and PYSPARK_DRIVER_PYTHON are correctly set.
```

This error is not easy to fix, because we're using the official Jupyter image, built on top of ```Ubuntu 20.04.1``` base image with ```python 3.8``` installed, while the executors official Spark image is being built on top of ```Debian GNU/Linux 10``` with ```python 3.7```.

At this time, Pyspark is only able to launch jobs in ```client``` mode, that enforces the driver process to run within the Jupyter container, so the only option to make this work is to build a fully customized Jupyter or workers image ( or both ).

### Kubernetes

- Ingress controller ( https://kind.sigs.k8s.io/docs/user/ingress/#ingress-nginx )
    ```
    kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/static/provider/kind/deploy.yaml
    kubectl wait --namespace ingress-nginx --for=condition=ready pod --selector=app.kubernetes.io/component=controller --timeout=90s
    ```

- Jupyter resources

    ```
    kubectl apply -f k8s/rbac.yml
    kubectl apply -f k8s/deployment.yml
    kubectl wait -n jupyter --for=condition=ready pod --selector=app=jupyter --timeout=240s
    ```

### Connect to Jupyter console

- http://localhost/tree?token=9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08

### Connect to Jupyter console ( without ingress )

- Create tunnel against service

    ```
    kubectl -n jupyter port-forward service/jupyter-all-spark 8888
    ```

- Connect to Jupyter console, using the token defined in secrets

    http://localhost:8888/tree?token=9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08

- Copy dataset example file

    ```
    kubectl cp ./datasets/players_20.csv jupyter-all-spark-notebook-c5dc44cd9-kflxc:/data/dataset.csv
    ```

- From here, we can create a Python notebook from ```notebooks/simple-notebook.py```
