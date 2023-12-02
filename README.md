# RiftBrawl

RiftBrawl est un jeu de combat compétitif où deux joueurs s'affrontent dans un combat sans fin. En utilisant des capacités uniques à chaque personnage, chaque joueur tente de vaincre son adversaire.

## Installation

Pour installer le jeu RiftBrawl, vous aurez besoin de Python 3.7 ou plus. Voici les étapes d'installation :
1. Clonez ce répertoire à l'aide de git :
```
git clone https://github.com/RiftBrawl/RiftBrawl.git
```
```
cd RiftBrawl
```
2. Vous pouvez lancer le jeu directement en exécutant le fichier ```run.py``` qui se chargera d'installer les dépendances :
```
python run.py
``` 
Si l'installation des dépendances ne fonctionne pas, installez les dépendances nécessaires à partir du fichier ```requirements.txt``` à l'aide de pip :
```
pip install -r requirements.txt
```
Les dépendances nécessaires sont :
* pygame>=1.9
* numpy>=1.17

## Commandes de jeu 

Les commandes par défaut pour le jeu sont les suivantes :

### Jouer 1 :

- Déplacer à droite : D
- Déplacer à gauche : Q
- Saut : Espace
- Déplacer vers le bas : S
- Action principale : F
- Action secondaire : G
- Déplacer vers le haut : Z

### Jouer 2 :

- Déplacer à droite : Flèche Droite
- Déplacer à gauche : Flèche Gauche
- Saut : Flèche Haute
- Déplacer vers le bas : Flèche Bas
- Action principale : L
- Action secondaire : M

## Fonctionnalités

RiftBrawl offre une variété de fonctionnalités pour améliorer l'expérience de jeu :
- Choix de personnage : Chaque joueur peut choisir parmi une variété de personnages uniques, chacun ayant ses propres capacités et styles de combat.
- Écran scindé : Le jeu offre un mode écran scindé, permettant à chaque joueur de se concentrer sur sa propre partie de l'écran.
- Effet parallaxe : Pour améliorer l'expérience visuelle, le jeu utilise un effet de parallaxe pour donner une sens de profondeur au monde du jeu.
- Système de vie : Chaque joueur a une certaine quantité de vie. Lorsqu'un joueur subit des dégâts, sa vie diminue. Lorsque la vie d'un joueur atteint zéro, il est vaincu.

## Autres informations 

Ce jeu est encore en cours de développement, certaines fonctionnalités peuvent ne pas être encore complètement implémentées.

Jouez et amusez-vous bien !