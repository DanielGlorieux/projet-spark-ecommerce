"""
Script de Génération des Datasets E-commerce
Auteur: ILBOUDO P. Daniel Glorieux
Date: 2025-12-26

Génère deux datasets volumineux avec des données réalistes :
- customers.csv (~150,000 lignes)
- orders.csv (~200,000 lignes)
"""

import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random

# Configuration
fake = Faker(['en_US', 'fr_FR', 'de_DE', 'es_ES', 'it_IT'])
Faker.seed(42)
np.random.seed(42)
random.seed(42)

# Paramètres
NUM_CUSTOMERS = 150000
NUM_ORDERS = 200000

print("🚀 Génération des datasets e-commerce...")
print(f"📊 Nombre de clients: {NUM_CUSTOMERS:,}")
print(f"📦 Nombre de commandes: {NUM_ORDERS:,}")
print()

# ========== DATASET 1: CUSTOMERS ==========
print("1️⃣ Génération du dataset CUSTOMERS...")

customers_data = []
customer_segments = ['Bronze', 'Silver', 'Gold', 'Platinum']
countries = ['France', 'USA', 'Germany', 'UK', 'Spain', 'Italy', 'Canada', 'Belgium']

for i in range(1, NUM_CUSTOMERS + 1):
    # Introduction volontaire de valeurs manquantes (2-3%)
    phone = fake.phone_number() if random.random() > 0.02 else None
    city = fake.city() if random.random() > 0.015 else None
    
    # Date d'inscription (dernières 3 années)
    registration_date = fake.date_between(
        start_date='-3y',
        end_date='today'
    )
    
    # Segment client (distribution réaliste)
    segment = np.random.choice(
        customer_segments,
        p=[0.50, 0.30, 0.15, 0.05]  # Majoritairement Bronze/Silver
    )
    
    # Total dépensé selon le segment
    if segment == 'Bronze':
        total_spent = round(random.uniform(10, 500), 2)
    elif segment == 'Silver':
        total_spent = round(random.uniform(500, 2000), 2)
    elif segment == 'Gold':
        total_spent = round(random.uniform(2000, 10000), 2)
    else:  # Platinum
        total_spent = round(random.uniform(10000, 50000), 2)
    
    # Introduction de quelques anomalies (< 0.1%)
    if random.random() < 0.001:
        total_spent = -random.uniform(10, 100)  # Valeur négative (anomalie)
    
    # Statut actif (90% actifs)
    is_active = random.random() > 0.1
    
    country = random.choice(countries)
    
    customers_data.append({
        'customer_id': i,
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': fake.email(),
        'phone': phone,
        'registration_date': registration_date.strftime('%Y-%m-%d'),
        'country': country,
        'city': city,
        'customer_segment': segment,
        'total_spent': total_spent,
        'is_active': is_active
    })
    
    if i % 30000 == 0:
        print(f"   ✓ {i:,} clients générés...")

df_customers = pd.DataFrame(customers_data)

# Introduction de doublons d'emails (~0.5%)
num_duplicates = int(NUM_CUSTOMERS * 0.005)
duplicate_indices = random.sample(range(NUM_CUSTOMERS), num_duplicates)
for idx in duplicate_indices:
    duplicate_email = df_customers.iloc[random.randint(0, NUM_CUSTOMERS-1)]['email']
    df_customers.at[idx, 'email'] = duplicate_email

print(f"   ✅ Dataset CUSTOMERS généré: {len(df_customers):,} lignes")
print()

# ========== DATASET 2: ORDERS ==========
print("2️⃣ Génération du dataset ORDERS...")

orders_data = []
product_categories = [
    'Electronics', 'Clothing', 'Home & Garden', 'Sports', 
    'Books', 'Beauty', 'Toys', 'Food', 'Automotive'
]

products = {
    'Electronics': ['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Camera'],
    'Clothing': ['T-Shirt', 'Jeans', 'Jacket', 'Dress', 'Shoes'],
    'Home & Garden': ['Chair', 'Table', 'Lamp', 'Sofa', 'Plant'],
    'Sports': ['Running Shoes', 'Yoga Mat', 'Bicycle', 'Dumbbells', 'Tennis Racket'],
    'Books': ['Fiction Book', 'Cookbook', 'Biography', 'Textbook', 'Magazine'],
    'Beauty': ['Perfume', 'Lipstick', 'Shampoo', 'Cream', 'Nail Polish'],
    'Toys': ['Action Figure', 'Board Game', 'Puzzle', 'Doll', 'LEGO Set'],
    'Food': ['Coffee', 'Chocolate', 'Wine', 'Cheese', 'Pasta'],
    'Automotive': ['Car Parts', 'Motor Oil', 'Tires', 'Battery', 'Wiper Blades']
}

payment_methods = ['Credit Card', 'PayPal', 'Bank Transfer', 'Cash on Delivery']
order_statuses = ['Completed', 'Pending', 'Shipped', 'Cancelled', 'Processing']

# Obtenir les customer_ids valides
valid_customer_ids = df_customers['customer_id'].tolist()

