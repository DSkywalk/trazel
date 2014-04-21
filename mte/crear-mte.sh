#!/bin/bash

BINARY=./mte
VECES=2
CHARS=5

ORGFILE="zelda_s.txt"
WRKFILE="wrk.out"
TMPFILE="/tmp/tmp.out"
STRTOREPLACE="#"



# PREPARE.... - 73,30 (5 - 2)  78,20 (2 - 5)

cp $ORGFILE $WRKFILE
> log.txt

IFS="$(printf '\n\r')"
LC_CTYPE=es_ES.iso88591
LANG=es_ES
LC_ALL=es_ES

REPLACE[0]=2
REPLACE[1]=16
REPLACE[2]=39
REPLACE[3]=37

for (( i = 0 ; i < ${#REPLACE[@]} ; i++ )) do
    let "CURCHARS=$CHARS-$i"
    echo "$CURCHARS = ${REPLACE[$i]}"

    OUT=`$BINARY $WRKFILE rules.txt 1 $CURCHARS $CURCHARS 2 1 ${REPLACE[$i]} out.txt`
    OUT=`awk -F\[ '{gsub("[\]]", " ", $NF); print $2}' out.txt 2> /dev/null`

    for TEXT in ${OUT[*]}; do
        VAR=`echo "$TEXT" | sed 's/ $//g'` # remove last space
        echo "SUBS:\"${VAR}\""
        #`sed -i.bak -e s/$VAR/$STRTOREPLACE/g $TMPFILE`
        awk -v OLD=${VAR} -v NEW=$STRTOREPLACE '
            ($0 ~ OLD) {gsub(OLD, NEW); count++}1
            END{ print count " substitutions occured with [" OLD "]" >> "log.txt" }
            ' "$WRKFILE" > $TMPFILE
        cp $TMPFILE $WRKFILE
    done

done


