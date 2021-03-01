import pyspark


conf = pyspark.SparkConf() \
    .setMaster('k8s://https://kubernetes.default.svc.cluster.local:443') \
    .set("spark.kubernetes.container.image", "luismiguelsaez/spark:3.0.2-python") \
    .set("spark.kubernetes.namespace","jupyter") \
    .set("spark.kubernetes.authenticate.serviceAccountName","jupyter") \
    .set("spark.kubernetes.authenticate.driver.serviceAccountName","jupyter") \
    .set("spark.kubernetes.authenticate.caCertFile", "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt") \
    .set("spark.kubernetes.authenticate.oauthTokenFile", "/var/run/secrets/kubernetes.io/serviceaccount/token") \
    .set("spark.executor.instances", "2") \
    .set("spark.driver.host", "jupyter-all-spark-driver.jupyter.svc.cluster.local") \
    .set("spark.driver.port", "29413")

sc = pyspark.SparkContext(conf=conf)

rdd = sc.parallelize([1,2,3,4,5,6,7,8,9,10])
rdd.collect()
rdd.getNumPartitions()
