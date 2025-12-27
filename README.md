# Projet d'Analyse de Données avec Apache Spark

##  Membres du Groupe
- **ILBOUDO P. Daniel Glorieux** - Data Ingestion & Préparation
- **PITROIPA Soraya** - Transformations & Jointures
- **KONE Khalis Aïman** - Analyses & Visualisations

---

##  Choix des Datasets

### Problématique Métier
**Analyse du comportement d'achat des clients e-commerce pour optimiser les ventes et la satisfaction client**

Objectifs :
- Identifier les segments de clients les plus rentables
- Analyser les tendances d'achat par catégorie et région
- Détecter les comportements anormaux (fraudes potentielles, abandons)
- Optimiser la stratégie de pricing et de fidélisation

### Datasets Sélectionnés

#### 1. **Dataset Customers (Clients)**
- **Source** : Généré avec données réalistes d'e-commerce
- **Taille** : ~150,000 lignes
- **Format** : CSV
- **Colonnes clés** :
  - `customer_id` (clé primaire)
  - `first_name`, `last_name`
  - `email`, `phone`
  - `registration_date`
  - `country`, `city`
  - `customer_segment` (Bronze, Silver, Gold, Platinum)
  - `total_spent`
  - `is_active`

#### 2. **Dataset Orders (Commandes)**
- **Source** : Généré avec données réalistes d'e-commerce
- **Taille** : ~200,000 lignes
- **Format** : CSV
- **Colonnes clés** :
  - `order_id` (clé primaire)
  - `customer_id` (clé étrangère → customers)
  - `order_date`
  - `product_category`
  - `product_name`
  - `quantity`
  - `unit_price`
  - `total_amount`
  - `payment_method`
  - `order_status`
  - `shipping_country`

### Justification du Choix

 **Volumétrie suffisante** : 150k+ et 200k+ lignes
 **Jointure naturelle** : `customer_id` permet des analyses riches
 **Problème métier réel** : applicable à tout e-commerce
 **Diversité des analyses possibles** :
  - Segmentation clients
  - Analyse temporelle
  - Analyse géographique
  - Analyse par catégorie produit
  - Détection d'anomalies (fraudes, valeurs aberrantes)

---

## 🛠️ Part 1 : Data Ingestion & Préparation (Daniel ILBOUDO)

### 1. Génération des Datasets

```bash
python src/generate_datasets.py
```

Génère :
- `data/raw/customers.csv` (~150k lignes)
- `data/raw/orders.csv` (~200k lignes)

### 2. Ingestion avec Spark

Le notebook `notebooks/01_data_ingestion_cleaning.ipynb` contient :

#### Chargement des données
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("EcommerceAnalysis") \
    .getOrCreate()

# Lecture avec inférence de schéma
df_customers = spark.read.csv("data/raw/customers.csv", header=True, inferSchema=True)
df_orders = spark.read.csv("data/raw/orders.csv", header=True, inferSchema=True)
```

#### Vérification des schémas
- Types de données automatiquement détectés
- Validation de la cohérence
- Identification des colonnes clés

### 3. Nettoyage & Préparation

#### Problèmes Identifiés et Solutions

##### **Customers Dataset**

| Problème | Impact | Solution Appliquée |
|----------|--------|-------------------|
| Valeurs manquantes dans `phone` | 2-3% | Remplacement par "Unknown" |
| Valeurs manquantes dans `city` | 1-2% | Remplacement par "Unknown" |
| Emails en double | ~0.5% | Déduplication (garde le plus récent) |
| Dates invalides | <1% | Suppression des lignes |
| `total_spent` négatif | <0.1% | Suppression (anomalies) |
| Format dates incohérent | - | Normalisation en `yyyy-MM-dd` |

##### **Orders Dataset**

| Problème | Impact | Solution Appliquée |
|----------|--------|-------------------|
| Valeurs manquantes dans `shipping_country` | 3-5% | Remplacement par pays du client (après jointure) |
| `quantity` = 0 ou négatif | ~1% | Suppression |
| `unit_price` = 0 ou négatif | ~1% | Suppression |
| `total_amount` incohérent | ~2% | Recalcul : `quantity * unit_price` |
| Format dates incohérent | - | Normalisation en `yyyy-MM-dd` |
| `order_status` NULL | <1% | Remplacement par "Pending" |

#### Transformations Appliquées

```python
# Normalisation des dates
df_customers = df_customers.withColumn(
    "registration_date_clean",
    to_date(col("registration_date"), "yyyy-MM-dd")
)

