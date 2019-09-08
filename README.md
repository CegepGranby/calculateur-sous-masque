# Calculateur de sous-masque réseau
**IMPORTANT**: Pour cet exercice, assurez-vous d'avoir **Python** d'installé.

## La tâche à faire
Vous devrez refaire une implémentation d'*ipcalc*. **Tout ce qui est affichage, manipulation et conversion des nombres binaires a déjà été fait pour vous**. Pour les plus curieux d'entre vous, vous pouvez jeter un coup d'oeil au fichier `ip_utils.py` j'ai mis une **tonne** de commentaire pour expliquer comment j'ai fait.

Voici ce que vous allez devoir recréer :

![ipcalc](https://github.com/CegepGranby/calculateur-sous-masque/blob/master/enonce/screenshot.png?raw=true)

Voici ma solution :

![ipcalc version Python](https://github.com/CegepGranby/calculateur-sous-masque/blob/master/enonce/solution.png?raw=true)

Pour vous donner une idée, mon implémentation (sans compter l'affichage) est d'environ 10 lignes de code.

## Comment faire
Vous devez tout d'abbord créer un fichier à la racine du projet appelé **exactement** : `solution.py`. Ensuite vous devrez créer une fonction appelée `ipcalc` prenant en paramètre une adresse ip. Voici à quoi elle devrait ressembler :

```python
def ipcalc(addr):
	# Le masque sous-réseau est déjà généré pour vous
	mask = addr.mask
	# Votre définition
```
Cette fonction sera appelée automatiquement lorsque vous faite :
```
$ python ipcalc.py
```
Cette commande partira le programme et demandera d'entrer une adresse IP CIDR. Si vous voulez éviter de la rentrer à chaque fois, faites :
```
$ python ipcalc.py -a ADRESSE_IP
```
Pour la passer en paramètre.

## Correcteur automatique
Le programme vient avec un correcteur automatique, pour l'appeler simplement faire :
```
$ python ipcalc.py -c
```

Par contre votre fonction `ipcalc` devra retourner un objet de type `IPAddress`. Voici comment faire :

```python

def ipcalc(addr):
	# ...
	addr.wildcard = wildcard
	addr.network = network
	addr.broadcast = broadcast
	addr.host_min = host_min
	addr.host_max = host_max
	addr.hosts = hosts
	return addr
```

## Notion pour le binaire
### Le "et" logique
Symbole Pythonien : `&`

| AND    | 0 | 1 |
|--------|---|---|
| **0**  | 0 | 0 |
| **1**  | 0 | 1 |


### Le "ou" logique
Symbole Pythonien : `|`

| OR     | 0 | 1 |
|--------|---|---|
| **0**  | 0 | 1 |
| **1**  | 1 | 1 |

### Le "ou" exclusif
Symbole Pythonien : `^`

| XOR    | 0 | 1 |
|--------|---|---|
| **0**  | 0 | 1 |
| **1**  | 1 | 0 |


### La négation binaire
Symbole Pythonien : `~`

| NOT    |   |
|--------|---|
| **0**  | 1 |
| **1**  | 0 |

### Le décalage de bit
Symboles Pythonien : `<<` et `>>`

Cet opérateur est surtout utilisé dans la partie que j'ai codé, vous n'aurez pas besoin de l'utiliser. Voici tout de même son fonctionnement en Python
```python
# Décalage à gauche
#          0001 => 1
1 << 1 # = 0010 => 2
1 << 2 # = 0100 => 4

# Décalage à droite
4 >> 1 # = 0010 => 2
4 >> 2 # = 0001 => 1
4 >> 3 # = 0000 => 0
```

**Note** : Sachez qu'une adresse IP est en fait un entier de 32 bits. Donc vous pouvez sans aucun problème faire l'addition ou la soustraction de deux adresses ou même avec un autre entier. (Je dis ça comme ça :wink:)