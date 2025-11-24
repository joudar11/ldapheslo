Autor: Kryštof Klika

# 🔄 AD Password History Bypasser

> „Protože moje staré heslo bylo dokonalé a odmítám se ho vzdát.“

Tento mikroprojekt slouží jako digitální protest proti bezpečnostním politikám které vynucují historii hesel. Skript automatizovaně provede sérii změn hesla v Active Directory tak aby naplnil buffer historie hesel a na konci nastavil zpět to původní které máte rádi.

## 🎯 O co jde

Administrátoři často nastavují politiku `Enforce password history` (vynucení historie hesel) typicky na hodnotu 24. To znamená že systém si pamatuje 24 minulých hesel a nedovolí vám je použít znovu.

Tento skript v Pythonu to řeší následovně:
1. Načte vaše současné heslo.
2. Cyklicky ho 23x změní přidáváním znaků čímž „vypláchne“ historii v AD.
3. Jako 24. změnu nastaví zpět vaše **původní heslo**.
4. Výsledek je, že systém i admin jsou spokojeni s provedenou změnou a vy máte své staré heslo zpět.

## 🛠 Požadavky

Ke spuštění potřebujete pouze Python a knihovnu pro práci s LDAP.

* Python 3.x
* Přístup k doménovému řadiči (nutná přítomnost ve firemní síti nebo na VPN)
* Účet v Active Directory

### Instalace závislostí

V příkazové řádce spusťte instalaci potřebné knihovny:

```bash
pip install ldap3
```

## ⚙️ Konfigurace

Před spuštěním je nutné upravit hlavičku skriptu a nastavit správnou adresu vašeho doménového řadiče.

Otevřete soubor se skriptem a upravte sekci KONFIGURACE:

```python
# ___ KONFIGURACE ___
SERVER_ADRESA = 'vas_server_ad.domena.cz' 
DOMENA = 'domena.cz' 
# ___ END KONFIGURACE ___
```

Uživatelské jméno se skript pokusí detekovat automaticky z proměnných prostředí systému.

## 🚀 Použití
Spusťte skript v terminálu:

```bash
python main.py
```
Zadejte své aktuální heslo.

Sledujte magii v přímém přenosu. Skript bude vypisovat průběh změn.

Po dokončení se můžete ihned přihlásit svým starým heslem.

## ⚠️ Disclaimer a varování
Použití tohoto skriptu je čistě na vlastní nebezpečí.

- Logy a SIEM: Tento skript vygeneruje 24 událostí změny hesla během několika sekund. Váš bezpečnostní tým to v logách uvidí a pravděpodobně to vyvolá poplach. Mějte připravenou dobrou výmluvu nebo čokoládu pro sys adminy.

- Minimální stáří hesla: Pokud máte v AD nastavenou politiku Minimum Password Age na hodnotu vyšší než 0 tento skript selže hned při prvním pokusu a může dojít k uzamčení účtu.

- Účel: Tento nástroj slouží výhradně ke studijním účelům a k demonstraci chování politik Active Directory. Autor nenese odpovědnost za případné problémy v zaměstnání.
