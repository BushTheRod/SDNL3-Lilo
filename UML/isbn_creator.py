from random import randint

def generer_isbn() : 
    chiffres = [9, 7, 8, 2, ]

    chiffres = [9, 7, 8, 2, ]

    for i in range(8) :
        chiffres.append(randint(0, 9))

    somme = 0
    for i in range (len(chiffres)) :
        if i % 2 == 0:
            somme += chiffres[i]
        else:
            somme += chiffres[i] * 3

    chiffres.append(somme % 10)

    isbn_créé = f"{chiffres[0]}{chiffres[1]}{chiffres[2]}-{chiffres[3]}-"
    nombre_de_chiffres_dans_editeur = randint(2, 5)
    for i in range(nombre_de_chiffres_dans_editeur) :
        isbn_créé += str(chiffres[4 + i])
    isbn_créé += "-"
    for i in range(8 - nombre_de_chiffres_dans_editeur) :
        isbn_créé += str(chiffres[4 + nombre_de_chiffres_dans_editeur + i])
    isbn_créé += f"-{chiffres[12]}"

    return isbn_créé

print(generer_isbn())
    


