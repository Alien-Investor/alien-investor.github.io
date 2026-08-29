#!/usr/bin/env bash
# dice-check.sh – Wrapper für verify_dice_seed.py (Würfel-Check SeedSigner)
#
# Prüft VOR jedem Start, dass Prüfskript und BIP39-Wortliste unverändert sind
# (sha256sum -c gegen SHA256SUMS im selben Ordner), und ruft dann das Skript
# auf. Damit ist die Prüfung nicht mehr zirkulär: verify_dice_seed.py prüft
# die Wortliste gegen eine Konstante in sich selbst – wer das Skript ändert,
# kann auch die Konstante ändern. Das SHA256SUMS-Manifest ist ein zweiter
# Kanal, den man auf Papier oder im Buch mitführt und von Hand vergleicht.
#
# ⚠ Auch dieser Wrapper ist nur so vertrauenswürdig wie sein Fundort. Ideal:
# alle vier Dateien (dice-check.sh, verify_dice_seed.py, bip39_english.txt,
# SHA256SUMS) in der Tails-Persistenz, Hashes einmal von Hand gegen das Buch /
# die Download-Seite abgeglichen. Danach: `./dice-check.sh` ohne Argumente
# (Ziffern werden abgefragt, landen nicht in der Shell-History) oder
# `./dice-check.sh --selftest`.
#
# Repo-Fassung: rekonstruiert am 2026-08-18 nach dem Merkzettel
# material/2026-08-17-merkzettel-claude-web-wuerfelpruefung-tails.md; das
# Original liegt in der Tails-Persistenz des Autors (~/Persistent/seedsigner/
# dice/) – beim nächsten Tails-Start per `diff` abgleichen, Abweichungen hier
# nachziehen.
set -euo pipefail

cd "$(dirname "$(readlink -f "$0")")"

for f in verify_dice_seed.py bip39_english.txt SHA256SUMS; do
  [ -f "$f" ] || { echo "ABBRUCH: $f fehlt in $(pwd)"; exit 2; }
done

echo "Integritätsprüfung (SHA256SUMS):"
if ! sha256sum -c --strict SHA256SUMS; then
  echo
  echo "ABBRUCH: Hash-Abweichung – Skript oder Wortliste wurden verändert."
  echo "Nicht verwenden. Dateien neu holen und Hashes gegen den zweiten Kanal prüfen."
  exit 1
fi
echo

exec python3 verify_dice_seed.py "$@"
