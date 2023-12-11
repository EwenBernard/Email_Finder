import requests

def get_email_from_hunter(first_name, last_name, company):
    try:
        url = "https://api.hunter.io/v2/domain-search"
        
        params = {
            "company": company,
            "api_key": "b18518ca2df34f86a00242e974b7866469b51702"
        }
        response = requests.get(url, params=params)
        data = response.json()

        # Check if the request was successful
        response.raise_for_status()
        print("DOMAIN", data["data"]["domain"])

        params = {
            "first_name": first_name,
            "last_name": last_name,
            "api_key": "b18518ca2df34f86a00242e974b7866469b51702"
        }

        if data["data"]["domain"]:
            params["domain"] = data["data"]["domain"]
        else:
            params["company"] = company

        response = requests.get(url, params=params)
        data = response.json()

        # Check if the request was successful
        response.raise_for_status()
        return data

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None



def match_user_input(name, last_name, hunter_data):
    matched_result = None
    remaining_data = []
    input_name = name.lower().strip()
    input_last_name = last_name.lower().strip()

    for email_data in hunter_data.get('data', {}).get('emails', []):
        if 'value' in email_data:
            if email_data['first_name'] and email_data['last_name'] and input_name == email_data['first_name'].lower() and input_last_name == email_data['last_name'].lower():
                matched_result = {
                    'name': email_data['first_name'],
                    'last_name': email_data['last_name'],
                    'email': email_data['value'],
                    'company': hunter_data.get('data', {}).get('organization', ''),
                    'confidence': email_data.get('confidence', None),
                    'source': email_data.get('sources', [])[0]['domain'] if email_data.get('sources', []) else None,
                }
            else:
                if not email_data.get('first_name', '') and not email_data.get('last_name', ''):
                    name = last_name = "Unknown"
                else:
                    name = email_data.get('first_name', '')
                    last_name = email_data.get('last_name', '')

                remaining_data.append({
                    'name': name,
                    'last_name': last_name,
                    'email': email_data.get('value', ''),
                    'company': hunter_data.get('data', {}).get('organization', ''),
                    'confidence': email_data.get('confidence', None),
                    'source': email_data.get('sources', [])[0]['domain'] if email_data.get('sources', []) else None,
                })
    if not remaining_data:
        remaining_data = None

    return matched_result, remaining_data


"""
# Exemple d'utilisation
first_name = "jean"
last_name = "soma"
company = "efrei.fr"

email = get_email_from_hunter(first_name, last_name, company)

matched_result, remaining_data = match_user_input(user_input, hunter_data)

#print("Matched Result:", matched_result)
#print("Remaining Data:", remaining_data)

"""
























