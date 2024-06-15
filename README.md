# Test technique Python pour AI Engineer

## Contexte

Lors de ce test, il s'agit de réaliser un script Python pour évaluer la performance d'un modèle de catégorisation de transactions bancaires.
La tache du modèle est de prédire le compte comptable d'une transaction bancaire, ce compte comptable étant un numéro à 6 chiffres.

## Format des données fournies

Le fichier de données ci-joint contient les résultats de l'application d'un modèle sur un dataset de test. Le fichier contient un document JSON par ligne, avec les champs suivants:
- id_transaction: un identifiant unique de transaction bancaire
- true_category: le bon compte comptable à prédire.
- predictions: les prédictions du modèle, sous forme d'un dictionnaire avec pour clé un compte comptable et pour valeur la probabilité de ce compte estimée par le modèle.

## Métrique d'évaluation

Lors de l'exploitation du modèle, nous préférons que le système ne categorise pas plutôt que de faire une erreur. Il sera donc nécessaire de déterminer un seuil de prédiction en-dessous duquel on ne tiendra pas compte de la prédiction du modèle.

Pour résumer, le système d'évaluation fonctionnera de la manière suivante:
1/ Le modèle prédit un compte comptable avec une probabilité P
2/ Si P < Seuil alors on ne prédit aucun compte comptable (NoPred)
3/ Si P >= Seuil alors:
  - Si le compte prédit est le bon compte, on considère qu'on a une bonne prédiction (GoodGuess)
  - Si le compte prédit n'est pas le bon compte, on a une mauvaise prédiction (BadGuess)

Afin de modéliser l'aversion à l'erreur, on adopte comme métrique d'évalution:
PenalizedGoodGuessRate = (GoodGuess - 5 * BadGuess) / (NoPred + GoodGuess + BadGuess)


## Objectif du test

Ecrire un script Python qui prends comme paramètres:
- dataset [REQUIRED]: le chemin vers le fichier de donnée
- threshold [OPTIONAL]: une valeur de seuil

Si le script est appelé avec un paramètre threshold, alors il doit calculer la PenalizedGoodGuessRate pour cette valeur de seuil.
Si le script est appelé sans paramètre threshold, alors il doit déterminer le seuil qui maximise la PenalizedGoodGuessRate.

Nous apporterons une attention particulière à produire un code correct, lisible et réutilisable.
