
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

### Python executors image build

While launching Pyspark jobs from Jupyter, where python version is 3.x, we'll get version mismatch errors because executors image has python 2.x as default. This happens because, in pyspark client mode, the driver runs in Jupyter container ( based on Ubuntu 20.04 ) and the executors runs on provided executor images ( built on top of Debian 10 ); those images have different python versions.

- Build fixed image

Follow [README.md](build/README.md) steps from ```build``` directory. From there, we will build a python bindings custom image, building the needed python version from code on the executor image.

### Kubernetes

- Ingress controller ( https://kind.sigs.k8s.io/docs/user/ingress/#ingress-nginx )
    ```
    kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/static/provider/kind/deploy.yaml
    kubectl wait --namespace ingress-nginx --for=condition=ready pod --selector=app.kubernetes.io/component=controller --timeout=90s
    ```

- Jupyter resources ( static )

    ```
    kubectl apply -f k8s/rbac.yml
    kubectl apply -f k8s/deployment.yml
    kubectl wait -n jupyter --for=condition=ready pod --selector=app=jupyter --timeout=240s
    ```

- Jupyter resources from Helm chart

  ```
  helm install jupyter-notebook helm/jupyter-spark
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
