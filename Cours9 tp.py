from random import randint

#Crée une séquence de 4 chiffres, allant de 1 à 6

def initCache(nbColors=6,nbPawns=4):

    return [randint(1,nbColors) for i in range(nbPawns)]

#Joueur entre une proposition, répète tant que la proposition est impossible.

def choose(nbColors=6,nbPawns=4):

    nocorrect = True

    while nocorrect:

        nocorrect = False

        selected = input('Input your proposal: ')

        if len(selected) == nbPawns:            #Vérification, a-t-on entré le bon nombre de chiffres?

            selected = [int(x) for x in list(selected)]

            for x in selected:

                if (x < 1) or (x > nbColors):   #Vérification, y a-t-il des valeurs interdites?

                    nocorrect = True

        else:

            nocorrect = True

    return selected

#Comparaison proposition à réponse

def evaluation(selected,cache): #Selected = valeur entrée par le joueur, cache = réponse à trouver

    WellPut = 0

    Misplaced = 0

    copySelected,copyCache = list(selected),list(cache) #Copie des listes pour pouvoir les modifier sans casser les boucles basées sur ces listes.

    for i in range(len(cache)):

        if copySelected[i] == copyCache[i]:

            WellPut += 1    #Si même valeur, dire qu'une est bien placée

            copySelected[i],copyCache[i] = -1,-1

    for i in range(len(cache)):

        for j in range(len(cache)): #Double for pour pouvoir parcourir toute la liste à chaque tour

            if (copySelected[i] == copyCache[j]) and (copySelected[i] != -1):   #Scanne la liste pour voir si il n'y a pas un chiffre correct mais mal placé. Est ignoré si on a pas déjà well put.

                Misplaced += 1  

                copySelected[i],copyCache[j] = -1,-1

    return WellPut,Misplaced

#Affiche les bons chiffres bien placés, et les bons chiffres mal placés

def display(well,bad):

    print(well,"well spot and",bad,"bad ",'\n')


#Affiche la réponse

def displayCache(cache):

    for x in cache:

        print(x,end='')

#Définition manuelle des paramètres du jeu, longueur de la chaîne à deviner, nombre de "couleurs" à deviner

def gameParameters():
    nbC = int(input('Input the number of colors: '))
    nbP = int(input(' Enter the length of the sequence to guess: '))
    nbTry = int(input(' Enter the number of trials: '))
    return nbC,nbP,nbTry
 
#Jeu joué manuellement

def master():
    nbC,nbP,nbTry = gameParameters()    #Initialisation jeu
    cache = initCache(nbC,nbP)          #Initialisation réponse
    notFound = True                     #Réponse pas trouvée
    tries = 1
    print() #Espace les print
    while notFound and (tries<=nbTry):  #Tant qu'on a pas trouvé et qu'on a pas dépassé le nombre d'essais
        print('try',tries)
        well,bad = evaluation(choose(nbC, nbP), cache)  #Vérification de notre réponse
        display(well,bad)
        if well == nbP: #Condition de réussite du jeu
            notFound = False
        else:
            tries += 1
    if tries == nbTry+1:
        print("lost, we had to find:",end=' ')
        displayCache(cache)
    else:
        print("Congratulations, you have found well:", end=' ')
        displayCache(cache)
 
#Algorithme de résolution automatique 1

def chooseGame(S,possibles,results,tries):
    if tries == 1:
        return [1,1,2,2]
    elif len(S) == 1: 
        return S.pop()
    else:
        return max(possibles, key=lambda x: min(sum(1 for p in S if evaluation(p,x) != res) for res in results))
 
#Algorithme de résolution automatique 2

def chooseGameBis(S,possibles,results,tries):
    if tries == 1:
        return [1,1,2,2]
    elif len(S)==1:
        return S.pop()
    else:
        Max = 0
        for x in possibles:
            Min = 1297
            for res in results:
                nb = 0
                for p in S:
                    if evaluation(p,x) != res:
                        nb+=1
                if nb<Min:
                    Min=nb
            if Max<Min:
                Max = Min
                xx = x
        return xx
                
#Jeu joué automatiquement

def game():
    nbC,nbP = 6,4
    cache = initCache(nbC,nbP)
    notFound = True
    tries = 1
    S = set((x,y,z,t) for x in range(1,7) for y in range(1,7) for z in range (1,7) for t in range(1,7))
    possibles = frozenset(S)
    results = frozenset((well,bad) for well in range(5) for bad in range(5-well) if not (well == 3 and bad == 1))
    while notFound and (tries<=10):
        print('try',tries)
        selected = chooseGameBis(S,possibles,results,tries)
        print('computer proposal: ',end='')
        displayCache(selected)
        print()
        well,bad = evaluation(selected,cache)
        display(well,bad)
        if well == nbP:
            notFound = False
        else:
            tries += 1
            S.difference_update(set(coup for coup in S if (well,bad) != evaluation(coup,selected)))
    if tries == 11:
        print("lost, we had to find:",end=' ')
        displayCache(cache)
    else:
        print("He is strong, he found", end=' ')
        displayCache(cache)
               
#Jeu lancé

def init():
    pasChoisi=True
    while pasChoisi==True:
        choix = int(input("Lancez le jeu : Automatiquement(0), Manuellement(1)"))
        if choix == 0 or choix == 1:
            pasChoisi = False
    if choix == 0:
        game()
    else:
        master()

init()