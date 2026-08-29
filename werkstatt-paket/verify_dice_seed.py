#!/usr/bin/env python3
"""
verify_dice_seed.py – Unabhängige Kontrolle des SeedSigner-Dice-Modus.

SeedSigner (0.8.7, helpers/mnemonic_generation.py) rechnet:
    entropy = SHA-256( Ziffernstring "1".."6" als ASCII )
    99 Würfe -> 32 Byte -> 24 Wörter, 50 Würfe -> erste 16 Byte -> 12 Wörter
    Wörter = BIP39-Mnemonic dieser Entropie (Checksumme = führende ENT/32 Bit
    von SHA-256(entropy)).

Dieses Skript macht dieselbe Rechnung NUR mit der Python-Standardbibliothek
(hashlib) und der offiziellen BIP39-Wortliste (bip39_english.txt, SHA-256
2f5eed53a4727b4bf8880d8f3f199efc90e58503646d9ff8eff3a2ed3b24dbda) – kein
embit, kein SeedSigner-Code. Stimmen die 24 Wörter mit dem Gerät überein, hat
das Gerät korrekt gerechnet.

Aufruf:
    python3 verify_dice_seed.py              -> fragt die Ziffern ab (empfohlen:
                                                landet NICHT in der Shell-History)
    python3 verify_dice_seed.py --selftest   -> Beispiele aus docs/dice_verification.md
    python3 verify_dice_seed.py 6551522313…  -> Ziffern als Argument (nur für
                                                Test-Seeds: steht danach in
                                                ~/.bash_history!)

⚠ Wer die Ziffern kennt, kennt den Seed. Das Skript sendet nichts und schreibt
nichts, aber der Rechner sieht die Eingabe (History, Scrollback, Zwischenablage).
Deshalb: Methode einmal mit einem Wegwerf-Seed prüfen. Einen echten Seed
niemals auf einem Online-Rechner eingeben – wenn überhaupt, nur auf einem
Offline-System (z. B. Tails ohne Netz), danach herunterfahren.
"""
import hashlib, sys
from pathlib import Path

WORDLIST_SHA256 = "2f5eed53a4727b4bf8880d8f3f199efc90e58503646d9ff8eff3a2ed3b24dbda"
DOC_ROLLS = ("655152231316521321611331544441236164664431121534415633526456254462"
             "245546236542364246312613322234612")
DOC_WORDS = ("eyebrow obvious such suggest poet seven breeze blame virtual frown "
             "dynamic donor harsh pigeon express broccoli easy apology scatter force "
             "recipe shadow claim radio")
DOC_ROLLS_50 = "65515223131652132161133154444123616466443112153441"
DOC_WORDS_50 = "hole luggage safe present express tragic orbit shed switch metal identify path"

def load_wordlist():
    p = Path(__file__).with_name("bip39_english.txt")
    data = p.read_bytes()
    h = hashlib.sha256(data).hexdigest()
    if h != WORDLIST_SHA256:
        sys.exit(f"ABBRUCH: bip39_english.txt hat falschen Hash ({h})")
    words = data.decode().split()
    assert len(words) == 2048
    return words

def dice_to_mnemonic(rolls: str, wordlist):
    rolls = rolls.strip()
    if len(rolls) not in (50, 99):
        sys.exit(f"ABBRUCH: {len(rolls)} Ziffern – erwartet 99 (24 Wörter) oder 50 (12 Wörter)")
    if any(c not in "123456" for c in rolls):
        sys.exit("ABBRUCH: nur Ziffern 1–6 erlaubt")
    entropy = hashlib.sha256(rolls.encode()).digest()
    if len(rolls) == 50:
        entropy = entropy[:16]
    ent_bits = len(entropy) * 8
    cs_bits = ent_bits // 32
    checksum = hashlib.sha256(entropy).digest()
    bits = "".join(f"{b:08b}" for b in entropy) + "".join(f"{b:08b}" for b in checksum)[:cs_bits]
    return [wordlist[int(bits[i:i+11], 2)] for i in range(0, len(bits), 11)]

def main():
    wl = load_wordlist()
    if len(sys.argv) == 2 and sys.argv[1] == "--selftest":
        ok24 = " ".join(dice_to_mnemonic(DOC_ROLLS, wl)) == DOC_WORDS
        ok12 = " ".join(dice_to_mnemonic(DOC_ROLLS_50, wl)) == DOC_WORDS_50
        print("Selbsttest 99 Würfe / 24 Wörter:", "OK" if ok24 else "FEHLER")
        print("Selbsttest 50 Würfe / 12 Wörter:", "OK" if ok12 else "FEHLER")
        sys.exit(0 if ok24 and ok12 else 1)
    if len(sys.argv) == 1:
        print("Würfelziffern eingeben (99 für 24 Wörter, 50 für 12; Leerzeichen erlaubt).")
        print("⚠ Nur Test-Seed auf einem Online-Rechner. Eingabe bleibt nur im Terminal.")
        try:
            rolls = input("> ").replace(" ", "")
        except (EOFError, KeyboardInterrupt):
            sys.exit("\nAbgebrochen, nichts berechnet.")
    elif len(sys.argv) == 2:
        rolls = sys.argv[1]
        print("⚠ Hinweis: Als Argument übergebene Ziffern landen in der Shell-History.\n")
    else:
        print(__doc__); sys.exit(1)
    words = dice_to_mnemonic(rolls, wl)
    print(f"{len(words)} Wörter aus {len(rolls.strip())} Würfen:\n")
    for i, w in enumerate(words, 1):
        print(f"{i:2d}. {w}")
    print("\nAm SeedSigner Wort für Wort vergleichen (Seed Words 1/6 … 6/6).")
    print("Danach: Terminal leeren (clear) oder Fenster schließen – die Wörter stehen sonst im Scrollback.")

if __name__ == "__main__":
    main()
