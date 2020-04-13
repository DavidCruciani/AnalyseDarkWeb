# AnalyseDarkWeb

Implémentation d'une méthodologie et d'un logiciel pour surveiller et avoir un aperçu rapide d'un site, ou d'un ensemble de sites, du dark web.

Prérequis :
- Python3 ;
- torsocks : `sudo apt-get install torsocks` ;
- Scikit-learn ; `sudo apt-get install python3-sklearn` ;
- MySQL ; `sudo apt-get install python3-mysql.connector` ;

Important :
- renseigner les bons chemins dans le fichier  `allVariables.py ` ;

### AllVariables.py
Ce fichier permet de spécifier des chemins d'accès, ainsi que les informations pour se connecter à la base. Plusieurs de c'est champ vont être temporaire mais peuvent être gardé en enlevant les 2 dernières lignes du fichier `aspireSite.py`

### Extraire des urls de la base de données pour les analyser :
Lancer  `python3 BDDextractLinks.py nombreUrl`. Un fichier temporaire sera créé dans le dossier choisi a cet effet il stockera les urls récupérées de la base de données le temps de les traiter. Il est possible de remplir le fichier, temporairement créé, à la main mais cette action est deconseillée car les urls récupérées dans la base de données sont marqué pour que personne d'autre ne traite la meme url. L'url ayant l'identifant le plus petit et qui n'a pas déjà était sélectionnée ou analysée est alors ajouté au fichier.

### Enrichir la base de données de classification :
Dans `/wordClassification/enrichirDB.py`, renseigner la variable `field` avec le mot pour lequel un réseau de mots associés est souhaité pour enrichir la base de données. Tout en bas, `addWord(it['item'],"Categorie")`, remplacer `Categorie` par la catégorie souhaitée (parmi uniquement celles-ci : Drug, Money, Market, Adult, Virus, Crime). Attention à respecter la casse comme présenté ici pour les différentes catégories. Ainsi, on ajoute les mots associés à `field` dans la catégorié mentionnée. La base de classification est accessible au format json dans `categories.json`.

### Ordre des scripts à lancer
- `python3 aspireSite.py` ;

La base de données va alors être rempli et va permettre au moteur de recherche darkoogle de fonctionner
