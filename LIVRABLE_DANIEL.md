# LIVRABLE - Part Daniel ILBOUDO
## Data Ingestion & Préparation (Fondation du pipeline)

**Date de livraison**: 26 Décembre 2025  
**Auteur**: ILBOUDO P. Daniel Glorieux  
**Projet**: Analyse E-commerce avec Apache Spark  
**Groupe**: Daniel ILBOUDO, Soraya PITROIPA, Khalis Aïman KONE

---

## ✅ LIVRABLES COMPLÉTÉS

### 1. Choix des Datasets ✅

#### Datasets Sélectionnés
- **Customers**: 150,000 lignes, 11 colonnes
- **Orders**: 200,000 lignes, 11 colonnes

#### Problématique Métier
**"Analyse du comportement d'achat des clients e-commerce pour optimiser les ventes et la satisfaction client"**

Objectifs analytiques:
- Identifier les segments de clients les plus rentables
- Analyser les tendances d'achat par catégorie et région
- Détecter les comportements anormaux (fraudes, abandons)
- Optimiser la stratégie de pricing et de fidélisation

#### Justification du Choix

✅ **Critère 1: Volumétrie suffisante**
- Customers: 150,000 lignes (> 100k requis)
- Orders: 200,000 lignes (> 100k requis)

✅ **Critère 2: Jointure pertinente**
- Clé de jointure: `customer_id`
- Relation 1-N (un client → plusieurs commandes)
- Permet analyses riches: RFM, lifetime value, segmentation

✅ **Critère 3: Problème métier réel**
- Applicable à tout e-commerce
- Questions business concrètes
- KPIs mesurables (CA, rétention, panier moyen)

✅ **Critère 4: Diversité analytique**
- Temporelle: évolution des ventes
- Géographique: performance par pays
- Comportementale: patterns d'achat
- Prédictive: churn, recommandations

**Documentation**: Voir README.md section "Choix des Datasets"

---

### 2. Ingestion des Données avec Spark ✅

#### Chargement Réalisé

```python
# Customers
df_customers = spark.read.csv(
    "data/raw/customers.csv",
    header=True,
    inferSchema=True
)

# Orders
df_orders = spark.read.csv(
    "data/raw/orders.csv",
    header=True,
    inferSchema=True
)
```

#### Vérification des Schémas

**Customers Schema:**
```
root
 |-- customer_id: integer
 |-- first_name: string
 |-- last_name: string
 |-- email: string
 |-- phone: string
 |-- registration_date: date
 |-- country: string
 |-- city: string
 |-- customer_segment: string (Bronze/Silver/Gold/Platinum)
 |-- total_spent: double
 |-- is_active: boolean
```

**Orders Schema:**
```
root
 |-- order_id: integer
 |-- customer_id: integer (FK)
 |-- order_date: date
 |-- product_category: string
 |-- product_name: string
 |-- quantity: integer
 |-- unit_price: double
 |-- total_amount: double
 |-- payment_method: string
 |-- order_status: string
 |-- shipping_country: string
```

#### Validations Effectuées
- ✅ Types de données cohérents (integer, string, double, date, boolean)
- ✅ Colonnes clés présentes (customer_id, order_id)
- ✅ Pas de colonnes manquantes
- ✅ Inférence de schéma correcte

**Code**: Voir notebook `notebooks/01_data_ingestion_cleaning.ipynb` sections 2-3

---

### 3. Nettoyage & Préparation ✅

#### A. Gestion des Valeurs Manquantes

**Customers:**
| Colonne | Valeurs NULL | Stratégie | Justification |
|---------|--------------|-----------|---------------|
| phone | 2,958 (1.97%) | → "Unknown" | Non critique pour l'analyse |
| city | 2,221 (1.48%) | → "Unknown" | Garde la ligne, pays disponible |

**Orders:**
| Colonne | Valeurs NULL | Stratégie | Justification |
|---------|--------------|-----------|---------------|
| order_status | 939 (0.47%) | → "Pending" | Statut par défaut métier |
| shipping_country | 8,050 (4.03%) | → "Unknown" | Temporaire, sera complété après jointure |

**Justification**: Suppression vs Remplacement
- **Supprimé**: Champs critiques pour calculs (montants, quantités, dates)
- **Remplacé**: Champs descriptifs non-critiques

#### B. Normalisation des Formats

