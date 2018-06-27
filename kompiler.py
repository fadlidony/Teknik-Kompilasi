from sys import *

tokens = []
tokens_expresion = []
num_stack = []
symbols = {}
line = 0

def open_file(filename):
    data = open(filename, "r"). read()
    data += "[EOF]"
    return data

def lex(filecontents):
    tok = ""
    num_expr = 0
    state = 0
    isexpr = 0
    isjika = 0
    jumlah_tokens =0
    varStarted = 0
    var = ""
    string = ""
    expr = ""
    ulang = ""
    n = 0
    selesai = 0
    ekspresi_kondisi = ""
    global line
    filecontents = list(filecontents)
    for char in filecontents:
        selesai = 0
        tok += char
        if tok == " " and varStarted==0:
            if state == 0:
                tok = ""
            else:
                tok = " "
        elif tok == "\n" or tok == "[EOF]":
            if tok!="" and n!=0:
                    line+=1
                    n=0
            if expr != "" and isexpr == 1:
                tokens.append("EXPR:" + expr)
                n+=1
                expr = ""
            elif expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                n+=1
                expr = ""
            if var != "":
                tokens.append("VAR:"+var)
                n+=1
                var = ""
                varStarted = 0
            tok = ""
            selesai=1
        elif tok == "=" and state == 0:
            if expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                n+=1
                expr = ""
            if var != "":
                tokens.append("VAR:"+var)
                n+=1
                var = ""
                varStarted = 0
            if tokens[-1] == "EQUALS" or tokens[-1] == "LEBIH" or tokens[-1] == "KURANG":
                if tokens[-1] == "EQUALS":
                    tokens[-1] = "EQEQ"
                elif tokens[-1] == "LEBIH":
                    tokens[-1] = "LEBIHSAMA"
                elif tokens[-1] == "KURANG":
                    tokens[-1] = "KURANGSAMA"
                n+=1
            else:
                tokens.append("EQUALS")
                n+=1
            tok = ""
        elif (tok == ">" or tok=="<") and state == 0:
            if expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                n+=1
                expr = ""
            if var != "":
                tokens.append("VAR:"+var)
                n+=1
                var = ""
                varStarted = 0
            if tokens[-1] == "EQUALS":
                tokens[-1] = "EQEQ"
                n+=1
            else:
                if tok == ">":
                    tokens.append("LEBIH")
                elif tok == "<":
                    tokens.append("KURANG")
                n+=1
            tok = ""
        elif tok == "$" and state == 0:
            varStarted = 1
            var += tok
            tok = ""
        elif varStarted == 1:

            if tok =="[" or tok == "]"  or tok == " " or tok == "+" or tok == "-" or tok == "/" or tok == "*" or tok == "(" or tok == ")":
                if var !="":
                    tokens.append("VAR:"+var)
                    n+=1
                    var = ""
                    varStarted = 0
            elif tok == "\n":
               # print "tok enter"
            # elif tok == "+" or tok == "-" or tok == "/" or tok == "*" or tok == "(" or tok == ")":
            #     if var != "":
            #         tokens.append("VAR:"+var)
            #         n+=1
            #         var = ""
            #         varStarted = 0
            var += tok
            if var == " ":
                var=""
            if tok =="[":
                tok = "["
                var=""
            elif tok == "+" or tok == "-" or tok == "/" or tok == "*" or tok == "(" or tok == ")":
                isexpr = 1
                expr += tok
                tok = ""
                var=""
            else:
                tok = ""
        elif tok == "TULIS" or tok == "tulis":
            tokens.append("NULIS")
            tok = ""
            n+=1
        elif tok == "ENDJIKA" or tok == "endjika":
            tokens.append("ENDIF")
            n+=1
            tok = ""
        elif tok == "ENDULANG" or tok == "endulang":
            tokens.append("ENDULANG")
            n+=1
            tok = ""
        elif tok == "JIKA" or tok == "jika":
            tokens.append("JIKA")
            tok = ""
            isjika=1
            n+=1
        elif tok == "ULANG" or tok == "ulang":
            tokens.append("ULANG")
            tok = ""
            n+=1
        elif tok == "MAKA" or tok == "maka":
            if expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                expr = ""
            tokens.append("MAKA")
            tok = ""
            n+=1
        elif tok == "LAKUKAN" or tok == "lakukan":
            if expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                expr = ""
            tokens.append("LAKUKAN")
            tok = ""
            n+=1
        elif tok == "DAN" or tok == "dan":
            if expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                expr = ""
            tokens.append("DAN")
            n+=1
            tok = ""
        elif tok == "kalautidak" or tok == "KALAUTIDAK":
            if expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                expr = ""
            n+=1
            tokens.append("KALAUTIDAK")
            tok = ""
        elif tok == "BACA" or tok == "baca":
            n+=1
            tokens.append("BACA")
            tok = ""
        elif (tok == "0" or tok == "1" or tok == "2" or tok == "3" or tok == "4" or tok == "5" or tok == "6" or tok == "7" or tok == "8" or tok == "9") and state==0:
            expr += tok
            tok = ""
        elif tok == "+" or tok == "-" or tok == "/" or tok == "*" or tok == "(" or tok == ")":
            isexpr = 1
            expr += tok
            tok = ""
        elif tok =="\t":
            tok = ""
        elif tok == "\"" or tok == " \"":
            if state == 0:
                state = 1
            elif state == 1:
                tokens.append("STRING:" + string + "\"")
                n+=1
                string = ""
                state = 0
                tok = ""
        elif state == 1:
            string += tok
            tok = ""
    #print(tokens)
    if selesai==0:
        if len(tokens)==0:
            pesan= "Sintax Error : Periksa kembali argumen baris ke - 1"
            print(pesan)
            exit()
        else:
            pesan= "Sintax Error : Periksa kembali argumen baris ke - "+str(line)
            print(pesan)
            exit()

    return tokens

