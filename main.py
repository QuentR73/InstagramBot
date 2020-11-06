from selenium import webdriver
from time import sleep


def initialisation():                                                                   #PERMET DE DEMARRER UNE PAGE CHROME POUR POUVOIR INTERAGIR AVEC
    monNavigateur = webdriver.Chrome(executable_path="C:\chromedriver.exe")                                 #Chemin du Driver Chrome
    monNavigateur.get("http://www.instagram.fr/accounts/login/")                                            #L'URL de connexion à Instagram
    sleep(3)                                                                                                #On fait une tempo pour laisser le temps à Chrome de s'ouvrir
    return monNavigateur                                                                                    #On retourne notre navigateur chrome avec la fenetre

def connexion(monBot, nomUtilisateur, motDePasseUtilisateur):                           #PERMET DE SE CONNECTER A INSTAGRAM AVEC UN NOM D'UTILISATEUR ET UN MOT DE PASSE
    monBtnActiveNotif = monBot.find_element_by_xpath("//*[text()='Accepter']")                              #On cherche le bouton qui contient le texte Accepter / Permet d'accepter les cookies
    monBtnActiveNotif.click()                                                                               #On click sur le boutton précédement trouvé
    sleep(1)

    champNomUtilisateur = monBot.find_element_by_name('username')                                           #On trouve l'input ou il faut rentrer le nom d'utilisateur pour la connexion
    champMotDePasse = monBot.find_element_by_name('password')                                               #On trouve l'input du mot de passe pour la connexion

    champNomUtilisateur.send_keys(nomUtilisateur)                                                           #On rempli le champs du nom d'utilisateur avec notre identifiant
    champMotDePasse.send_keys(motDePasseUtilisateur)                                                        #Le mot de passe qui correspond au nom d'utilisateur

    monBtnConnexion = monBot.find_element_by_xpath("//*[text()='Connexion']")                               #On sélectionne le boutton qui permet de lancer la connexion
    monBtnConnexion.click()                                                                                 #On active ce boutton
    sleep(3)                                                                                                #On fait une tempo pour laisser le temps d'afficher la page

    monBtnEnregistrerIdentifiant = monBot.find_element_by_xpath("//*[text()='Enregistrer les identifiants']")   #On trouve le boutton pour enregistrer les identifiants
    monBtnEnregistrerIdentifiant.click()                                                                        #On active le boutton
    sleep(3)                                                                                                    #Nouvelle tempo

    monBtnActiveNotif = monBot.find_element_by_xpath("//*[text()='Activer']")                               #On trouve le boutton pour activer les notifications
    monBtnActiveNotif.click()                                                                               #On active le boutton
    sleep(2)                                                                                                #Tempo


def gagnerFollowers(monBot, nomUtilisateur, motDePasseUtilisateur, monHashtag):         #Permet de gagner des followers en suivant des gens en espérant un follow back

    connexion(monBot, nomUtilisateur, motDePasseUtilisateur)                                                #On se connecte à un page web

    monBot.get("http://instagram.com/explore/tags/" + monHashtag)                                           #On ouvre la page du hastag

    mesPublicationsASabonner = []                                                                           #Variable qui contiendra tous les liens des gens auxquels on va s'abonner

    nombreDeScroll = 2
    while nombreDeScroll > 0:
        monBot.execute_script("window.scrollTo(0, document.body.scrollHeight);")                            #On scroll down sur la page pour afficher plus de resultat
        sleep(2)                                                                                            #On marque une tempo pour laisser le temps d'affichage

        liens = monBot.find_elements_by_tag_name('a')                                                       #On recherche tous tag A
        for lien in liens:                                                                                  #Pour tags trouvés
            href = lien.get_attribute("href")                                                               #On isole les liens
            if "/p/" in href:                                                                               #On selectionne que les liens vers des publications: Il contient "/p/"
                mesPublicationsASabonner.append(href)                                                       #On ajoute le liens de la publication a la liste
                print(href + " : L'utilisateur va etre suivi")

        nombreDeScroll = nombreDeScroll - 1                                                                 #On scroll sur la page

    for profil in mesPublicationsASabonner:                                                                 #Pour chaque lien vers un publication
        monBot.get(profil)                                                                                  #On ouvre le liens de la publication
        sleep(1)                                                                                            #Tempo

        monBot.find_element_by_xpath('//button[text()="S’abonner"]').click()                                #On click sur le boutton pour s'abonner
        monBot.find_element_by_xpath("//span[@class='fr66n']").click()                                      #On clikc sur le boutton J'aime

        monFichier = open("mesAbonnements.txt", "a")                                                        #On ouvre le fichier texte qui contient tous les publications ou on s'est abonnés
        monFichier.write(profil + "\n")                                                                     #On ecrit dans le fichier le lien de la publication
        monFichier.close()                                                                                  #Fermeture du fichier
        sleep(2)


