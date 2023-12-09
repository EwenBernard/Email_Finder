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



def match_user_input(user_input, hunter_data):
    matched_result = None
    remaining_data = []

    for email_data in hunter_data.get('data', {}).get('emails', []):
        if 'first_name' in email_data and 'last_name' in email_data and 'value' in email_data:
            full_name = f"{email_data['first_name']} {email_data['last_name']}".lower()
            user_input_lower = user_input.lower()

            if user_input_lower in full_name:
                matched_result = {
                    'name': email_data['first_name'],
                    'last_name': email_data['last_name'],
                    'email': email_data['value'],
                    'company': hunter_data.get('data', {}).get('organization', ''),
                    'confidence': email_data.get('confidence', None),
                    'source': email_data.get('sources', [])[0]['domain'] if email_data.get('sources', []) else None,
                }
            else:
                remaining_data.append({
                    'name': email_data.get('first_name', ''),
                    'last_name': email_data.get('last_name', ''),
                    'email': email_data.get('value', ''),
                    'company': hunter_data.get('data', {}).get('organization', ''),
                    'confidence': email_data.get('confidence', None),
                    'source': email_data.get('sources', [])[0]['domain'] if email_data.get('sources', []) else None,
                })

    return matched_result, remaining_data


"""
# Exemple d'utilisation
first_name = "jean"
last_name = "soma"
company = "efrei.fr"
user_input = f"{first_name} {last_name}"
hunter_data = get_email_from_hunter(first_name, last_name, company)

matched_result, remaining_data = match_user_input(user_input, hunter_data)

#print("Matched Result:", matched_result)
#print("Remaining Data:", remaining_data)

"""
