def evalExpression(expr):

    return eval(expr)


def doNULIS(toNULIS):
    if(toNULIS[0:6] == "STRING"):
        toNULIS = toNULIS[8:]
        toNULIS = toNULIS[:-1]
    elif(toNULIS[0:3] == "NUM"):
        toNULIS = toNULIS[4:]
    elif(toNULIS[0:4] == "EXPR"):
        toNULIS = evalExpression(toNULIS[5:])
    print(toNULIS)

def getSTRING(toNULIS):
    if(toNULIS[0:6] == "STRING"):
        toNULIS = toNULIS[8:]
        toNULIS = toNULIS[:-1]
    elif(toNULIS[0:3] == "NUM"):
        toNULIS = toNULIS[4:]
    elif(toNULIS[0:4] == "EXPR"):
        toNULIS = evalExpression(toNULIS[5:])
    return toNULIS

def doASSIGN(varname, varvalue):
    symbols[varname[4:]] = varvalue

def getVARIABLE(varname):
    varname = varname[4:]
    if varname in symbols:
        return symbols[varname]
    else:
        return "VARIABEL ERROR: variabel tidak terdefinisi"
        exit()

def getBACA(string, varname):
    i = raw_input(string[1:-1]+ " ")
    try:
        int(i)
        symbols[varname] = "NUM:"+i
    except:
        symbols[varname] = "STRING:\"" +i +"\""