def seDesabonner(monBot, nomUtilisateur, motDePasseUtilisateur):                        #PERMET DE SE DESABONNER DES UTILISATEURS AUXQUELS ON S'EST ABONNER
    connexion(monBot, nomUtilisateur, motDePasseUtilisateur)                                                #On se connecte à instagram
    monFichierAbonnements = open("mesAbonnements.txt", "r")                                                 #On ouvre le fichier qui contient le liens des abonnement précédents
    lignes = monFichierAbonnements.readlines()                                                              #On lit le fichier ligne par ligne et on l'ajoute à la list
    monFichierAbonnements.close()

    for ligne in lignes:                                                                                    #Pour chaque ligne
        monBot.get(ligne)                                                                                   #On ouvre la publication
        sleep(2)                                                                                            #Tempo
        monBot.find_element_by_xpath('//button[text()="Abonné(e)"]').click()                                #On clique sur le boutton pour se désabonner
        sleep(1)
        monBot.find_element_by_xpath('//button[text()="Se désabonner"]').click()                            #On clique sur le boutton pour confirmer
        sleep(1)

    monFichierAbonnement = open("mesAbonnements.txt", "w")                                                  #On ouvre le fichier
    monFichierAbonnement.write("")                                                                          #On efface tout
    monFichierAbonnement.close()                                                                            #On ferme le fichier

def commenterPublication(monBot, nomUtilisateur, motDePasseUtilisateur, monHashtag, commentaire):   #PERMET DE COMMENTER UNE PUBLICATION QUI EST CIBLEE GRACE A UN HASHTAG

    connexion(monBot, nomUtilisateur, motDePasseUtilisateur)                                                #On se connecte à un page web

    monBot.get("http://instagram.com/explore/tags/" + monHashtag)                                           #On ouvre la page du hastag
    sleep(2)

    mesPublicationsACommenter = []                                                                          #Notre liste des publications que nous allons commenter

    nombreDeScroll = 2                                                                                      #Notre de scroll down : Plus elevé = plus de publications
    while nombreDeScroll > 0:
        monBot.execute_script("window.scrollTo(0, document.body.scrollHeight);")                            #On scroll pour afficher plus de publication
        sleep(1)

        liens = monBot.find_elements_by_tag_name('a')                                                       #On trouve les elements qui ont le tag 'a'
        for lien in liens:                                                                                  #Pour chaque liens de la liste
            href = lien.get_attribute("href")                                                               #On recupere le lien url
            if "/p/" in href:                                                                               #Si le lien contient '/p/' on sait que c'est un publication. Sinon ca veut etre n'importe quel autre lien
                mesPublicationsACommenter.append(href)                                                      #On ajouter à la liste des publications à commenter
                print(href + " : La publication va etre commentée")                                         #On affiche à l'utilisateur
        nombreDeScroll = nombreDeScroll - 1                                                                 #On baise le scroll

    for maPublication in mesPublicationsACommenter:                                                         #Pour chaque publication retenues
        monBot.get(maPublication)                                                                           #On ouvre la page de la publication
        sleep(1)                                                                                            #Tempo pour laisser le temps à l'affichage
        monCommentaire = monBot.find_element_by_class_name("Ypffh")                                         #On trouve l'élément pour laisser le commentaire
        monCommentaire.click()                                                                              #On clique desus pour l'activé / Il est désactivé par défaut
        monCommentaire = monBot.find_element_by_class_name("Ypffh")                                         #On reselectionne notre zone de texte du commentaire

        monCommentaire.send_keys(commentaire)                                                               #On ajoute le commentaire
        monBot.find_element_by_xpath('//button[text()="Publier"]').click()                                  #On publie le commentaire
        monBot.find_element_by_xpath("//span[@class='fr66n']").click()                                      #On clique sur le bouton j'aime pour donner un peu de crédit à notre commentaire ;)
        sleep(1)

