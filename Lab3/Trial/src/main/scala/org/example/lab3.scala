package org.example

import org.apache.spark.sql.SparkSession

object lab3 extends App{

//  System.setProperty("hadoop.home.dir", "=C:/hadoop/bin")
  val spark = SparkSession.builder()
    .master("local[1]")
    .getOrCreate();

  spark.sparkContext.setLogLevel("ERROR");


//  println("First SparkContext:")
//  println("APP Name :"+spark.sparkContext.appName);
//  println("Deploy Mode :"+spark.sparkContext.deployMode);
//  println("Master :"+spark.sparkContext.master);
//

//  val s3accessKeyAws = "minioadmin"
//  val s3secretKeyAws = "minioadmin"
//  val connectionTimeOut = "600000"
//  val s3endPointLoc: String = "http://127.0.0.1:9000"
//  val sourceBucket: String = "log-files"
//
//
//  spark.sparkContext.hadoopConfiguration.set("fs.s3a.endpoint", s3endPointLoc)
//  spark.sparkContext.hadoopConfiguration.set("fs.s3a.access.key", s3accessKeyAws)
//  spark.sparkContext.hadoopConfiguration.set("fs.s3a.secret.key", s3secretKeyAws)
//  spark.sparkContext.hadoopConfiguration.set("fs.s3a.connection.timeout", connectionTimeOut)
//
//  spark.sparkContext.hadoopConfiguration.set("spark.sql.debug.maxToStringFields", "100")
//  spark.sparkContext.hadoopConfiguration.set("fs.s3a.path.style.access", "true")
//  spark.sparkContext.hadoopConfiguration.set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
//  spark.sparkContext.hadoopConfiguration.set("fs.s3a.connection.ssl.enabled", "true")
//
////  val inputPath: String = s"s3a://$sourceBucket/2023-01-10_10-30.json"
//  val inputPath: String = s"s3a://$sourceBucket/test_clean.csv"


//  val json_minio = spark
//    .read
//    .format("s3selectJson")
//    .load(inputPath)


  /*
  Read logs
   */
  val df_original = spark
    .read
    .json("./2023-01-10_10-30.json")
  println("Original df length")
  println(df_original.count())

  // filter out by label === spam
  val df_spam = df_original
    .filter(df_original("label") === "spam")
  println("Spam only filter df length")
  println(df_spam.count())

  
  /*
  Read emails from Postgres - not working yet
  https://spark.apache.org/docs/latest/sql-data-sources-jdbc.html
  https://hevodata.com/learn/spark-postgresql/

   */
  val df_post = spark.read
  .format("jdbc")
  .option("url", "jdbc:postgresql://localhost:5432/email_ingestion")
  .option("dbtable", "emails")
  .option("user", "ingestion_service")
  .option("password", "puppet-soil-SWEETEN")
  .option("driver", "org.postgresql.Driver")
  .load()

  println(df_post.schema)

}
