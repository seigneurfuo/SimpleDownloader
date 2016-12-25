# coding: utf8
# !/bin/usr/python

# Modification récente: 24 décembre 2016

import urllib, urllib2, re, wget, os, sys, json

# Préparation du projet
os.chdir("data")
url = sys.argv[1]
projectName = url.replace("/", "_").replace(":", "_")

if os.path.exists(projectName):
    print "Le dossier existe déja"
    exit

else:
    os.makedirs(projectName)
    os.chdir(projectName)

    # Line.me
    if "line.me" in url:
        # Ouverture de l'url passée en argument
        html = urllib2.urlopen(url).read()
        
        # Création d'une règle de recherche regex pour liste les urls des images
        images = re.findall('url\(([^)]+)\)', html)

        # Pour chaque image dans la liste des images trouvées
        for id_, image in enumerate(images):
            # Affichage du fichier en cours de téléchargement
            print "\n", id_ + 1, "/", len(images)
            
            # Téléchargement
            wget.download(image)
            
    elif "danbooru.donmai.us/pools" in url:
        # Utilisation de l'api de danbooru pour le téléchragement des images d'un pool
        
        # Découpage de l'adresse source
        splitedUrl = url.split("/")
        
        # Récupère la l'identifiant du pool dans l'emplacement 4 du tableau
        poolId = splitedUrl[4]

        # Url de base pour l'api des pools danbooru
        poolBaseUrl = "http://danbooru.donmai.us/pools/%s.json" %poolId
        
        # Récupération des informations sur le post
        poolApiResult = urllib2.urlopen(poolBaseUrl).read()
        
        # Convertion de la réponse en objet JSON
        poolApiJsonResult = json.loads(poolApiResult)
        
        # Liste des images du pool (ex: 100 200 300)
        poolPosts = poolApiJsonResult["post_ids"]
        
        # Convertion en une liste Python
        postList = poolPosts.split(" ")
        
        # Pour chaque post dans la liste
        for id_, postId in enumerate(postList):
            # Url de base pour l'api des posts dannbooru
            postBaseUrl = "http://danbooru.donmai.us/posts/%s.json" %postId
            
            # Récupération des informations sur le post
            postApiResult = urllib2.urlopen(postBaseUrl).read()
            
            # Convertion de la réponse en objet JSON
            postApiJsonResult = json.loads(postApiResult)
            
            #Récupération de l'url de l'image du post
            pictureUrl = postApiJsonResult["large_file_url"]
            
            # Génération de l'adresse de téléchargement
            downloadUrl = "http://danbooru.donmai.us/%s" %pictureUrl
            
            # Affichage du fichier en cours de téléchargement
            print "\n", id_ + 1, "/", len(postList)
            
            # Téléchargement
            wget.download(downloadUrl)
            
    os.chdir("./../")
