# CryptoLab — César & Vigenère

Application Flask d'analyse cryptographique classique.

## Lancement rapide

```bash
pip install flask
python app.py
# Ouvrir http://127.0.0.1:5000
```

## Fonctionnalités

| Onglet | Description |
|--------|-------------|
| ① César | Chiffrer / déchiffrer avec décalage réglable + analyse fréquentielle |
| ② Vigenère | Chiffrement poly-alphabétique par clé + indice de coïncidence |


## API REST (JSON)

```
POST /api/caesar          { text, shift, mode }
POST /api/caesar/brute    { text }
POST /api/vigenere        { text, key, mode }
POST /api/analyze         { text }
```

## Structure

```
crypto_project/
├── app.py              # Serveur Flask + algorithmes
├── requirements.txt
└── templates/
    └── index.html      # Interface web complète
```