**Dates:**
```python
# Avant: string "2023-05-12"
# Après: date type Spark (yyyy-MM-dd)
df = df.withColumn("registration_date", to_date(col("registration_date"), "yyyy-MM-dd"))
```

**Montants:**
```python
# Recalcul pour cohérence
df_orders = df_orders.withColumn(
    "total_amount",
    round(col("quantity") * col("unit_price"), 2)
)
```

**Justification**:
- Dates en format natif Spark → Opérations temporelles optimisées
- Montants recalculés → Élimine incohérences de saisie

#### C. Traitement des Anomalies

**Anomalies Détectées et Traitées:**

| Type Anomalie | Quantité | Action | Impact |
|---------------|----------|--------|--------|
| total_spent < 0 (customers) | 125 | Supprimé | 0.08% |
| quantity ≤ 0 (orders) | 2,012 | Supprimé | 1.01% |
| unit_price ≤ 0 (orders) | 2,064 | Supprimé | 1.03% |
| total_amount incohérent | ~4,000 | Recalculé | 2.00% |
| Emails dupliqués | 6,635 | Dédupliqué | 4.42% |

**Justification**:
- Valeurs négatives/nulles → Erreurs de saisie, aucune valeur métier
- Incohérences → Recalcul préférable à suppression
- Doublons → Garde enregistrement le plus récent (business rule)

#### D. Préparation pour Jointure

**Validations Effectuées:**

1. **Clé Primaire (customers.customer_id)**
   - ✅ Aucune valeur NULL
   - ✅ Valeurs uniques (après déduplication)
   - ✅ Type: integer

2. **Clé Étrangère (orders.customer_id)**
   - ✅ Aucune valeur NULL
   - ✅ Type: integer (même que PK)
   - ✅ Intégrité référentielle validée

3. **Test de Jointure**
   ```python
   join_test = df_orders.join(df_customers, "customer_id", "inner")
   # Résultat: 100% des orders matchent un customer
   ```

**Justification**:
- Intégrité référentielle garantie → Pas de données perdues en jointure
- Types cohérents → Performance optimale
- Validation avant sauvegarde → Évite erreurs en aval

---

### 4. DataFrames Propres et Exploitables ✅

#### Résultats Finaux

**Customers Clean:**
- Lignes: ~147,000 (98% conservées)
- Qualité: 100% (aucune valeur invalide)
- Format: Parquet + CSV
- Emplacement: `data/processed/customers_clean.parquet`

**Orders Clean:**
- Lignes: ~194,000 (97% conservées)
- Qualité: 100% (aucune valeur invalide)
- Format: Parquet + CSV
- Emplacement: `data/processed/orders_clean.parquet`

#### Métriques de Qualité

| Critère | Customers | Orders | Status |
|---------|-----------|--------|--------|
| Valeurs NULL critiques | 0 | 0 | ✅ |
| Valeurs négatives | 0 | 0 | ✅ |
| Doublons | 0 | N/A | ✅ |
| Formats normalisés | 100% | 100% | ✅ |
| Intégrité référentielle | N/A | 100% | ✅ |
| **SCORE GLOBAL** | **100%** | **100%** | ✅ |

#### Prêt pour les Étapes Suivantes

✅ **Jointure** (Soraya):
- Clés validées et cohérentes
- Aucune perte de données attendue
- Performance optimale (format Parquet)

✅ **Analyses** (Khalis):
- Données complètes et fiables
- Formats normalisés
- Calculs cohérents

---

### 5. Documentation ✅

1. **README.md**
   - Problématique métier
   - Description des datasets
   - Justification des choix
   - Transformations détaillées
   - Structure du projet
   - Instructions d'installation

2. **QUICKSTART.md**
   - Guide de démarrage rapide
   - Commandes essentielles
   - Troubleshooting
   - Statistiques des datasets

3. **notebooks/01_data_ingestion_cleaning.ipynb**
   - Code Spark complet
   - Analyses exploratoires
   - Visualisations de qualité
   - Commentaires détaillés
   - Résultats validés

4. **src/generate_datasets.py**
   - Génération automatique des données
   - Injection d'anomalies réalistes
   - Statistiques de génération

5. **requirements.txt**
   - Dépendances Python complètes
   - Versions fixées

6. **.gitignore**
   - Exclusions appropriées
   - Fichiers volumineux exclus
