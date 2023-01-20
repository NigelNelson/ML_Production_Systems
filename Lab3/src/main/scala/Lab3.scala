
import org.apache.spark.sql.{DataFrame, Dataset, Row, SparkSession}

import java.util.Properties


object Lab3 extends  App {

  val spark: SparkSession = SparkSession.builder()
    .master("local[1]")
    .getOrCreate()

  spark.sparkContext.setLogLevel("ERROR")


  // Set S3 access properties
  spark.sparkContext
    .hadoopConfiguration.set("fs.s3a.access.key", "training_service")
  spark.sparkContext
    .hadoopConfiguration.set("fs.s3a.secret.key", "minioadmin")
  spark.sparkContext
    .hadoopConfiguration.set("fs.s3a.endpoint", "http://127.0.0.1:9000")
  spark.sparkContext
    .hadoopConfiguration.set("fs.s3a.connection.ssl.enabled", "false")

  // Read logs from Minio
  val df_original: DataFrame = spark
    .read
    .json("s3a://log-files/*.json")
  println("Original df length")
  println(df_original.count())

  // filter out by label === spam
  val df_spam: Dataset[Row] = df_original
    .filter(df_original("label") === "spam")
  println("Spam only filter df length:")
  println(df_spam.count())

  // Define Postgres properties
  val url = "jdbc:postgresql://127.0.0.1:5432/email_ingestion"
  val tableName = "emails"
  val props = new Properties()
  props.setProperty("user", "ingestion_service")
  props.setProperty("password", "puppet-soil-SWEETEN")

  // Read Postgres table into DataFrame
  val tableDf: DataFrame = spark.read
    .jdbc(url, tableName, props)
  println("Postgres df email count:")
  println(tableDf.count())

  // Join the Postgres dataframe table and the spam table
  val joinedDf = tableDf.join(df_spam, Seq("email_id"), "left_outer").dropDuplicates(Seq("email_id"))
  println("Joined table count:")
  println(joinedDf.count())

  // Write joined df to Minio
  joinedDf.coalesce(1).write.mode("overwrite").json("s3a://emails/ingestion_service")
}