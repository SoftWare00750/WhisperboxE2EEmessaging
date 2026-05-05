# 📟 WhisperBox (WWB) | End-to-End Encrypted Messaging

WhisperBox is a professional-grade **Zero-Knowledge** messaging platform designed to ensure that privacy is the default state, not an option[cite: 1]. By performing all cryptographic operations locally within the browser's sandbox, the system ensures that sensitive data is never exposed to the network in an unencrypted format[cite: 1].

---

## 🏗️ System Architecture

WhisperBox operates on a **decoupled client-server model** specifically engineered to isolate cryptographic keys from the relay infrastructure[cite: 1].

*   **Frontend (The Client):** A responsive Single Page Application (SPA) that acts as the primary security controller[cite: 1]. It handles RSA key generation, AES encryption/decryption, and local data persistence via **IndexedDB**[cite: 1].
*   **Backend (The Relay):** A FastAPI service hosted at `https://whisperbox.koyeb.app/`[cite: 1]. It functions as an oblivious "blind postman," storing public keys for user discovery and routing encrypted "envelopes" between users without the technical ability to inspect their contents[cite: 1].
*   **Storage Layer:** Private keys reside exclusively on the user's device, while the remote database stores user identities, public keys, and encrypted message blobs[cite: 1].

---

## 🔐 Encryption Flow

The platform utilizes a **Hybrid Cryptosystem**, combining the efficiency of symmetric encryption with the robust key-sharing capabilities of asymmetric encryption[cite: 1].

### **1. The Sending Phase**
*   **Key Discovery:** The sender retrieves the recipient’s **RSA-OAEP 2048-bit** public key from the backend[cite: 1].
*   **Symmetric Encryption:** The application generates a random **AES-GCM 256-bit** session key to encrypt the message body, ensuring both confidentiality and integrity[cite: 1].
*   **Asymmetric Wrapping:** The AES session key is then encrypted (wrapped) using the recipient’s RSA public key[cite: 1].
*   **Data Package:** The resulting payload—consisting of the `ciphertext`, `iv` (Initialization Vector), and `encrypted_key`—is sent to the server[cite: 1].

### **2. The Receiving Phase**
*   **Retrieval:** The recipient downloads the encrypted payload from the relay[cite: 1].
*   **Unwrapping:** Using their local **Private Key** (retrieved from IndexedDB), the recipient decrypts the AES session key[cite: 1].
*   **Final Decryption:** The decrypted AES key is used to unlock the message ciphertext, revealing the original plaintext[cite: 1].

---

## 🔑 Key Management

WhisperBox places the power—and the responsibility—of digital identity management directly in the user's hands[cite: 1].

*   **Local Private Keys:** Private keys are generated on the client and stored in **IndexedDB**[cite: 1]. This browser-based storage is isolated and significantly more secure than standard `localStorage`[cite: 1].
*   **Public Key Distribution:** Public keys are shared with the server during registration, acting as "lockable boxes" that others can use to send you secure data[cite: 1].
*   **Manual Backup:** Since the server cannot recover lost keys, the application includes a **Backup** feature[cite: 1]. Users can export their keys as a `.json` file for offline storage or to transfer their identity to another device[cite: 1].

---

## ⚖️ Security Trade-offs

| Feature | Security Benefit | Practical Trade-off |
| :--- | :--- | :--- |
| **Zero-Knowledge** | Server breaches cannot leak message content[cite: 1]. | No "Password Reset" or key recovery by the administrator[cite: 1]. |
| **Local Keys** | Keys are never transmitted over the internet[cite: 1]. | Identity is tied to the specific browser/device used during setup[cite: 1]. |
| **Public Registry** | Simplifies starting new secure threads with contacts[cite: 1]. | The server can see communication metadata (who is talking to whom)[cite: 1]. |

---

## ⚠️ Known Limitations

*   **Multi-Device Synchronization:** Messages sent to one device are not automatically viewable on another unless the same private key is manually imported to the new device[cite: 1].
*   **Metadata Visibility:** While message *content* is mathematically hidden, the backend can technically observe communication patterns and timestamps[cite: 1].
*   **Recovery Dependency:** Losing both the browser's local storage and the backup file results in a permanent loss of access to all historical messages[cite: 1].
*   **1-to-1 Messaging:** This version is architected for direct peer-to-peer messaging; group encryption requires more advanced multi-recipient key wrapping protocols[cite: 1].

---

## 🚀 Deployment & Usage
1.  **Backend Status:** The backend logic is currently live and accessible at `https://whisperbox.koyeb.app/`[cite: 1].
2.  **Launch Client:** Open `whisperbox.html` in any modern web browser[cite: 1].
3.  **Registration:** Generate your keys locally and begin messaging securely[cite: 1].
