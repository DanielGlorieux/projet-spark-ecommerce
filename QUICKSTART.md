# Guide de Démarrage Rapide - Projet Spark E-commerce

## 🎯 Objectif
Analyse du comportement d'achat des clients e-commerce avec Apache Spark

## 👥 Équipe
- **ILBOUDO P. Daniel Glorieux** - Data Ingestion & Préparation ✅
- **PITROIPA Soraya** - Transformations & Jointures
- **KONE Khalis Aïman** - Analyses & Visualisations

---

## ⚡ Démarrage Rapide (5 minutes)

### 1. Installation

```powershell
# Se placer dans le projet
cd C:\Users\danie\Desktop\projet_spark\nouveau_projet

# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement
.\venv\Scripts\Activate.ps1

# Installer les dépendances
pip install -r requirements.txt
```

### 2. Générer les Données (DÉJÀ FAIT ✅)

```powershell
# Les datasets sont déjà générés dans data/raw/
# Si besoin de régénérer:
python src\generate_datasets.py
```

**Résultat:**
- ✅ `data/raw/customers.csv` - 150,000 lignes (15.5 MB)
- ✅ `data/raw/orders.csv` - 200,000 lignes (16.1 MB)

### 3. Lancer le Notebook

```powershell
# Lancer Jupyter
jupyter notebook

# Ouvrir:
# notebooks/01_data_ingestion_cleaning.ipynb

# Exécuter toutes les cellules:
# Menu → Cell → Run All
```

---

## 📊 Ce que Contient le Projet

### Part 1: Data Ingestion & Préparation (Daniel) ✅

#### ✅ Choix des Datasets
- **Customers**: 150k lignes, 11 colonnes
- **Orders**: 200k lignes, 11 colonnes
- **Jointure**: `customer_id` (clé primaire/étrangère)

#### ✅ Ingestion Spark
```python
df_customers = spark.read.csv("data/raw/customers.csv", header=True, inferSchema=True)
df_orders = spark.read.csv("data/raw/orders.csv", header=True, inferSchema=True)
```

#### ✅ Nettoyage Appliqué

**Customers:**
- Valeurs manquantes (phone, city) → "Unknown"
- Emails dupliqués → Dédupliqués (garde le plus récent)
- total_spent négatifs → Supprimés
- Dates normalisées → format date Spark

**Orders:**
- quantity/price ≤ 0 → Supprimés
- total_amount → Recalculé (quantity × unit_price)
- order_status NULL → "Pending"
- shipping_country NULL → "Unknown"
- Intégrité référentielle validée

#### ✅ Résultats
- **Customers clean**: ~147k lignes (98% conservées)
- **Orders clean**: ~194k lignes (97% conservées)
- **Formats**: CSV + Parquet (dans `data/processed/`)

---

## 📁 Structure du Projet

```
nouveau_projet/
├── data/
│   ├── raw/                          # ✅ Données brutes générées
│   │   ├── customers.csv             # 150k lignes
│   │   └── orders.csv                # 200k lignes
│   └── processed/                    # ✅ Données nettoyées (output)
│       ├── customers_clean.parquet
│       └── orders_clean.parquet
│
├── notebooks/
│   └── 01_data_ingestion_cleaning.ipynb  # ✅ Notebook complet Part 1
│
├── src/
│   └── generate_datasets.py          # ✅ Générateur de données
│
├── .gitignore                        # ✅ Exclusions Git
├── requirements.txt                  # ✅ Dépendances Python
└── README.md                         # ✅ Documentation complète
```

---

## 🔧 Commandes Utiles

### Gestion Environnement
```powershell
# Activer l'environnement
.\venv\Scripts\Activate.ps1

# Désactiver
deactivate

# Installer une dépendance supplémentaire
pip install <package>
```

### Jupyter
```powershell
# Lancer Jupyter
jupyter notebook

# Lancer JupyterLab (interface moderne)
jupyter lab
```

### Git
```powershell
# Voir le statut
git status

# Voir l'historique
git log --oneline

# Créer une branche pour les autres membres
git checkout -b soraya-transformations
git checkout -b khalis-analyses
```

