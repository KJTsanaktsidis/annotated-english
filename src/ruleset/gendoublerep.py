#!/usr/bin/python3
import sys

#Generates rules of the form "x" "x" -> "x" ,,

tabs = "            "
preamble = "define DoubleReplace\n"
pattern = '"{}" "{}" -> "{}" ,, \n'

rule = preamble

for c in sys.argv[1]:
    rule += tabs + pattern.format(c, c, c)

#add a useless rule
rule += tabs + '"@" -> "@";'
print(rule)
