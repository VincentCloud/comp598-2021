#!/bin/bash

STRING1="potus"
WORD2="\bfake\b"
FILE_PATH=$1
NUM_OF_ROWS_TO_CHECK=10000
LINE_START=99
LINE_END=200

line_count=$(wc -l < $FILE_PATH)

if [ $line_count -lt $NUM_OF_ROWS_TO_CHECK ]
then
  echo "The file is too small, get a file with more than ${NUM_OF_ROWS_TO_CHECK} lines"
else
  echo $line_count
  head -n 1 $FILE_PATH

  selected_rows=$(tail -n $NUM_OF_ROWS_TO_CHECK $FILE_PATH)

  echo $selected_rows | grep -io $STRING1 | wc -l

  selected_interval_rows=$(tail -n +$LINE_START $FILE_PATH | head -n $LINE_END)
  echo $selected_interval_rows | grep -o $WORD2 | wc -l

fi