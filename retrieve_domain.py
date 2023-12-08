import requests

def get_email_from_hunter(first_name, last_name, company, api_key):
    url = "https://api.hunter.io/v2/domain-search"

    params = {
        "company": company,
        "first_name": first_name,
        "last_name": last_name,
        "api_key": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()

    # Obtenez l'adresse e-mail à partir des résultats de la recherche
    if data.get("data", {}).get("emails"):
        return data["data"]["emails"][0]["value"]  # Renvoie la première adresse e-mail trouvée
    else:
        return None  # Aucune adresse e-mail trouvée

# Exemple d'utilisation de la fonction
first_name = "julio"
last_name = "ibc"
company = "capgemini"
api_key = "58f5d6980b1a5b9b191d4185525104dc40b8eb57"

email = get_email_from_hunter(first_name, last_name, company, api_key)

if email:
    print(f"L'adresse e-mail trouvée est : {email}")
else:
    print("Aucune adresse e-mail trouvée.")

































"""import requests

def get_domain_by_company_name(api_key, company_name):
    url = f"https://company.clearbit.com/v2/companies/find?name={company_name}"

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Gère les erreurs HTTP
        data = response.json()

        # Vérifie si des données d'entreprise ont été trouvées
        if data.get('id'):
            domain = data['domain']
            return domain
        else:
            return None

    except requests.exceptions.RequestException as e:
        print(f"Une erreur s'est produite lors de la requête : {e}")
        return None

# Remplacez "VOTRE_CLE_API_CLEARBIT" par votre clé API Clearbit
api_key = "sk_2d6388be3ba6277b96f362027e6f1ac2"
company_name = "airbnb.com"

domain = get_domain_by_company_name(api_key, company_name)

if domain:
    print(f"Le domaine de {company_name} est : {domain}")
else:
    print(f"Aucun domaine trouvé pour {company_name}")
"""