for i in range(1, NUM_ORDERS + 1):
    # Customer ID (80% clients actifs, 20% tous les clients)
    if random.random() < 0.8:
        customer_id = random.choice(valid_customer_ids)
    else:
        customer_id = random.choice(valid_customer_ids)
    
    # Date de commande (dernières 2 années)
    order_date = fake.date_between(
        start_date='-2y',
        end_date='today'
    )
    
    # Catégorie et produit
    category = random.choice(product_categories)
    product_name = random.choice(products[category])
    
    # Quantité (distribution réaliste)
    quantity = np.random.choice(
        [1, 2, 3, 4, 5, 10],
        p=[0.60, 0.20, 0.10, 0.05, 0.03, 0.02]
    )
    
    # Introduction d'anomalies (quantité négative ou 0)
    if random.random() < 0.01:
        quantity = random.choice([0, -1, -2])
    
    # Prix unitaire selon la catégorie
    if category == 'Electronics':
        unit_price = round(random.uniform(50, 1500), 2)
    elif category == 'Clothing':
        unit_price = round(random.uniform(10, 200), 2)
    elif category == 'Home & Garden':
        unit_price = round(random.uniform(20, 500), 2)
    elif category == 'Sports':
        unit_price = round(random.uniform(15, 800), 2)
    elif category == 'Books':
        unit_price = round(random.uniform(5, 50), 2)
    elif category == 'Beauty':
        unit_price = round(random.uniform(10, 150), 2)
    elif category == 'Toys':
        unit_price = round(random.uniform(10, 100), 2)
    elif category == 'Food':
        unit_price = round(random.uniform(5, 80), 2)
    else:  # Automotive
        unit_price = round(random.uniform(20, 300), 2)
    
    # Introduction d'anomalies (prix négatif ou 0)
    if random.random() < 0.01:
        unit_price = random.choice([0, -random.uniform(10, 100)])
    
    # Total amount (parfois incohérent - 2%)
    if random.random() < 0.02:
        total_amount = round(random.uniform(10, 1000), 2)  # Incohérent
    else:
        total_amount = round(quantity * unit_price, 2)
    
    # Shipping country (3-5% manquant)
    shipping_country = random.choice(countries) if random.random() > 0.04 else None
    
    # Payment method
    payment_method = random.choice(payment_methods)
    
    # Order status (distribution réaliste + quelques NULL)
    if random.random() < 0.005:
        order_status = None
    else:
        order_status = np.random.choice(
            order_statuses,
            p=[0.70, 0.10, 0.10, 0.05, 0.05]
        )
    
    orders_data.append({
        'order_id': i,
        'customer_id': customer_id,
        'order_date': order_date.strftime('%Y-%m-%d'),
        'product_category': category,
        'product_name': product_name,
        'quantity': quantity,
        'unit_price': unit_price,
        'total_amount': total_amount,
        'payment_method': payment_method,
        'order_status': order_status,
        'shipping_country': shipping_country
    })
    
    if i % 40000 == 0:
        print(f"   ✓ {i:,} commandes générées...")

df_orders = pd.DataFrame(orders_data)
print(f"   ✅ Dataset ORDERS généré: {len(df_orders):,} lignes")
print()

# ========== SAUVEGARDE ==========
print("3️⃣ Sauvegarde des datasets...")

output_dir = 'data/raw'
import os
os.makedirs(output_dir, exist_ok=True)

customers_path = f'{output_dir}/customers.csv'
orders_path = f'{output_dir}/orders.csv'

df_customers.to_csv(customers_path, index=False)
df_orders.to_csv(orders_path, index=False)

print(f"   ✅ {customers_path} ({len(df_customers):,} lignes, {os.path.getsize(customers_path) / (1024*1024):.2f} MB)")
print(f"   ✅ {orders_path} ({len(df_orders):,} lignes, {os.path.getsize(orders_path) / (1024*1024):.2f} MB)")
print()

# ========== STATISTIQUES ==========
print("📊 STATISTIQUES DES DATASETS")
print("=" * 60)
print()
print("CUSTOMERS:")
print(f"  • Total lignes: {len(df_customers):,}")
print(f"  • Emails uniques: {df_customers['email'].nunique():,}")
print(f"  • Emails dupliqués: {len(df_customers) - df_customers['email'].nunique():,}")
print(f"  • Valeurs manquantes:")
print(f"    - phone: {df_customers['phone'].isna().sum():,} ({df_customers['phone'].isna().sum()/len(df_customers)*100:.2f}%)")
print(f"    - city: {df_customers['city'].isna().sum():,} ({df_customers['city'].isna().sum()/len(df_customers)*100:.2f}%)")
print(f"  • Total_spent négatifs: {(df_customers['total_spent'] < 0).sum()}")
print(f"  • Distribution segments:")
for segment in customer_segments:
    count = (df_customers['customer_segment'] == segment).sum()
    print(f"    - {segment}: {count:,} ({count/len(df_customers)*100:.1f}%)")
print()

print("ORDERS:")
print(f"  • Total lignes: {len(df_orders):,}")
print(f"  • Clients uniques: {df_orders['customer_id'].nunique():,}")
print(f"  • Valeurs manquantes:")
print(f"    - shipping_country: {df_orders['shipping_country'].isna().sum():,} ({df_orders['shipping_country'].isna().sum()/len(df_orders)*100:.2f}%)")
print(f"    - order_status: {df_orders['order_status'].isna().sum():,} ({df_orders['order_status'].isna().sum()/len(df_orders)*100:.2f}%)")
print(f"  • Quantités anormales (≤0): {(df_orders['quantity'] <= 0).sum():,}")
print(f"  • Prix anormaux (≤0): {(df_orders['unit_price'] <= 0).sum():,}")
print(f"  • Distribution catégories:")
for cat in product_categories[:5]:  # Top 5
    count = (df_orders['product_category'] == cat).sum()
    print(f"    - {cat}: {count:,} ({count/len(df_orders)*100:.1f}%)")
print()

print("✅ GÉNÉRATION TERMINÉE AVEC SUCCÈS!")
print()
print("Prochaines étapes:")
print("  1. Ouvrir Jupyter: jupyter notebook")
print("  2. Exécuter: notebooks/01_data_ingestion_cleaning.ipynb")
