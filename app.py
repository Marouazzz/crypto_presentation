from flask import Flask, render_template, request, jsonify
import string
import collections

app = Flask(__name__)

# ─────────────────────────────────────────
#  ALGORITHME DE CÉSAR
# ─────────────────────────────────────────

def caesar_cipher(text: str, shift: int, mode: str = "encrypt") -> str:
    """Chiffrement/Déchiffrement de César."""
    if mode == "decrypt":
        shift = -shift
    result = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result.append(chr((ord(char) - base + shift) % 26 + base))
        else:
            result.append(char)
    return "".join(result)


def caesar_brute_force(ciphertext: str) -> list[dict]:
    """Attaque par force brute sur César — retourne les 26 décalages."""
    results = []
    for shift in range(26):
        decrypted = caesar_cipher(ciphertext, shift, mode="decrypt")
        results.append({"shift": shift, "text": decrypted})
    return results


# ─────────────────────────────────────────
#  ALGORITHME DE VIGENÈRE
# ─────────────────────────────────────────

def vigenere_cipher(text: str, key: str, mode: str = "encrypt") -> str:
    """Chiffrement/Déchiffrement de Vigenère."""
    key = key.upper()
    key_filtered = [c for c in key if c.isalpha()]
    if not key_filtered:
        return text

    result = []
    key_idx = 0
    for char in text:
        if char.isalpha():
            shift = ord(key_filtered[key_idx % len(key_filtered)]) - ord('A')
            if mode == "decrypt":
                shift = -shift
            base = ord('A') if char.isupper() else ord('a')
            result.append(chr((ord(char) - base + shift) % 26 + base))
            key_idx += 1
        else:
            result.append(char)
    return "".join(result)


# ─────────────────────────────────────────
#  ANALYSE DE FRÉQUENCE
# ─────────────────────────────────────────

FRENCH_FREQ = {
    'E': 14.715, 'A': 7.636, 'I': 7.529, 'S': 7.948, 'N': 7.095,
    'R': 6.553, 'T': 7.244, 'O': 5.378, 'L': 5.456, 'U': 6.311,
    'D': 3.669, 'C': 3.260, 'M': 2.968, 'P': 2.521, 'V': 1.628,
    'G': 1.049, 'F': 1.066, 'B': 0.901, 'H': 0.737, 'Q': 1.362,
    'J': 0.613, 'X': 0.427, 'Z': 0.326, 'Y': 0.128, 'K': 0.049, 'W': 0.114
}

ENGLISH_FREQ = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97,
    'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25,
    'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36,
    'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.49,
    'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07
}

def frequency_analysis(text: str) -> dict:
    """Analyse de fréquence des lettres d'un texte."""
    letters_only = [c.upper() for c in text if c.isalpha()]
    if not letters_only:
        return {"frequencies": {}, "total": 0, "most_common": []}

    total = len(letters_only)
    counter = collections.Counter(letters_only)
    frequencies = {letter: round((count / total) * 100, 2)
                   for letter, count in counter.items()}
    most_common = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)[:10]

    return {
        "frequencies": frequencies,
        "total": total,
        "most_common": most_common
    }


def index_of_coincidence(text: str) -> float:
    """Calcule l'indice de coïncidence (IC) du texte."""
    letters = [c.upper() for c in text if c.isalpha()]
    n = len(letters)
    if n < 2:
        return 0.0
    counter = collections.Counter(letters)
    ic = sum(count * (count - 1) for count in counter.values()) / (n * (n - 1))
    return round(ic, 6)


# ─────────────────────────────────────────
#  ROUTES FLASK
# ─────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/caesar", methods=["POST"])
def api_caesar():
    data = request.get_json()
    text = data.get("text", "")
    shift = int(data.get("shift", 3))
    mode = data.get("mode", "encrypt")
    result = caesar_cipher(text, shift, mode)
    freq = frequency_analysis(result)
    ic = index_of_coincidence(result)
    return jsonify({"result": result, "frequency": freq, "ic": ic})


@app.route("/api/caesar/brute", methods=["POST"])
def api_caesar_brute():
    data = request.get_json()
    text = data.get("text", "")
    results = caesar_brute_force(text)
    return jsonify({"results": results})


@app.route("/api/vigenere", methods=["POST"])
def api_vigenere():
    data = request.get_json()
    text = data.get("text", "")
    key = data.get("key", "")
    mode = data.get("mode", "encrypt")
    if not key:
        return jsonify({"error": "La clé ne peut pas être vide"}), 400
    result = vigenere_cipher(text, key, mode)
    freq = frequency_analysis(result)
    ic = index_of_coincidence(result)
    return jsonify({"result": result, "frequency": freq, "ic": ic})


@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    data = request.get_json()
    text = data.get("text", "")
    freq = frequency_analysis(text)
    ic = index_of_coincidence(text)
    brute = caesar_brute_force(text)
    return jsonify({"frequency": freq, "ic": ic, "brute_force": brute})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
