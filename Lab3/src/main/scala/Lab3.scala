
import org.apache.spark.sql.{DataFrame, Dataset, Row, SparkSession}

import java.util.Properties


object Lab3 extends  App {

  val spark: SparkSession = SparkSession.builder()
    .master("local[1]")
    .getOrCreate()

  spark.sparkContext
    .hadoopConfiguration.set("fs.s3a.access.key", "training_service")
  spark.sparkContext
    .hadoopConfiguration.set("fs.s3a.secret.key", "minioadmin")
  spark.sparkContext
    .hadoopConfiguration.set("fs.s3a.endpoint", "http://127.0.0.1:9000")
  spark.sparkContext
    .hadoopConfiguration.set("fs.s3a.connection.ssl.enabled", "false")



  spark.sparkContext.setLogLevel("ERROR")

  /*
   Read logs
    */
  val df_original: DataFrame = spark
    .read
    .json("s3a://log-files/*.json")
  println("Original df length")
  println(df_original.count())

  // filter out by label === spam
  val df_spam: Dataset[Row] = df_original
    .filter(df_original("label") === "spam")
  println("Spam only filter df length")
  println(df_spam.count())


  /*
  Read emails from Postgres - not working yet
  https://spark.apache.org/docs/latest/sql-data-sources-jdbc.html
  https://hevodata.com/learn/spark-postgresql/

   */

  val url = "jdbc:postgresql://127.0.0.1:5432/email_ingestion"
  val tableName = "emails"
  val props = new Properties()
  props.setProperty("user", "ingestion_service")
  props.setProperty("password", "puppet-soil-SWEETEN")

  // read table into DataFrame
  val tableDf: DataFrame = spark.read
    .jdbc(url, tableName, props)
  println(tableDf.count())

  val joinedDf = tableDf.join(df_spam, tableDf("email_id") === df_spam("email_id"), "left_outer").drop(df_spam.id)
  println("Joined table count:")
  println(joinedDf.count())

  val allColumnNames=joinedDf.columns
  println(allColumnNames.mkString(","))

  joinedDf.write.json("s3a://emails/test")




}