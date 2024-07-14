# Super Tramp Supported files

Repozitář se skripty, které generují podpůrné soubory na dětský tábor SuperTramp.

## Skripty

| jmeno             | soubor                       | popis                                                                                                                                                                                       |
| ----------------- | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Lístky do letadla | `generate-airport-ticket.py` | Letadlové lístky pro každé díte z tábora. Skript čte jména ze souboru `names.txt` a údaje na lístek jsou generované ve skriptu.                                                             |
| Šifry             | `generate-secret.py`         | Šifruje text tak, že náhodně prohodí písmenka v abecedě. Výstupem skriptu jsou dva pdf soubory (`cipher.pdf` a `encrypted_texts.pdf`). První obashuje klíč k šifře, druhý zašifrovaný text. |
| Čtyřmístná čísla  | `generate-numbers-cards.py`  | Generuje na papír 6 čtyřmínstých čísel v náhodném pořadí. Skript zajistí, že se čísla nikdy neopakují.                                                                                      |