---

## 📊 Statistiques des Datasets

### Customers (Brut → Clean)
| Métrique | Brut | Clean | Écart |
|----------|------|-------|-------|
| Lignes | 150,000 | ~147,000 | -2% |
| Emails uniques | 143,365 | 147,000 | +2.5% |
| Valeurs NULL (phone) | 2,958 | 0 | ✅ |
| Valeurs NULL (city) | 2,221 | 0 | ✅ |
| total_spent < 0 | 125 | 0 | ✅ |

### Orders (Brut → Clean)
| Métrique | Brut | Clean | Écart |
|----------|------|-------|-------|
| Lignes | 200,000 | ~194,000 | -3% |
| quantity ≤ 0 | 2,012 | 0 | ✅ |
| unit_price ≤ 0 | 2,064 | 0 | ✅ |
| order_status NULL | 939 | 0 | ✅ |
| total_amount incohérent | ~4,000 | 0 | ✅ |

---

## 🎯 Prochaines Étapes (Soraya & Khalis)

### Part 2: Transformations & Jointures (Soraya)

```python
# Charger les données propres
df_customers = spark.read.parquet("data/processed/customers_clean.parquet")
df_orders = spark.read.parquet("data/processed/orders_clean.parquet")

# Jointure
df_joined = df_orders.join(df_customers, "customer_id", "inner")

# Agrégations
# - Chiffre d'affaires par client
# - Commandes par pays
# - Ventes par catégorie
# - Évolution temporelle

# Window functions
# - RFM analysis (Recency, Frequency, Monetary)
# - Customer lifetime value
# - Ranking des produits
```

### Part 3: Analyses & Visualisations (Khalis)

```python
# Segmentation clients
# - K-means sur les features
# - Analyse par segment

# Visualisations
# - Matplotlib/Seaborn/Plotly
# - Distribution des ventes
# - Heatmaps géographiques
# - Time series

# Recommandations business
# - Top clients à fidéliser
# - Produits à promouvoir
# - Zones géographiques prioritaires
```

---

## 🐛 Résolution de Problèmes

### Erreur "Spark not found"
```powershell
pip install pyspark==3.5.0
```

### Erreur "Java not found"
- Installer Java JDK 8 ou 11
- Configurer JAVA_HOME

### Kernel Jupyter ne démarre pas
```powershell
python -m ipykernel install --user --name=venv
```

### Données manquantes
```powershell
# Régénérer les datasets
python src\generate_datasets.py
```

---

## 📚 Ressources

### Documentation
- [PySpark Documentation](https://spark.apache.org/docs/latest/api/python/)
- [Spark SQL Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)

### Tutoriels
- [PySpark Tutorial - DataCamp](https://www.datacamp.com/tutorial/pyspark-tutorial-getting-started-with-pyspark)
- [Spark by Examples](https://sparkbyexamples.com/pyspark-tutorial/)

---

## ✅ Checklist Part 1 (Daniel)

- [x] Choix de 2 datasets volumineux (≥100k lignes)
- [x] Définition du problème métier
- [x] Justification du choix
- [x] Chargement des datasets avec Spark
- [x] Vérification des schémas
- [x] Gestion des valeurs manquantes
- [x] Normalisation des formats
- [x] Préparation des colonnes pour jointure
- [x] Justification des transformations
- [x] DataFrames propres et exploitables
- [x] Documentation dans README
- [x] Commit Git: `data_ingestion_cleaning`

---

## 📞 Contact

**ILBOUDO P. Daniel Glorieux**  
Part 1: Data Ingestion & Préparation  
Statut: ✅ Complété

**Membres du groupe:**
- ILBOUDO P. Daniel Glorieux
- PITROIPA Soraya
- KONE Khalis Aïman

---

## 🎉 Félicitations!

Vous avez maintenant un pipeline de données propre et prêt pour l'analyse. Les datasets sont nettoyés, validés et optimisés pour les étapes suivantes.

**Prochaine étape**: Passer le projet à Soraya et Khalis pour continuer! 🚀
