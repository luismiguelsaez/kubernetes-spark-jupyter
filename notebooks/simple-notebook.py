from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .appName("SparkSessionTest") \
    .master('k8s://https://kubernetes.default.svc.cluster.local:443') \
    .config("spark.submit.deployMode","client") \
    .config("spark.kubernetes.container.image", "spark-py:3.0.2-py3.8.8") \
    .config("spark.kubernetes.namespace","jupyter") \
    .config("spark.kubernetes.authenticate.driver.serviceAccountName","jupyter") \
    .config("spark.kubernetes.authenticate.caCertFile", "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt") \
    .config("spark.kubernetes.authenticate.oauthTokenFile", "/var/run/secrets/kubernetes.io/serviceaccount/token") \
    .config("spark.executorEnv.PYSPARK_MAJOR_PYTHON_VERSION","3") \
    .config("spark.executorEnv.PYSPARK_PYTHON","/usr/bin/python3") \
    .config("spark.executor.instances", "2") \
    .config("spark.executor.extraClassPath", "") \
    .config("spark.executor.extraJavaOptions", "") \
    .config("spark.jars", "") \
    .config("spark.files","") \
    .config("spark.driver.host", "jupyter-all-spark-driver.jupyter.svc.cluster.local") \
    .config("spark.driver.port", "29413") \
    .getOrCreate()

sc = spark.sparkContext

# PI calculation example

## Native

import numpy as np
from time import time
from random import random

inside = 0
n = 10000000

t_0 = time()
for i in range(n):
    x, y = random(), random()
    if x**2 + y**2 < 1:
        inside += 1
print(np.round(time()-t_0, 3), "seconds elapsed for naive method and n=", n)
print("pi is roughly", inside/n*4)

## Spark job

from time import time
import numpy as np
from random import random
from operator import add

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('CalculatePi').getOrCreate()
sc = spark.sparkContext

n = 10000000

def is_point_inside_unit_circle(p):
    # p is useless here
    x, y = random(), random()
    return 1 if x*x + y*y < 1 else 0

t_0 = time()

count = sc.parallelize(range(0, n)) \
             .map(is_point_inside_unit_circle).reduce(add)
print(np.round(time()-t_0, 3), "seconds elapsed for spark approach and n=", n)
print("Pi is roughly %f" % (4.0 * count / n))

# Destroy session
sc.stop()