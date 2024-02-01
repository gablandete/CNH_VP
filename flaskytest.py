from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

DATABASE = 'produits.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def get_produits():
    with get_db_connection() as conn:
        return conn.execute('SELECT * FROM produits').fetchall()

def get_marques():
    with get_db_connection() as conn:
        return conn.execute('SELECT DISTINCT marque FROM produits').fetchall()

def get_produit_by_modele(modele):
    with get_db_connection() as conn:
        return conn.execute('SELECT * FROM produits WHERE LOWER(modele) = ?', (modele.lower(),)).fetchone()

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    produit_trouve = None
    produits = get_produits()
    marques = get_marques()

    if request.method == 'POST':
        nom_produit = request.form.get('produit')
        produit_trouve = get_produit_by_modele(nom_produit)
        
        if produit_trouve:
            message = ('Votre produit continuera à être remboursé' if produit_trouve['remboursement'] == 'Remboursé'
                       else 'Perdu, la réforme du gouvernement va probablement conduire au déremboursement de votre fauteuil')
        else:
            message = 'Produit non trouvé'
    
    return render_template('index.html', message=message, produits=produits, produit_trouve=produit_trouve, marques=marques)