def main():         #LE MAIN DU PROGRAMME

    a = True                                                                                                #Variable pour connaitre l'action que veut effectuer l'utilisateur
    while a:
        print(".----------------------------------------------------------------------------------.")       #Pour la beauté du geste
        print("|                      Author : Quentin RUFFIER DES AIMES                          |")
        print("|                                Version 1.0                                       |")
        print("|                          https://github.com/QuentR73                             |")
        print("|                                Follow for fun !!                                 |")
        print("'----------------------------------------------------------------------------------'")       #Fin de la beauté du geste
        print("1/ Informations\n2/ Suivre des gens par Hastag (+like)\n3/ Se désabonner depuis la dernière fois\n4/ Pour commenter une publication possédant un hashtag\nQ/ Pour quitter")
        print("------------------------------------------------------------------------------------")

        x = input("Entre ton choix : ")                                                                     #On affiche les différents choix qu'à l'utilisateur
        print("------------------------------------------------------------------------------------")
        if x == "1":                                                                                        #Si l'utilisateur choisi le cas 1
            print("Informations :")
        elif x == "2":                                                                                      #Si l'utilisateur choisi le cas 2
            nomUtilisateur = input("Ton nom d'utilisateur pour la connexion : ")                            #On demande le nom d'utilisateur utile à la connexion
            motDePasseUtilisateur = input("Ton mot de passe pour la connexion : ")                          #On demande le mot de passe de l'utilisateur pour la connexion au site
            monHashtag = input("Hashtag correspond au profil que l'ont veut suivre (1 mot sans le #) : ")   #On demande à l'utilisateur d'entrée un hastag pour cibler les profils

            monBot = initialisation()                                                                       #On lance une nouvelle initialisation (pour ouvrir une nouvelle page)
            gagnerFollowers(monBot, nomUtilisateur, motDePasseUtilisateur, monHashtag)                      #On appelle la fonction qui va permettre de suivre des gens en masse
        elif x == "3":                                                                                      #Si l'utilisateur choisi le cas 3
            nomUtilisateur = input("Ton nom d'utilisateur pour la connexion : ")                            #On demande le nom d'utilisateur utile à la connexion
            motDePasseUtilisateur = input("Ton mot de passe pour la connexion : ")                          #On demande le mot de passe de l'utilisateur pour la connexion au site
            monBot = initialisation()                                                                       #On lance une nouvelle initialisation (pour ouvrir une nouvelle page)
            seDesabonner(monBot, nomUtilisateur, motDePasseUtilisateur)                                     #Appel de la méthode pour se désabonner
        elif x == "4":                                                                                      #Si l'utilisateur veut lancer le bot pour commenter des publications
            nomUtilisateur = input("Ton nom d'utilisateur pour la connexion : ")                            #On demande le nom d'utilisateur utile à la connexion
            motDePasseUtilisateur = input("Ton mot de passe pour la connexion : ")                          #On demande le mot de passe de l'utilisateur pour la connexion au site
            monHashtag = input("Commenter des publications qui possède le hashtag : (1 mot sans le #) : ")  #On demande à l'utilisateur d'entrée un hastag pour cibler les publications
            commentaireAPoster = input("Le commentaire à poster : ")                                        #On demande à l'utilisateur le commentaire qu'il veut poster

            monBot = initialisation()                                                                           #Nouvelle initialisation du BOT
            commenterPublication(monBot, nomUtilisateur, motDePasseUtilisateur, monHashtag, commentaireAPoster) #Appel de la fonction pour poster des commentaire


        elif x == "Q":                                                      #Si l'utilisateur choisi de quitter
            a = False                                                       #Fin du While / Fin du programme
        elif x == "q":                                                      #Si l'utilisateur choisi de quitter
            a = False                                                       #Fin du While / Fin du programme
main()


