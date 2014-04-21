--------------------------------------------------------------------------------
MTE Search Tool                                           Copyright (C) 2013 CUE
--------------------------------------------------------------------------------

Tool to search MTE from a text file

Usage: MTE filename rules codesize minimum maximum total output

filename ... text file to analyze
rules ...... rules table file
codesize ... MTE code size
minimum .... minimum MTE string length
maximum .... maximum MTE string length
number ..... minimum number of occurrences
total ...... number of MTE to search
output ..... output file name


rules table file
-----------------
- the file must be an ASCII file
- empty lines are ignored
- starting spaces or tabulations are ignored
- comment lines, starting by ';', are ignored
- 'new line' must be CR+LF or LF
- character 0x00 is never permitted
- you can specify all non-permitted characters in a line starting by '.'
- you can specify a non-permitted character with their 2-bytes hexadecimal value
- you can specify codes to exclude text between both in a line starting by '-'

Example:
; rules example

; exclude numbers
.0123456789

0D ; exclude CR and LF
0A

-[] ; exclude text between square brackets
-{} ; exclude text between curly brackets

; end of rules example


history
-------
v1.0 ... 2013-02-22 ... first public version
v1.1 ... 2013-05-12 ... solved: when the rules file ends with a hexadecimal code
                               without CR/LF, the code was ignored
                        added: exclude the text between two codes (256 max)
                        added: minimum number of occurrences
                        added: write the total bytes saved
v1.2 ... 2013-07-29 ... added: control the MTE size in the operations
                        added: write the total MTE space size
                        added: write the minimum number of occurrences
                        solved: some rare situations with best_size=-1


--------------------------------------------------------------------------------
MTE Search Tool                                           Copyright (C) 2013 CUE
--------------------------------------------------------------------------------
