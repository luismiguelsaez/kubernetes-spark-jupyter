
# Spark + Jupyter notebooks

## Documentation

Jupyter deployment is based on official images, as described in the following webpages:

- https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-all-spark-notebook
- https://github.com/jupyter/docker-stacks/tree/master/all-spark-notebook

Client mode execution is described here:

- https://spark.apache.org/docs/latest/running-on-kubernetes.html#client-mode


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

### Kubernetes

- Ingress controller ( https://kind.sigs.k8s.io/docs/user/ingress/#ingress-nginx )
    ```
    kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/static/provider/kind/deploy.yaml
    ```

- Jupyter resources

    ```
    kubectl apply -f k8s/rbac.yml
    kubectl apply -f k8s/deployment.yml
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
