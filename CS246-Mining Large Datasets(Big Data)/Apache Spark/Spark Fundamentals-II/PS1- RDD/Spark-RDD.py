from pyspark import SparkContext,SparkConf

"""Examine roles of partitions on join operation on resilient 
distributed datasets to be more efficient in keyed operations  
"""

#Set up spark context and configurations.
config = SparkConf()
sparkContext = SparkContext(conf = config)

"""Data consists of informations collected from bike share system in California. 
Specificly, We will use where trips start and end,then use those informations to join with station data. """

#Read files and exclude header informations
tripFile = sparkContext.textFile("Data//trips//trip_data.csv")
inputHeader = tripFile.first()
tripFile = tripFile.filter(lambda line: line != inputHeader) \
                            .map(lambda line: line.split(","))

stationFile = sparkContext.textFile("Data//stations//station_data.csv")
stationHeader = stationFile.first()
stationFile = stationFile.filter(lambda line: line != stationHeader) \
                            .map(lambda line: line.split(",")) \
                            .keyBy(lambda key: int(key[0])) \
                            .partitionBy(int(tripFile.getNumPartitions()))

#Perform join operation on equally partitioned datasets.
trip_start_points = stationFile.join(tripFile.keyBy(lambda trip: int(trip(4))))
trip_end_points = stationFile.join(tripFile.keyBy(lambda trip: int(trip(7))))