def parse(toks):
    i = 0
    jikamaka = 0
    kondisi = 1
    loop = 0
    n_toks_loop = 0
    t = 0
    toks_loop = []
    while(i<len(toks)):
        if toks[i]=="ULANG":
            t=5
            while toks[i+t] != "ENDULANG":
                toks_loop.append(toks[i+t])
                t+=1
            n_toks_loop=len(toks_loop)
            i+=5
        else:
            i+=1
    i=0
    # print n_toks_loop
    while(i < len(toks)):
            if toks[i] == "KALAUTIDAK":
                if kondisi == 0:
                     kondisi = 1
                elif kondisi ==1:
                     kondisi =0
                i+=1
            elif toks[i] == "ENDIF":
                jikamaka -= 1
                kondisi =1
                i+=1
            elif toks[i] == "ENDULANG":
                if loop == 1:
                    i=i-n_toks_loop-5
                elif loop ==0:
                    i+=1
            elif toks[i]== "NULIS":
                if kondisi == 1:
                    try:
                        if toks[i+1][0:6] == "STRING":
                            doNULIS(toks[i+1])
                        elif toks[i+1][0:3] == "NUM":
                            doNULIS(toks[i+1])
                        elif toks[i+1][0:4] == "EXPR":
                            doNULIS(toks[i+1])
                        elif toks[i+1][0:3] == "VAR":
                            doNULIS(getVARIABLE(toks[i+1]))
                        else:
                            print ("Syntax Error : Penulisan argumen \"TULIS\" salah, periksa kembali argumen baris ke - "+ str(line))
                            exit()
                    except:
                        print("Sintax Error : Penulisan argumen \"TULIS\" salah, periksa kembali argumen baris ke - "+ str(line))
                i+=2
            elif toks[i][0:3] + " " + toks[i+1]== "VAR EQUALS":
                if kondisi == 1:
                    try:
                        if toks[i+2][0:3] + " " + toks[i+3][0:4]== "VAR EXPR":
                            doASSIGN(toks[i], "NUM:" + str(evalExpression(getVARIABLE(toks[i+2])[4:]+toks[i+3][5:])))
                            i+=4
                        elif toks[i+2][0:4] + " " + toks[i+3][0:3]== "EXPR VAR":
                            doASSIGN(toks[i], "NUM:" + str(evalExpression(toks[i+2][5:]+getVARIABLE(toks[i+3])[4:])))
                            i+=4
                        elif toks[i+2][0:6] == "STRING":
                            doASSIGN(toks[i], toks[i+2])
                            i+=3
                        elif toks[i+2][0:3] == "NUM":
                            doASSIGN(toks[i], toks[i+2])
                            i+=3
                        elif toks[i+2][0:4] == "EXPR":
                            doASSIGN(toks[i], "NUM:" + str(evalExpression(toks[i+2][5:])))
                            i+=3
                        elif toks[i+2][0:3] == "VAR":
                            doASSIGN(toks[i], getVARIABLE(toks[i+2]))
                            i+=3
                    except:
                    # print(str(evalExpression(toks[i+2][5:])))
                        if toks[i+2][0:6] == "STRING":
                            doASSIGN(toks[i], toks[i+2])
                        elif toks[i+2][0:3] == "NUM":
                            doASSIGN(toks[i], toks[i+2])
                        elif toks[i+2][0:4] == "EXPR":
                            doASSIGN(toks[i], "NUM:" + str(evalExpression(toks[i+2][5:])))
                        elif toks[i+2][0:3] == "VAR":
                            doASSIGN(toks[i], getVARIABLE(toks[i+2]))
                        i+=3
            elif (toks[i] + " " + toks[i+1][0:6] + " " + toks[i+2][0:3] == "BACA STRING VAR") and kondisi == 1:
                if kondisi == 1:
                    try:
                        getBACA(toks[i+1][7:],toks[i+2][4:])
                    except:
                        print("Sintax Error : Penulisan argumen \"BACA\" salah, periksa kembali argumen baris ke - "+ str(line))
                        exit()
                i+=3
            elif toks[i] == "JIKA":
                jikamaka +=1
                if toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3]=="NUM EQEQ NUM":
                    if toks[i+1][4:] == toks[i+3][4:]:
                        kondisi=1
                    else:
                        kondisi=0
                    i+=5
                elif toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3]=="NUM LEBIH NUM":
                    if int(toks[i+1][4:]) > int(toks[i+3][4:]):
                        kondisi=1
                    else:
                        kondisi=0
                    i+=5
                elif toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3]=="NUM LEBIHSAMA NUM":
                    if int(toks[i+1][4:]) >= int(toks[i+3][4:]):
                        kondisi=1
                    else:
                        kondisi=0
                    i+=5
                elif toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3]=="NUM KURANG NUM":
                    if int(toks[i+1][4:]) < int(toks[i+3][4:]):
                        kondisi=1
                    else:
                        kondisi=0
                    i+=5
                elif toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3]=="NUM KURANGSAMA NUM":
                    if int(toks[i+1][4:]) <= int(toks[i+3][4:]):
                        kondisi=1
                    else:
                        kondisi=0
                    i+=5
                elif toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3]=="VAR EQEQ VAR":
                    if getVARIABLE(toks[i+1]) == getVARIABLE(toks[i+3]):
                        kondisi=1
                    else:
                        kondisi=0
                    i+=5
                elif toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3]=="VAR LEBIH VAR":
                    try:
                        if int(getVARIABLE(toks[i+1])[4:]) > int(getVARIABLE(toks[i+3])[4:]):
                            kondisi=1
                        else:
                            kondisi=0
                        i+=5
                    except:
                        print("Sintaks Error : Penulisan variabel tidak benar pada argumen \"JIKA\"")
                        exit()
                elif toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3]=="VAR LEBIHSAMA VAR":
                    try:
                        if int(getVARIABLE(toks[i+1])[4:]) >= int(getVARIABLE(toks[i+3])[4:]):
                            kondisi=1
                        else:
                            kondisi=0
                        i+=5
                    except:
                        print("Sintaks Error : Penulisan variabel tidak benar pada argumen \"JIKA\"")
                        exit()
                elif toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3]=="VAR KURANG VAR":
                    try:
                        if int(getVARIABLE(toks[i+1])[4:]) < int(getVARIABLE(toks[i+3])[4:]):
                            kondisi=1
                        else:
                            kondisi=0
                        i+=5
                    except:
                        print("Sintaks Error : Penulisan variabel tidak benar pada argumen \"JIKA\"")
                        exit()
                elif toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3]=="VAR KURANGSAMA VAR":
                    try:
                        if int(getVARIABLE(toks[i+1])[4:]) <= int(getVARIABLE(toks[i+3])[4:]):
                            kondisi=1
                        else:
                            kondisi=0
                        i+=5
                    except:
                        print("Sintaks Error : Penulisan variabel tidak benar pada argumen \"JIKA\"")
                        exit()
                elif toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3]=="VAR EQEQ NUM":
                    try:
                        if getVARIABLE(toks[i+1])[4:] == toks[i+3][4:]:
                            kondisi=1
                        else:
                            kondisi=0
                        i+=5
                    except:
                        print("Sintaks Error : Penulisan variabel tidak benar pada argumen \"JIKA\"")
                        exit()
                elif toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3]=="VAR LEBIH NUM":
                    try:
                        if int(getVARIABLE(toks[i+1])[4:]) > toks[i+3][4:]:
                            kondisi=1
                        else:
                            kondisi=0
                        i+=5
                    except:
                        print("Sintaks Error : Penulisan variabel tidak benar pada argumen \"JIKA\"")
                        exit()
                elif toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3]=="VAR LEBIHSAMA NUM":
                    try:
                        if int(getVARIABLE(toks[i+1])[4:]) >= toks[i+3][4:]:
                            kondisi=1
                        else:
                            kondisi=0
                        i+=5
                    except:
                        print("Sintaks Error : Penulisan variabel tidak benar pada argumen \"JIKA\"")
                        exit()
                elif toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3]=="VAR KURANG NUM":
                    try:
                        if int(getVARIABLE(toks[i+1])[4:]) < toks[i+3][4:]:
                            kondisi=1
                        else:
                            kondisi=0
                        i+=5
                    except:
                        print("Sintaks Error : Penulisan variabel tidak benar pada argumen \"JIKA\"")
                        exit()
                elif toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3]=="VAR KURANGSAMA NUM":
                    try:
                        if int(getVARIABLE(toks[i+1])[4:]) <= toks[i+3][4:]:
                            kondisi=1
                        else:
                            kondisi=0
                        i+=5
                    except:
                        print("Sintaks Error : Penulisan variabel tidak benar pada argumen \"JIKA\"")
                        exit()
                elif toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3]=="NUM EQEQ VAR":
                    if toks[i+1][4:] == getVARIABLE(toks[i+3])[4:]:
                        kondisi=1
                    else:
                        kondisi=0
                    i+=5
                elif toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3]=="NUM LEBIH VAR":
                    try:
                        if int(toks[i+1][4:]) > int(getVARIABLE(toks[i+3])[4:]):
                            kondisi=1
                        else:
                            kondisi=0
                        i+=5
                    except:
                        print("Sintaks Error : Penulisan variabel tidak benar pada argumen \"JIKA\"")
                        exit()
                elif toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3]=="NUM LEBIHSAMA VAR":
                    try:
                        if int(toks[i+1][4:]) >= int(getVARIABLE(toks[i+3])[4:]):
                            kondisi=1
                        else:
                            kondisi=0
                        i+=5
                    except:
                        print("Sintaks Error : Penulisan variabel tidak benar pada argumen \"JIKA\"")
                        exit()
                elif toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3]=="NUM KURANG VAR":
                    try:
                        if int(toks[i+1][4:]) < int(getVARIABLE(toks[i+3])[4:]):
                            kondisi=1
                        else:
                            kondisi=0
                        i+=5
                    except:
                        print("Sintaks Error : Penulisan variabel tidak benar pada argumen \"JIKA\"")
                        exit()
                elif toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3]=="NUM KURANGSAMA VAR":
                    try:
                        if int(toks[i+1][4:]) <= int(getVARIABLE(toks[i+3])[4:]):
                            kondisi=1
                        else:
                            kondisi=0
                        i+=5
                    except:
                        print("Sintaks Error : Penulisan variabel tidak benar pada argumen \"JIKA\"")
                        exit()
                elif toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:6]=="VAR EQEQ STRING":
                    if getSTRING(getVARIABLE(toks[i+1])) == getSTRING(toks[i+3]):
                        kondisi=1
                    else:
                        kondisi=0
                    i+=5
                elif toks[i+1][0:6] + " " + toks[i+2] + " " + toks[i+3][0:3]=="STRING EQEQ VAR":
                    if getSTRING(toks[i+1]) == getSTRING(getVARIABLE(toks[i+3])):
                        kondisi=1
                    else:
                        kondisi=0
                    i+=5
                elif toks[i+1][0:6] + " " + toks[i+2] + " " + toks[i+3][0:3]=="STRING EQEQ VAR":
                    if getSTRING(toks[i+1]) == getSTRING(getVARIABLE(toks[i+3])):
                        kondisi=1
                    else:
                        kondisi=0
                    i+=5
                else:
                    print ("Sintax error: Kalimat \"Jika Maka\" tidak benar, coba periksa kembali")
                    exit()
            elif toks[i]=="ULANG":
                # print "Pengulangan terdeteksi"
                # print "kondisi:"+str(loop)
                if toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3]=="NUM KURANGSAMA VAR":
                    try:
                        if int(toks[i+1][4:]) <= int(getVARIABLE(toks[i+3])[4:]):
                            loop=1
                        else:
                            loop=0
                            i+=n_toks_loop
                    except:
                        print("Sintaks Error : Penulisan variabel tidak benar pada argumen \"ULANG\"")
                        exit()
                elif toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3]=="NUM KURANG VAR":
                    try:
                        if int(toks[i+1][4:]) < int(getVARIABLE(toks[i+3])[4:]):
                            loop=1
                        else:
                            loop=0
                            i+=n_toks_loop
                    except:
                        print("Sintaks Error : Penulisan variabel tidak benar pada argumen \"ULANG\"")
                        exit()
                elif toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3]=="NUM LEBIH VAR":
                    try:
                        if int(toks[i+1][4:]) > int(getVARIABLE(toks[i+3])[4:]):
                            loop=1
                        else:
                            loop=0
                            i+=n_toks_loop
                    except:
                        print("Sintaks Error : Penulisan variabel tidak benar pada argumen \"ULANG\"")
                        exit()
                elif toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3]=="NUM LEBIHSAMA VAR":
                    try:
                        if int(toks[i+1][4:]) >= int(getVARIABLE(toks[i+3])[4:]):
                            loop=1
                        else:
                            loop=0
                            i+=n_toks_loop
                    except:
                        print("Sintaks Error : Penulisan variabel tidak benar pada argumen \"ULANG\"")
                        exit()
                elif toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3]=="VAR LEBIH NUM":
                    try:
                        if int(getVARIABLE(toks[i+1])[4:]) > int(toks[i+3][4:]):
                            loop=1
                        else:
                            loop=0
                            i+=n_toks_loop
                    except:
                        print("Sintaks Error : Penulisan variabel tidak benar pada argumen \"ULANG\"")
                        exit()
                elif toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3]=="VAR LEBIHSAMA NUM":
                    try:
                        if int(getVARIABLE(toks[i+1])[4:]) >= int(toks[i+3][4:]):
                            loop=1
                        else:
                            loop=0
                            i+=n_toks_loop
                    except:
                        print("Sintaks Error : Penulisan variabel tidak benar pada argumen \"ULANG\"")
                        exit()
                elif toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3]=="VAR KURANG NUM":
                    try:
                        if int(getVARIABLE(toks[i+1])[4:]) < int(toks[i+3][4:]):
                            loop=1
                        else:
                            loop=0
                            i+=n_toks_loop
                    except:
                        print("Sintaks Error : Penulisan variabel tidak benar pada argumen \"ULANG\"")
                        exit()
                elif toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3]=="VAR KURANGSAMA NUM":
                    try:
                        if int(getVARIABLE(toks[i+1])[4:]) <= int(toks[i+3][4:]):
                            loop=1
                        else:
                            loop=0
                            i+=n_toks_loop
                    except:
                        print("Sintaks Error : Penulisan variabel tidak benar pada argumen \"ULANG\"")
                        exit()
                i+=5

def jalan():
    data = open_file(argv[1])
    toks = lex(data)
    parse(toks)

jalan()
