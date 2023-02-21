def contar_vocales(cad: str )-> tuple:

    #pre: recibo una cadena y debo contabilizar las vocales 
    #post: devuleve una tupla con toda la cant de vocales ya sea con mayuscula, min y dieresis 
    tup= [0,0,0,0,0]

    for i in range(len(cad)):
        if "a"== cad[i] or "á"== cad[i] :
            tup[0]+=1
        elif "e"== cad[i]  or "é"== cad[i]:
            tup[1]+=1
        elif "i"== cad[i] or "í"== cad[i]:
            tup[2]+=1
        elif "o"== cad[i] or  "ó"== cad[i]:
            tup[3]+=1
        elif "u"== cad[i] or "ú"== cad[i] or "ü"== cad[i]:
            tup[4]+=1
    return tuple(tup)

print(contar_vocales("El cuervo es un pájaro de mal agüero"))