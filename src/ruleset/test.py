#!/usr/bin/python3
#This guy runs through an integration test suite of grouping examples
from subprocess import Popen, PIPE

phase34_testcases = {
    r"night" : r"#n,@i\natpos{},#t",
    r'cons\pln${e}c\nat{u}tive' : r'#c,@o,#ns,@\pln${e},#c,@\nat{u},#t,@i,#v,@e',
    r'science' : r'#s\no{c},@ie,#n\no{c},@e',
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
    r'cyan' : r'#\no{c},@ya,#n',
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

phase35_testcases = {
    r'bait' : r'#b,@ai,#t',
    r'science' : r'#s\no{c},@i,@e,#n\no{c},@e',
    r'y\pln{e}ah' : r'#y,@\pln{e},@a',
    r'\nat{o}\st{a}\no{s}i\no{s}' : r'@\nat{o},@\st{a},#\no{s},@i,#\no{s}',
    r'f\brd{ie}ld' : r'#f,@\brd{ie},#ld',
    r's\brd{u}pral\st{i}ng\w{u}inal' : r'#s,@\brd{u},#pr,@a,#l,@\st{i},#\co{n}\co{g}\w{u},@i,#n,@a,#l',
    r'v\nat{e}\si{h}icle' : r'#v,@\nat{e},@i,#cl,@e',
    r'higher' : r'#h,@i\natpos{},@e,#r',
    r'heghit' : r"#h,@ei,#t",
    r"night" : r"#n,@i\natpos{},#t",
    r'a\ser{}way' : r'@a -> #w,@ay',
    r'flowing' : r'#fl,@ow,@i,#\co{n}',
    r'see-ing' : r'#s,@ee <- @i,#\co{n}',
    r'lion' : r'#l,@i,@o,#n',
    r'hallow\st{e}en' : r'#h,@a,#ll,@ow,@\st{e}e,#n',
    r'me\udp${ow}' : r'#m,@e,@\udp${ow}',
    r'sh\rnd{o}e' : r'#sh,@\rnd{o},@e',
    r'ha\se{}w\udp${ai}i' : r'#h,@a - #w,@\udp${ai},@i',
    r'\pln{e}dinbur\opq{gh}' : r'@\pln{e},#d,@i,#nb,@u,#r,@a',
    r'gluey' : r'#gl,@u,@ey',
    r'gluier' : r'#gl,@u,@i,@e,#r'
}

phase36_testcases = {
    r't\pln{e}l\iot{e}v\pln{i}\svo{si}on' : r"#t,@''\pln{e},#l,@\iot{e},#v,@'\pln{i},#\svo{si},@o,#n",
    r"out\se{}go\sel{}ing" : r"@ou,#t-#g,@'o-@i,#\co{n}",
    r"out\sel{}go\sel{}ing" : r"@'ou,#t-#g,@'o-@i,#\co{n}",
    r"\stst{o}utg\st{o}\se{}ing" : r"@''ou,#tg,@'o-@i,#\co{n}",
    r"ag\st{o}" : r"@a,#g,@'o",
    r"hou\no{s}e" : r"#h,@'ou,#\no{s},@e",
    r"yo-yo" : r"#y,@'o-#y,@o",
    r"ire\sel{}land" : r"@'i,#r,@e-#l,@a,#nd",
    r"complic\stst{a}te" : r"#c,@'o,#mpl,@i,#c,@''a,#t,@e",
    r"science" : r"#s\no{c},@'i,@e,#n\no{c},@e",
    r"ma\sno{ch}\st{i}ne" : r"#m,@a,#\sno{ch},@'i,#n,@e",
    r"ini\sno{t}ia\sno{ti}on" : r"@i,#n,@''i,#\sno{t},@i,@'a,#\sno{ti},@o,#n",
    r"r\pln$${e}pr\iot{e}senta\sno{ti}on" : r"#r,@''\pln{e},#pr,@\iot{e},#s,@e,#nt,@'a,#\sno{ti},@o,#n"
}

phase37_testcases = {
    r"so" : r"#|s,@'*+o",
    r"me" : r"#|m,@'*+e",
    r"my" : r"#|m,@'*+y",
    r"high" : r"#|h,@'*+i",
    r"night" : r"#|n,@'*+i,#|t",
    r"toe" : r"#|t,@'*+o,@_%+e",
    r"giant" : r"#|\hvo{g},@'*+i,@_%+a,#:nt",
    r"po\iot{e}t" : r"#|p,@'*+o,@_%+\iot{e},#|t",
    r"micro" : r"#|m,@'*+i,#|cr,@_%+o",
    r"plate" : r"#|pl,@'*+a,#|t,@_%+e",
    r"phony" : r"#:ph,@'*+o,#|n,@_%+y",
    r"dino\no{s}aur" : r"#|d,@'*+i,#|n,@_%+o,#|\no{s},@_%!au,#|r",
    r"able" : r"@'*+a,#|bl,@_%+e",
    r"idle" : r"@'*+i,#|dl,@_%+e",
    r"nucl\iot{e}ar" : r"#|n,@'*+u,#|cl,@_%+\iot{e},@_%+a,#|r",
    r"vague" : r"#|v,@'*+a,#|\co{g},@_%+e",
    r"saffron" : r"#|s,@'&+a,#:ffr,@_%+o,#|n",
    r"little" : r"#|l,@'&+i,#:ttl,@_%+e",
    r"twenty" : r"#:tw,@'&+e,#:nt,@_%+y",
    r"aqua" : r"@'&+a,#:kw,@_%+a",
    r"temple" : r"#|t,@'&+e,#:mpl,@_%+e",
    r"checking" : r"#:ch,@'&+e,#:ck,@_%+i,#|\co{n}",
    r"graphic" : r"#|gr,@'&+a,#:ph,@_%+i,#|c",
    r"pha\co{r}ynx" : r"#:ph,@'&+a,#:\co{r},@_%+y,#:nx",
    r"t\si{o}u\co{gh}er" : r"#|t,@'&+u,#:\co{gh},@_%+e,#|r",
    r"fate" : r"#|f,@'*+a,#|t,@_%+e",
    r"fat" : r"#|f,@'&+a,#|t",
    r"hungry" : r"#|h,@'&+u,#:\co{n}\co{g}r,@_%+y",
    r"winner" : r"#|w,@'&+i,#:nn,@_%+e,#|r",
    r"\iot{e}r\st{a}dic\nat{a}te" : r"@_%+\iot{e},#|r,@'*+a,#|d,@_%+i,#|c,@_%+\nat{a},#|t,@_%+e",
    r"\sno{s}ugar" : r"#|\sno{s},@'*+u,#|g,@_%+a,#|r",
    r"lantern" : r"#|l,@'&+a,#:nt,@_%+e,#:rn",
    r"player" : r"#|pl,@'&+ay,@_%+e,#|r",
    r"fair" : r"#|f,@'&!ai,#|r",
    r"laird" : r"#|l,@'&!ai,#:rd",
    r"fairy" : r"#|f,@'&!ai,#|r,@_%+y",
    r"ear\sel{}ring" : r"@'&!ea,#|r-#|r,@_%+i,#|\co{n}",
    r"card"  : r"#|c,@'&!a,#:rd",
    r"far" :  r"#|f,@'&!a,#|r",
    r"norm" : r"#|n,@'&!o,#:rm",
    r"first" : r"#|f,@'&!i,#:rst",
    r"her" : r"#|h,@'&!e,#|r",
    r"fir\sel{}ry" : r"#|f,@'&!i,#|r-#|r,@_%+y",
    r"pray\si{e}r" : r"#|pr,@'&!ay,#|r",
    r"may\si{o}r" : r"#|m,@'&!ay,#|r",
    r"err" : r"@'&!e,#:rr",
    r"whirr" : r"#|\co{w},@'&!i,#:rr",
    r"carry" : r"#|c,@'&+a,#:rr,@_%+y",
    r"mi\co{r}\iot{a}cle" : r"#|m,@'&+i,#:\co{r},@_%+\iot{a},#|cl,@_%+e"
}

def test(testcases, fst, name):
    successct = 0
    failct = 0

    for inword,outword in testcases.items():
        actualout = ''
        with Popen(['flookup', '-i', '-x', fst], stdin=PIPE, stdout=PIPE) as p:
            actualout = p.communicate(input=inword.encode(encoding='UTF-8'))[0]
        utfout = actualout.decode(encoding='UTF-8')
        trimmedout = utfout.strip('\r\n ')
        if trimmedout == outword:
            successct += 1
        else:
            failct += 1
            print('Failed {} (expected ({}), got ({})'.format(inword, outword, trimmedout))

    print('{}: Passed: {}/{}, failed: {}/{}'.format(name, successct, len(testcases), failct, len(testcases)))

test(phase34_testcases, 'phase34.fst', 'Phase 3.4 Grouping')
test(phase35_testcases, 'phase35.fst', 'Phase 3.5 Units')
test(phase36_testcases, 'phase36.fst', 'Phase 3.6 Stress')
test(phase37_testcases, 'phase37.fst', 'Phase 3.7 Vowel Catagorisation')
