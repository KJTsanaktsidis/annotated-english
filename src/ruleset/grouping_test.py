#!/usr/bin/python3
#This guy runs through an integration test suite of grouping examples
from subprocess import Popen, PIPE

testcases = {
    r'cons\pln${e}c\nat{u}tive' : r'#c,@o,#ns,@\pln${e},#c,@\nat{u},#t,@i,#v,@e',
    r'science' : r'#sc,@ie,#nc,@e',
    r'de\si{b}t' : r'#d,@e,#t',
    r'f\brd{a}s\si{t}en' : r'#f,@\brd{a},#s,@e,#n',
    r'go\sel{}ing' : r'#g,@o <- @i,#\co{n}',
    r'diph\no{th}ong' : r'#d,@i,#ph\no{th},@o,#\co{n}',
    r'cry' : r'#cr,@y',
    r'boy\sel{}fr\si{i}end' : r'#b,@oy <- #fr,@e,#nd',
    r'b\si{u}ying' : r'#b,@yi,#\co{n}',
    r'flowing' : r'#fl,@owi,#\co{n}',
    r'\idp{ey}e' : r'@\idp{ey}e',
    r'when' : r'#\co{w},@e,#n',
    r'k\nat{i}w\nat{i}' : r'#k,@\nat{i},#w,@\nat{i}',
    r'b\iot{e}\ser{}ware' : r'#b,@\iot{e} -> #w,@a,#r,@e',
    r'cyan' : r'#c,@ya,#n',
    r'twine' : r'#tw,@i,#n,@e',
    r'gu\brd{a}tem\brd${a}la' : r'#\co{g}w,@\brd{a},#t,@e,#m,@\brd${a},#l,@a',
    r'g\brd{u}\co{r}\brd{u}' : r'#g,@\brd{u},#\co{r},@\brd{u}',
    r'g\si{h}\nat{o}st' : r'#g,@\nat{o},#st',
    r'ship\selr{}wreck' : r'#sh,@i,#p <<- #r,@e,#ck',
    r'peng\se{}\w{u}in' : r'#p,@e,#\co{n} - #\w{u},@i,#n',
    r'\co{g}\si{u}est' : r'#\co{g},@e,#st',
    r'qu\opq{a}lity' : r'#kw,@\opq{a},#l,@i,#t,@y',
    r'liquor' : r'#l,@i,#kw,@o,#r',
    r'\w{ou}\brd{i}ja' : r'#\w{ou},@\brd{i},#j,@a',
    r'a\ser{}way' : '@a -> #w,@ay'
}

successct = 0
failct = 0

for inword,outword in testcases.items():
    actualout = ''
    with Popen(['flookup', '-i', '-x', 'group.fst'], stdin=PIPE, stdout=PIPE) as p:
        actualout = p.communicate(input=inword.encode(encoding='UTF-8'))[0]
    utfout = actualout.decode(encoding='UTF-8')
    trimmedout = utfout.strip('\r\n ')
    if trimmedout == outword:
        successct += 1
    else:
        failct += 1
        print('Failed {} (expected ({}), got ({})'.format(inword, outword, trimmedout))

print('Passed: {}/{}, failed: {}/{}'.format(successct, len(testcases), failct, len(testcases)))