# Gestion des valeurs manquantes
df_customers = df_customers.fillna({
    "phone": "Unknown",
    "city": "Unknown"
})

# Déduplication
df_customers = df_customers.dropDuplicates(["email"])

# Validation des montants
df_orders = df_orders.filter(
    (col("quantity") > 0) & 
    (col("unit_price") > 0)
)

# Recalcul des totaux
df_orders = df_orders.withColumn(
    "total_amount_clean",
    col("quantity") * col("unit_price")
)
```

#### Préparation pour la Jointure

**Colonne de jointure** : `customer_id`

Vérifications effectuées :
-  Pas de valeurs NULL dans `customer_id` des deux datasets
-  Tous les `customer_id` dans orders existent dans customers
-  Types cohérents (Integer)
-  Clé primaire respectée (customers.customer_id unique)

### 4. Justification des Choix

#### Pourquoi ces transformations ?

1. **Valeurs manquantes** :
   - Téléphone/Ville non critiques → "Unknown" préserve les données
   - Dates/Montants critiques → Suppression pour garantir la qualité

2. **Déduplication** :
   - Emails en double = comptes multiples → garde le plus récent
   - Préserve l'intégrité référentielle

3. **Validation métier** :
   - Quantités/Prix négatifs = erreurs de saisie → Suppression
   - Total_amount recalculé → Garantit cohérence

4. **Normalisation dates** :
   - Format unique facilite les analyses temporelles
   - Compatible avec les fonctions Spark

### 5. Résultats

#### Datasets Propres Générés

**Customers Clean**
- Lignes avant : ~150,000
- Lignes après : ~147,000 (-2%)
- Prêt pour jointure : 

**Orders Clean**
- Lignes avant : ~200,000
- Lignes après : ~194,000 (-3%)
- Prêt pour jointure : 

#### Formats de Sortie

```bash
data/processed/
├── customers_clean.csv
├── customers_clean.parquet
├── orders_clean.csv
└── orders_clean.parquet
```

Parquet recommandé pour les étapes suivantes (performance).

---

##  Installation

```bash
# Créer environnement virtuel
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Installer dépendances
pip install -r requirements.txt
```

##  Utilisation

```bash
# 1. Générer les datasets
python src/generate_datasets.py

# 2. Lancer Jupyter
jupyter notebook

# 3. Ouvrir et exécuter
notebooks/01_data_ingestion_cleaning.ipynb
```

---

##  Structure du Projet

```
nouveau_projet/
├── data/
│   ├── raw/                    # Données brutes générées
│   │   ├── customers.csv
│   │   └── orders.csv
│   └── processed/              # Données nettoyées (output Part 1)
│       ├── customers_clean.csv
│       ├── customers_clean.parquet
│       ├── orders_clean.csv
│       └── orders_clean.parquet
│
├── notebooks/
│   └── 01_data_ingestion_cleaning.ipynb  # Notebook Part 1 (Daniel)
│
├── src/
│   └── generate_datasets.py    # Script de génération des données
│
├── requirements.txt            # Dépendances Python
└── README.md                   # Ce fichier
```

---

##  Prochaines Étapes (Autres Membres)

### Part 2 - Soraya : Transformations & Jointures
- Jointure `customers ⋈ orders`
- Agrégations (CA par client, par pays, par catégorie)
- Window functions (évolution temporelle)
- Création de features (RFM, lifetime value)

### Part 3 - Khalis : Analyses & Visualisations
- Segmentation clients
- Analyses prédictives
- Dashboards Matplotlib/Plotly
- Recommandations business

---

##  Technologies

- **Apache Spark 3.5+** - Traitement distribué
- **PySpark** - API Python pour Spark
- **Jupyter Notebook** - Environnement interactif
- **Pandas** - Génération de données
- **Faker** - Données réalistes

---

##  Commit Git

```bash
git add .
git commit -m "data_ingestion_cleaning - Part Daniel ILBOUDO"
git push origin main
```

---

##  Auteur - Part 1

**ILBOUDO P. Daniel Glorieux**
- Data Ingestion & Préparation
- Génération des datasets
- Nettoyage et validation
- Préparation pour jointures

- ## Part2
**PITROIPA SORAYA
-(Transformations & Jointures)
-code 02_transformations_joitures.ipynb
