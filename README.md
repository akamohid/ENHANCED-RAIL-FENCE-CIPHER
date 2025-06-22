#  🔐 Enhanced Rail-Fence Cipher (ERFC)

**😎 A Emoji-Based Encryption System for Modern Secure Communication 😍**

Developed by: **Mohid Arshad** and **Mohammad Umar**  
School of Electrical Engineering and Computer Science (SEECS)  
National University of Sciences and Technology (NUST), Islamabad, Pakistan

---

## 📘 Abstract

The **Enhanced Rail-Fence Cipher (ERFC)** is a modern encryption scheme that merges classical transposition with emoji-based substitution, aiming to bridge security with human-centered design. ERFC is built on the classical Rail Fence Cipher, enhanced with key-based emoji substitution, randomized matrix transposition, and integrity hashing via SHA-256. It is especially useful for educational, lightweight secure messaging, and cryptographic puzzles.

---

## 📚 Table of Contents

- [🔐 Enhanced Rail-Fence Cipher (ERFC)](#-enhanced-rail-fence-cipher-erfc)
  - [📘 Abstract](#-abstract)
  - [📚 Table of Contents](#-table-of-contents)
  - [🧠 Architecture Overview](#-architecture-overview)
  - [⚙️ System Components](#️-system-components)
  - [🔐 How ERFC Works](#-how-erfc-works)
    - [🔄 Substitution Mapping](#-substitution-mapping)
    - [🔳 Matrix Construction](#-matrix-construction)
    - [🧂 Salt Generation](#-salt-generation)
    - [🧬 SHA-256 Hashing](#-sha-256-hashing)
  - [🔏 Encryption Process](#-encryption-process)
  - [🔓 Decryption Process](#-decryption-process)
  - [🔐 Security Analysis](#-security-analysis)
  - [⚡ Performance \& Efficiency](#-performance--efficiency)
  - [📦 Applications](#-applications)
  - [💾 Installation](#-installation)
  - [▶️ Usage (CLI)](#️-usage-cli)
  - [🧪 Testing](#-testing)
  - [📂 Project Structure](#-project-structure)
  - [🔖 Citation](#-citation)
  - [🤝 Contributing](#-contributing)
  - [📄 License](#-license)
  - [🧾 Related Paper](#-related-paper)
  - [📞 Contact and Feedback](#-contact-and-feedback)

---

## 🧠 Architecture Overview

ERFC is based on four main layers of transformation:

1. **Substitution Layer**  
   Each character is mapped to a unique emoji using a deterministic key-based hash. This hides textual patterns and adds visual obfuscation.

2. **Grid-based Matrix Transposition**  
   The emoji-encoded message is inserted into a 2D matrix following a spiral or random walk pattern determined by a hashed key.

3. **Salt & Length Encryption**  
   The message length is encrypted and padded with salt to disguise size and improve resistance to pattern matching.

4. **SHA-256 Integrity Hash**  
   The ciphertext is shipped with a hash of the plaintext for authenticity and tamper detection.

---

## ⚙️ System Components

| Component             | Purpose                                       |
|----------------------|-----------------------------------------------|
| `emoji_map()`         | Maps each character to a unique emoji        |
| `generate_matrix()`   | Creates a randomized grid for transposition  |
| `encrypt()`           | Full pipeline for encryption (substitution → matrix → hash) |
| `decrypt()`           | Full decryption and verification             |
| `salt_and_length()`   | Obfuscates message length and adds padding   |
| `sha256_hash()`       | Ensures message authenticity and integrity   |

---

## 🔐 How ERFC Works

The encryption process involves several transformations:

### 🔄 Substitution Mapping
Each alphanumeric character is replaced with a unique emoji. The key is hashed and determines the emoji permutation used.

### 🔳 Matrix Construction
The emoji string is placed into a 2D matrix (grid) using a randomized spiral pattern, improving diffusion and hiding order.

### 🧂 Salt Generation
Salt is added to the encrypted string, and the original message length is encrypted using the key to prevent size leakage.

### 🧬 SHA-256 Hashing
The SHA-256 hash of the original plaintext is stored to verify the message on decryption.

---

## 🔏 Encryption Process

```python
from src.erfc import encrypt

plaintext = "MyPassword123"
key = "SecretKey"
ciphertext, integrity_hash = encrypt(plaintext, key)
```

**Result**:
- `ciphertext`: Encrypted emoji sequence.
- `integrity_hash`: SHA-256 hash of the original message.

---

## 🔓 Decryption Process

```python
from src.erfc import decrypt

decrypted = decrypt(ciphertext, key, integrity_hash)
assert decrypted == plaintext
```

On mismatch, the function raises an error or warning indicating integrity failure.

---

## 🔐 Security Analysis

ERFC was evaluated using standard cryptographic principles:

- **Confusion & Diffusion:** Achieved via emoji substitution and matrix transposition.
- **Avalanche Effect:** Small input changes cause widespread output differences.
- **Brute-Force Resistance:** Keyed substitution and random placement yield high entropy.
- **Frequency Analysis Defense:** Emoji layer destroys alphabetic patterns.

> See [Section VI: Security Analysis](docs/ERFC_paper.pdf) for in-depth analysis and math.

---

## ⚡ Performance & Efficiency

- Time complexity is O(n) for substitution and matrix insertion.
- Memory use is linear with message size.
- Efficient enough for short messages and emojis across platforms.

---

## 📦 Applications

- 🔐 Secure casual messaging (especially emoji-supported platforms)
- 🎮 Puzzle-based CTF (Capture The Flag) competitions
- 📚 Teaching cryptographic concepts interactively
- 🎨 Creating secret emoji art or encoding for games

---

## 💾 Installation

```bash
git clone https://github.com/akamohid/Enhanced-Rail-fence-Cipher.git

cd ERFC
python src/erfc.py
```

Optional:
```bash
python -m venv .venv
source .venv/bin/activate
```

No additional dependencies required – works with Python 3.8+.

---

## ▶️ Usage (CLI)

```bash
python src/erfc.py
```

You will be prompted to enter a message and secret key.  
Encrypted output and hash will be displayed.

---

## 🧪 Testing

```bash
python tests/test_erfc.py
```

✔️ Confirms correct encryption/decryption cycle.

---

## 📂 Project Structure

```
ERFC/
├── docs/
│   └── ERFC_paper.pdf
├── src/
│   └── erfc.py
├── tests/
│   └── test_erfc.py
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CITATION.cff
└── CHANGELOG.md
```

---

## 🔖 Citation

If used in academic or technical work, cite as:

```bibtex
@misc{mohid2025erfc,
  author       = {Mohammad Umar and Mohid Arshad},
  title        = {Enhanced Rail Fence Cipher (ERFC)},
  year         = 2025,
  howpublished = {GitHub},
  url          = {https://github.com/akamohid/Enhanced-Rail-fence-Cipher}
}
```

Or use the `CITATION.cff` included in the repository.

---

## 🤝 Contributing

We welcome contributions!

- Create a feature branch
- Follow PEP8 guidelines
- Add test cases for your changes
- Submit a pull request with a clear description

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for guidelines.

---

## 📄 License

This project is licensed under the MIT License. See [`LICENSE`](LICENSE) for full terms.

---

## 🧾 Related Paper

Full research methodology, algorithms, and evaluation are included in:

```
docs/ERFC_paper.pdf
```

---
## 📞 Contact and Feedback

GitHub: [akamohid](https://github.com/akamohid)  
Email: "akamohid@gmail.com"
