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
     for identify stop words, we pick 5 times the average frequency as threshold, this script is run as:

     python ./genStopWords.py

2. building inverted index
  In this part, we build a mapper/reducer
  mapper : mapper.py
  reducer : reducer.py

  a. In mapper, each word in original file will be mapped to a line of:

        word  filename  chunk_Start_Point   relative_line_num_in_chunk  inline_offset

  b. Reducer will collect these information, for each word output a line of word followed
     by list of possible positions. Moreover, reducer will collect MAXIMUM line num of each
     chunk, and after output all word information, it outputs chunk_start_point->maximum_line
     as a dictionary leading by triple stars ( "***" )
  c. we put the text files in /tmp/data, set output directory to /tmp/out, running with cmd

     hadoop jar ${HADOOP_HOME}/share/hadoop/tools/lib/hadoop-streaming-2.7.1.jar -files mapper.py,reducer.py,stops.txt -mapper "mapper.py" -reducer "reducer.py" -input /tmp/data/* -output /tmp/out

  d. we grabbing the result, then rename it to out1.txt for further use, which is also provided.

3. query one word
  In this part, use script cmdQuery.py to query a word, with following format:
    python cmdQuery.py word

  This script will do the following:
  a. take out1.txt as input, first find "***" line, then convert the next line as a dictionary.
  b. the dictionary in previous step is for each chunk, not aggregate, the script then convert it to aggregate form:
     which like ["0":"100", "100":100, "200":100] -> ["0":0, "100":100, "200":200]
  c. then it will use the grabAWord function in process.py to find corresponding line in out1.txt, give the output.

4. web server
  In this part, use server.py to run a web server:

    python server.py

  Then you can open a browser, access URL http://127.0.0.1:8080/, input to the input box
  server.py will grab your input, then pass it to process function in process.py, which do the following:
  a. read in all stop words
  b. split the input of logical and text, for each word/words group, gives a list of [logical, word0, word1, ...]
  c. if any of the word is stop word, return with a warning
  d. build plain and aggregate chunk line count dictionary
  e1. if a single word, query that word in each line of step b
  e2. if a word group, call function grabConsecutiveWords.

  You'll see the output in the next page, if there is(are) logical connector(s) in query, the result page will first
  shows all single query result of each separate word(word group), and show the logical result at last.
