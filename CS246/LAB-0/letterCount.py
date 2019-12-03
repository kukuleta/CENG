from pyspark import SparkContext,SparkConf
import re
import sys
"""
Write a Spark application which outputs the number of words that start with each
letter. This means that for every letter we want to count the total number of (non-
unique) words that start with that letter. In your implementation ignore the letter case,
i.e., consider all words as lower case. You can ignore all non-alphabetic characters."""

config = SparkConf() #Get configuration defaults
spark = SparkContext(conf=config) #Initialize spark context

#Take file path to read from command line that passed as argument
lines = spark.textFile(sys.argv[1])

# Following lines deal wih finding count of each letter appearing in first letter of each word.
letterCounts = lines.flatMap(lambda line: re.findall("\w+",line)) \
        .map(lambda word: word.lower()) \
        .filter(lambda word: re.match("[a-z]+",word)) \
        .map(lambda word: (word[0],1)) \
        .reduceByKey(lambda v1,v2: v1 + v2)
letterCounts.saveAsTextFile(sys.argv[2]) #Save output into file.
spark.stop()
