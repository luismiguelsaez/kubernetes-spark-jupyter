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

#conf = pyspark.SparkConf() \
#    .setMaster('k8s://https://kubernetes.default.svc.cluster.local:443') \
#    .set("spark.kubernetes.container.image", "spark-py:3.0.2") \
#    .set("spark.kubernetes.namespace","jupyter") \
#    .set("spark.kubernetes.authenticate.driver.serviceAccountName","jupyter") \
#    .set("spark.kubernetes.authenticate.caCertFile", "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt") \
#    .set("spark.kubernetes.authenticate.oauthTokenFile", "/var/run/secrets/kubernetes.io/serviceaccount/token") \
#    .set("spark.driverEnv.PYSPARK_PYTHON","python3") \
#    .set("spark.executorEnv.PYSPARK_PYTHON","python3") \
#    .set("spark.executor.instances", "2") \
#    .set("spark.jars", "") \
#    .set("spark.driver.host", "jupyter-all-spark-driver.jupyter.svc.cluster.local") \
#    .set("spark.driver.port", "29413")
#sc = pyspark.SparkContext(conf=conf)

rdd = sc.parallelize([1,2,3,4,5,6,7,8,9,10])
rdd.collect()
rdd.getNumPartitions()

#from pyspark.sql import SparkSession
#
#spark = SparkSession(sc)
#df = spark.read.csv('/opt/spark/work-dir/dataset.csv')
