In PA2, we pick five production of William Shakespeare， which are:
  THE SONNETS : pg1041.txt
  THE TRAGEDY OF JULIUS CAESAR : pg1120.txt
  A Midsommer Nights Dreame : pg2242.txt
  The Merchant of Venice : pg2243.txt
  The Tragedie of Hamlet : pg2265.txt

  i.   We convert all words to lower case and use regular express to keep ONLY a-z characters,
       so "you'l" will be convert to "youl"
  ii.  We make all the outputs 1-indexed
  iii. please make sure out0.txt, out1.txt is located in the same folder for step 3, 4.

1. building stop word list
  In this part, we run a simple map-reduce of word count,
  mapper : mapper0.py
  reducer : reducer0.py
  a. we put the text files in /tmp/data, set output directory to /tmp/out0, running with cmd

     hadoop jar ${HADOOP_HOME}/share/hadoop/tools/lib/hadoop-streaming-2.7.1.jar -files mapper0.py,reducer0.py -mapper "mapper0.py" -reducer "reducer0.py" -input /tmp/data/* -output /tmp/out0

  b. After grabbing the result, we rename it to out0.txt, which is also provided.
  c. Then use script genStopWords.py which takes out0.txt as input and output stop words to stops.txt,
     for identifying stop words, we pick a threshold such that it is 5 times the average frequency. 
     To run the script:

     python ./genStopWords.py

2. building inverted index
  In this part, we build a mapper/reducer
  mapper : mapper.py
  reducer : reducer.py

  a. In mapper, each word in the original file will be mapped to a line of:

        word  filename  chunk_Start_Point   relative_line_num_in_chunk  inline_offset

  b. Reducer will collect this information for each word, and output the line of the word followed
     by a list of possible positions. Moreover, reducer will store the MAXIMUM line num of each
     chunk, and after all word information has been output, it then outputs chunk_start_point->maximum_line
     as a dictionary prepended by triple stars ( "***" )
  c. we put the text files in /tmp/data, set output directory to /tmp/out. 
     To run the command:

     hadoop jar ${HADOOP_HOME}/share/hadoop/tools/lib/hadoop-streaming-2.7.1.jar -files mapper.py,reducer.py,stops.txt -mapper "mapper.py" -reducer "reducer.py" -input /tmp/data/* -output /tmp/out

  d. we grab the result, and rename it to out1.txt for further use, which is also provided.

3. query one word
  In this part, the script cmdQuery.py is used to query a word with the following format:
    python cmdQuery.py word

  This script will do the following:
  a. take out1.txt as input, first it finds the line prepended with "***", then it converts the next line into a dictionary.
  b. the dictionary in previous step is not aggregate in its raw form, but the script converts it to aggregate form:
     which is of the form ["0":"100", "100":100, "200":100] -> ["0":0, "100":100, "200":200]
  c. then it will use the grabAWord function in process.py to find the corresponding line in out1.txt, and give the output.

4. web server
  In this part, use server.py to run a web server:

    python server.py

  Then you can open a browser and access URL http://127.0.0.1:8080/ where you will provide input to the input box.
  server.py will grab your input, then pass it to the process function in process.py, which does the following:
  a. read in all stop words
  b. split the input of logical and text, for each word/words group, gives a list of [logical, word0, word1, ...]
  c. if any of the words is a stop word, return with a warning
  d. build a plain and aggregate chunk line count dictionary
  e1. if a single word, query that word in each line of step b
  e2. if a word group, call function grabConsecutiveWords.

  You'll see the output in the next page. If there is(are) logical connector(s) in a query, the result page will first
  show all single query results of each separate word(word group), then it will show the logical result at the end of the output.
