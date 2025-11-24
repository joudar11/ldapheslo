import ldap3
import os
import sys
import time
import getpass

# --- KONFIGURACE ---
SERVER_ADRESA = "adresa.domenoveho.radice.firma.cz"
DOMENA = "domena.firma.cz"
# --- END KONFIGURACE ---
STARE_HESLO = getpass.getpass("Zadejte vaše heslo: ")
POSLEDNI_HESLO = STARE_HESLO
# Získání systémových informací
UZIVATEL_SAM = os.environ.get('USERNAME') 
UPN = f'{UZIVATEL_SAM}@{DOMENA}'

HISTORIE_HESEL = 24

if not UZIVATEL_SAM:
    print("CHYBA: Nepodařilo se získat uživatelské jméno.")
    sys.exit(1)

for i in range(HISTORIE_HESEL):

    print(f"Probíhá změna hesla pro uživatele: {UPN}")

    if i == HISTORIE_HESEL-1:
        NOVE_HESLO = POSLEDNI_HESLO
    else:
        NOVE_HESLO = STARE_HESLO + "1"

    try:
        # 1. Navázání zabezpečeného spojení (LDAPS)
        server = ldap3.Server(SERVER_ADRESA, port=636, use_ssl=True, get_info=ldap3.ALL)
        conn = ldap3.Connection(server, user=UPN, password=STARE_HESLO, auto_bind=True)

        if not conn.bind:
            raise Exception(f"Ověření uživatele {UPN} se starým heslem selhalo. Chyba: {conn.result['description']}")

        # 2. Vyhledání uživatelského objektu (pro získání DN)
        # Získání Base DN z informací o serveru
        try:
            base_dn = conn.server.info.other['defaultNamingContext'][0]
        except (IndexError, KeyError):
            # Fallback pro případ, že informace o serveru nejsou dostupné
            print("[Inference] Nelze automaticky zjistit Base DN. Použijeme nejčastější formát.")
            base_dn = ','.join([f'dc={part}' for part in DOMENA.split('.')])
        
        conn.search(base_dn, f'(sAMAccountName={UZIVATEL_SAM})', attributes=['distinguishedName'])
        
        if not conn.entries:
            raise Exception(f"Nepodařilo se najít uživatele {UZIVATEL_SAM} v Active Directory.")
            
        user_dn = conn.entries[0].distinguishedName

        # 3. Změna hesla pomocí rozšířené operace 6806 (Microsoft standard)
        success = conn.extend.microsoft.modify_password(user_dn, NOVE_HESLO, STARE_HESLO)

        if success:
            print("\n✅ ÚSPĚCH: Heslo bylo úspěšně změněno v Active Directory.")
        else:
            raise Exception(f"Změna hesla selhala. AD chyba: {conn.result['description']}")

        conn.unbind()
        
    except ldap3.core.exceptions.LDAPInvalidCredentialsResult:
        print(f"\nCHYBA: Staré heslo pro uživatele {UPN} je neplatné. Změna nebyla provedena.")
    except Exception as e:
        print(f"\nKRITICKÁ CHYBA: {e}")
        sys.exit(1)
    
    STARE_HESLO = NOVE_HESLO
    time.sleep(2)