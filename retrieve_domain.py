import requests

def get_email_from_hunter(first_name, last_name, company):
    url = "https://api.hunter.io/v2/domain-search"

    params = {
        "company": company,
        "first_name": first_name,
        "last_name": last_name,
        "api_key": "58f5d6980b1a5b9b191d4185525104dc40b8eb57"
    }

    response = requests.get(url, params=params)
    data = response.json()
    return data 

"""    # Obtenez l'adresse e-mail à partir des résultats de la recherche
    if data.get("data", {}).get("emails"):
        return data["data"]["emails"][0]["value"]  # Renvoie la première adresse e-mail trouvée
    else:
        return None  # Aucune adresse e-mail trouvée
    """

# Exemple d'utilisation de la fonction
first_name = "jean"
last_name = "soma"
company = "efrei.fr"

email = get_email_from_hunter(first_name, last_name, company)

if email:
    print(f"L'adresse e-mail trouvée est : {email}")
else:
    print("Aucune adresse e-mail trouvée.")



























