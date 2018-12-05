# TP Panda Basket

## Prérequis
- Python 2.7
- Panda3d 1.9.4
- tensorflow 1.12.0

## Creation d'un jeu de donnée:
#### Instructions
Lancez la commande `python main_apprentissage.py` (laissez tourner pendant 10 minutes minimum)

#### Paramètre de la classe App:
```python
App(chemin_fichier='train_data.csv')
```

## Conversion d'un jeu de donnée en modele pour tensorflow:
#### Instruction
Lancez la commande `python main_conversion.py`

#### Paramètre de la fonction conversion:
```python
conversion(chemin_donnee='train_data.csv', chemin_modele='tf_model.h5')
```

## Lancement de la prediction depuis le jeu de donnée:
#### Instruction
Lancez la commande `python main_prediction_donnee.py`

#### Paramètre de la classe App:
```python
App(chemin_fichier='train_data.csv')
```

## Lancement de la prediction depuis le modele:
#### Instruction
Lancez la commande `python main_prediction_modele.py`

#### Paramètre de la classe App:
```python
App(chemin_fichier='tf_model.h5')
```
