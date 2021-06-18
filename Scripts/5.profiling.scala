import org.apache.spark.sql.{DataFrame, Row, SparkSession}

object Profiling {
  def readDataset(spark: SparkSession, pathCSV:String,
                  delim : String, multiline: Boolean,
                  ignoreTrailing: Boolean):DataFrame = {
    spark.read
      .option("header", "true").option("inferSchema", "true")
      .option("delimiter", delim).option("quote", "\"")
      .option("escape", "\"").option("multiline",multiline)
      .option("ignoreTrailingWhiteSpace", ignoreTrailing)
      .csv(s"$pathCSV")
  }

  //def readParquet(spark: SparkSession, path: String): DataFrame ={
  //  spark.read.load(s"$path")
  //}

  def run(spark: SparkSession): Unit ={
    val dsInfo = spark.read.option("header","true")
      .option("inferSchema","true")
      .option("escape", "\"")
      .csv("C:\\Users\\User\\Desktop\\TFG\\information_csv_all_datasets.csv")

    dsInfo.printSchema()

    var mapDS = Map[String, DataFrame]()
    var sourceDS = Map[String, String]()
    //
    dsInfo.select("filename","delimiter", "multiline","ignoreTrailing", "source").collect()
      .foreach{
              //
       case Row( filename: String, delimiter: String, multiline:Boolean , ignoreTrailing: Boolean, source:String) =>
            println(s"$filename $delimiter $multiline  $ignoreTrailing")
         //CSV
         mapDS = mapDS + (filename -> readDataset(spark, source,delimiter,multiline,ignoreTrailing))
         //Parquet
         //mapDS = mapDS + (filename -> readParquet(spark, source))
          //sourceDS = sourceDS + (filename -> source)
      }

    val listFiles = mapDS.keySet.toSeq


    for(f <- listFiles){
      println(s"profiling dataset ${f}")
      mapDS.get(f).get.printSchema()
      mapDS.get(f).get.attributeProfile()
      val profile_map = mapDS.get(f).get.getAttributeProfile
      val profile = profile_map.drop("FrequentWords", "FrequentWordsInSoundex", "firstWord", "lastWord")
      profile.coalesce(1).write.mode("overwrite").option("header","true")
        .csv("C:\\Users\\User\\Desktop\\TFG\\Profiles_all\\"+f.replace(".csv","_profile"))
    }
  }


  def main(args: Array[String]): Unit = {
    System.setProperty("hadoop.home.dir","C:\\Users\\User\\Desktop\\spark-3.0.1-bin-hadoop2.7\\winutils\\winutils")
    val spark = SparkSession.builder().master("local[*]").appName("test").getOrCreate()

    val sc = spark.sparkContext
    sc.setLogLevel("ERROR")

    run(spark)
  }

}