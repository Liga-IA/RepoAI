# Melting Point Prediction (Kaggle Competition)

This repository contains a machine learning solution developed for the **Melting Point Prediction** competition on **Kaggle**.  
The objective of the competition is to predict the melting point (**Tm**) of chemical compounds based on their molecular structure and associated descriptor features.
Link: <https://www.kaggle.com/competitions/melting-point>
---

## Problem Overview

Melting point is an important physicochemical property related to molecular structure and thermal stability.  
In this competition, molecules are provided as **SMILES strings**, along with additional categorical descriptor features. The task is to build a regression model capable of predicting the melting point for unseen compounds.

---

## Methodology

### Feature Engineering
- **RDKit** is used as a cheminformatics toolkit to process molecular structures.
- Molecular representations include:
  - **Morgan fingerprints** (radius 2 and 3),
  - **MACCS keys**,
  - **Physicochemical descriptors** (e.g., molecular weight, polarity, hydrogen bond counts).
- These features are concatenated with the original `Group*` descriptors to form the final input matrix.

### Models Evaluated
- Decision Tree Regressor  
- Random Forest Regressor  
- XGBoost Regressor  

Tree-based models consistently outperformed simpler approaches, with **XGBoost** providing the best overall performance.

### Model Selection & Validation
- Train/test split and **K-fold cross-validation** were used for evaluation.
- **Early stopping** was applied to select a robust number of estimators.
- The final configuration was chosen based on median performance across folds to reduce overfitting.

---

## Results

- Final model: **XGBoost Regressor**
- Evaluation metric: **RMSE**
- Performance reached a plateau around RMSE ≈ **44**, consistent across multiple models and validation strategies.

The asymmetric distribution of melting points and the presence of high-value compounds contribute to the difficulty of further reducing the error.

---

## Notes

- A simple feed-forward neural network was also tested but underperformed compared to tree-based models on this structured dataset.
- The focus of this project is on **feature engineering, model comparison, and validation**, rather than achieving top Kaggle leaderboard rankings.
