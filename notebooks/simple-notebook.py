from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .appName("SparkSessionTest") \
    .master('k8s://https://kubernetes.default.svc.cluster.local:443') \
    .config("spark.kubernetes.container.image", "spark-py:3.0.2") \
    .config("spark.kubernetes.namespace","jupyter") \
    .config("spark.kubernetes.authenticate.driver.serviceAccountName","jupyter") \
    .config("spark.kubernetes.authenticate.caCertFile", "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt") \
    .config("spark.kubernetes.authenticate.oauthTokenFile", "/var/run/secrets/kubernetes.io/serviceaccount/token") \
    .config("spark.driverEnv.PYSPARK_PYTHON","python3") \
    .config("spark.executorEnv.PYSPARK_PYTHON","python3") \
    .config("spark.executor.instances", "2") \
    .config("spark.jars", "") \
    .config("spark.driver.host", "jupyter-all-spark-driver.jupyter.svc.cluster.local") \
    .config("spark.driver.port", "29413") \
    .getOrCreate()

sc = spark.sparkContext

n = 100000 * 2

def f(_):
    x = random() * 2 - 1
    y = random() * 2 - 1
    return 1 if x ** 2 + y ** 2 < 1 else 0

from operator import add

count = sc.parallelize(range(1, n + 1), 2).map(f).reduce(add)
print("Pi is roughly %f" % (4.0 * count / n))

sc.stop()