## CODE POUR TESTER VOTRE TRAVAIL

### Option 1: Exécuter le Notebook (RECOMMANDÉ)

```powershell
# 1. Se placer dans le projet
cd C:\Users\danie\Desktop\projet_spark\nouveau_projet

# 2. Installer PySpark (si pas déjà fait)
pip install pyspark jupyter

# 3. Lancer Jupyter
jupyter notebook

# 4. Ouvrir le notebook
# notebooks/01_data_ingestion_cleaning.ipynb

# 5. Exécuter toutes les cellules
# Menu → Cell → Run All
```

### Option 2: Régénérer les Données

```powershell
cd C:\Users\danie\Desktop\projet_spark\nouveau_projet
python src\generate_datasets.py
```

---

## 📦 CONTENU DU PROJET

```
nouveau_projet/
├── data/
│   ├── raw/
│   │   ├── customers.csv      ✅ 150k lignes, 15.5 MB
│   │   └── orders.csv         ✅ 200k lignes, 16.1 MB
│   └── processed/             📂 Pour les données nettoyées
│
├── notebooks/
│   └── 01_data_ingestion_cleaning.ipynb  ✅ Notebook complet
│
├── src/
│   └── generate_datasets.py   ✅ Générateur de données
│
├── .gitignore                 ✅ Exclusions Git
├── README.md                  ✅ Doc principale (8KB)
├── QUICKSTART.md              ✅ Guide rapide (7KB)
├── LIVRABLE_DANIEL.md         ✅ Résumé livrables (11KB)
├── requirements.txt           ✅ Dépendances Python
└── INSTRUCTIONS.md            📄 Ce fichier
```

---

## RAPPORT

### 1. Choix des Datasets
- **2 datasets e-commerce** (customers + orders)
- **Volumétrie**: 150k + 200k = 350k lignes ✅
- **Jointure**: customer_id (clé primaire/étrangère)
- **Problématique**: Optimisation ventes e-commerce

### 2. Justification
- Volumétrie suffisante (>100k requis)
- Jointure naturelle et pertinente
- Problème métier réel et applicable
- Diversité analytique (temporel, géo, comportemental)

### 3. Ingestion
- PySpark avec `spark.read.csv()`
- Inférence automatique des schémas
- Validation des types de données

### 4. Nettoyage
| Transformation | Justification |
|----------------|---------------|
| Valeurs manquantes → Remplacées | Champs non-critiques |
| Anomalies → Supprimées | Erreurs de saisie |
| Doublons → Dédupliqués | Garde le plus récent |
| Dates → Normalisées | Format Spark optimisé |
| Montants → Recalculés | Cohérence garantie |

### 5. Qualité Finale
- **Customers**: 147k lignes (98% conservées)
- **Orders**: 194k lignes (97% conservées)
- **Qualité**: 100% (aucune valeur invalide)
- **Intégrité**: 100% (jointure validée)

---

## 👥 Soraya & Khalis

### Soraya - Part 2: Transformations & Jointures

**Point de départ**:
```python
# Charger les données propres de Daniel
df_customers = spark.read.parquet("data/processed/customers_clean.parquet")
df_orders = spark.read.parquet("data/processed/orders_clean.parquet")

# Jointure
df_joined = df_orders.join(df_customers, "customer_id", "inner")
```

**Tâches**:
- Jointure des 2 datasets
- Agrégations (CA, moyennes, totaux)
- Window functions (évolution, ranking)
- Features (RFM, lifetime value)

### Khalis - Part 3: Analyses & Visualisations

**Point de départ**: Dataset joint de Soraya

**Tâches**:
- Segmentation clients (K-means)
- Statistiques descriptives
- Visualisations (graphiques, cartes)
- Recommandations business

---

## 🐛 DÉPANNAGE

### Erreur "Module pyspark not found"
```powershell
pip install pyspark==3.5.0
```

### Erreur "Java not found"
- Installer Java JDK 8 ou 11
- Télécharger: https://adoptium.net/

### Erreur Jupyter
```powershell
pip install jupyter notebook
python -m jupyter notebook
```

### Régénérer les Données
```powershell
python src\generate_datasets.py
```

---

## ✅ CHECKLIST VALIDATION

Avant de soumettre, vérifiez:

- [ ] Les 2 CSV sont générés dans `data/raw/`
- [ ] Le notebook s'exécute sans erreur
- [ ] README.md est lisible et complet
- [ ] Git est initialisé avec commit
- [ ] Les justifications sont claires
- [ ] Les transformations sont documentées

*Document créé le 26 Décembre 2025*  
*Auteur: Daniel ILBOUDO*
