STATS_FILE="/Users/aalcedo/repos/stats.txt"
OUTPUT="/Users/aalcedo/repos/output.txt"
FINAL_FILE="/Users/aalcedo/repos/final.txt"
BACKUP_EXTENSION="bck"

echo "INIT STATISTICS SCRIPT `date` "$'\r' >> /Users/aalcedo/repos/stats.txt

for file in /Users/aalcedo/repos/stats/*
do
    if [ -d "$file" ]
    then
        cd $file
        if [ -d ".git" ]
        then
            echo "`date` ---------- $file ----------"$'\r' >> $STATS_FILE
            git pull origin
            COMMAND="git-quick-stats -T"
            eval ${COMMAND} >> $STATS_FILE
        fi
    fi
done

echo $'\r' >> $STATS_FILE

TOTAL_NUMBER_OF_LINES=$(wc -l < $STATS_FILE | xargs)
START_LINE_WITH_NEW_STATS=$(grep -n "INIT STATISTICS SCRIPT" $STATS_FILE | tail -1 | cut -d : -f 1 | xargs)
FIRST_LINE_STATS=$[TOTAL_NUMBER_OF_LINES - START_LINE_WITH_NEW_STATS]
COMMAND="tail -n $FIRST_LINE_STATS '$STATS_FILE'"

eval ${COMMAND} >> $OUTPUT

# Remove all lines with first commit
COMMAND="rm \"$OUTPUT$BACKUP_EXTENSION\""
eval ${COMMAND}
COMMAND="sed -i '$BACKUP_EXTENSION' '/first commit/d' $OUTPUT"
eval ${COMMAND}

# Remove all lines with last commit
COMMAND="rm \"$OUTPUT$BACKUP_EXTENSION\""
eval ${COMMAND}
COMMAND="sed -i '$BACKUP_EXTENSION' '/last commit/d' $OUTPUT"
eval ${COMMAND}

# Remove all lines with lines changed
COMMAND="rm \"$OUTPUT$BACKUP_EXTENSION\""
eval ${COMMAND}
COMMAND="sed -i '$BACKUP_EXTENSION' '/lines changed/d' $OUTPUT"
eval ${COMMAND}

# Replace all the (xxxxx%) for a comma ,
COMMAND="rm \"$OUTPUT$BACKUP_EXTENSION\""
eval ${COMMAND}
COMMAND="sed -i '$BACKUP_EXTENSION' -E 's/\([0-9]+\%\)/,/' $OUTPUT"
eval ${COMMAND}

# Remove all lines with insertions, deletions, files, commits
COMMAND="rm \"$OUTPUT$BACKUP_EXTENSION\""
eval ${COMMAND}
COMMAND="sed -i '$BACKUP_EXTENSION' -E 's/insertions:/ /' $OUTPUT"
eval ${COMMAND}
COMMAND="rm \"$OUTPUT$BACKUP_EXTENSION\""
eval ${COMMAND}
COMMAND="sed -i '$BACKUP_EXTENSION' -E 's/deletions:/ /' $OUTPUT"
eval ${COMMAND}
COMMAND="rm \"$OUTPUT$BACKUP_EXTENSION\""
eval ${COMMAND}
COMMAND="sed -i '$BACKUP_EXTENSION' -E 's/files:/ /' $OUTPUT"
eval ${COMMAND}
COMMAND="rm \"$OUTPUT$BACKUP_EXTENSION\""
eval ${COMMAND}
COMMAND="sed -i '$BACKUP_EXTENSION' -E 's/commits:/ /' $OUTPUT"
eval ${COMMAND}


rm $FINAL_FILE
# Read output line by line
PREVIOUS_LINE=""
while read line;
do

  if [[ $line == *"----------"* ]];
  then
    READING_USER=0
  fi

  if [[ $line == *"Contribution stats"* ]];
  then
    READING_USER=0
    echo "$PREVIOUS_LINE" >> $FINAL_FILE
  fi

  if [[ $line == *"@"* ]];
  then
    echo "$USER_LINE" >> $FINAL_FILE
    USER_LINE=""
    READING_USER=1
  fi

  if [[ $line == *"total:"* ]];
  then
    READING_USER=2
  fi

  if [[ $READING_USER > 0 ]];
  then
    USER_LINE="$USER_LINE  $line"
  fi

  PREVIOUS_LINE=$line
done < $OUTPUT
