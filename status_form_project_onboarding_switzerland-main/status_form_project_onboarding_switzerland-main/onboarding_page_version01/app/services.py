import requests
from app.config import PIPEFY_API_URL, HEADERS, INITIAL_REGISTRATION_PIPE_ID, BENEFICIARY_KYC_PIPE_ID, RISK_PROFILE_PIPE_ID

def get_card_titles_from_pipe(pipe_id):
    query = {
        'query': '''
        query {
            pipe(id: ''' + str(pipe_id) + ''') {
                phases {
                    name
                    cards(first: 10) {
                        edges {
                            node {
                                title
                            }
                        }
                    }
                }
            }
        }
        '''
    }
    response = requests.post(PIPEFY_API_URL, json=query, headers=HEADERS)
    if response.status_code != 200:
        print("Erro na requisição:", response.status_code)
        print("Resposta:", response.text)
        return []
    
    data = response.json()
    if 'data' not in data or 'pipe' not in data['data'] or not data['data']['pipe']:
        print("Dados inesperados na resposta:", data)
        return []

    phases = data['data']['pipe']['phases']
    card_titles = []
    for phase in phases:
        for edge in phase['cards']['edges']:
            card = edge['node']
            card_titles.append(card['title'])
    
    return card_titles

def get_forms_status_for_card(card_title):
    forms = [
        {'form': 'Initial Registration and Account Holders', 'pipe_id': INITIAL_REGISTRATION_PIPE_ID},
        {'form': 'Beneficiary Principal KYC', 'pipe_id': BENEFICIARY_KYC_PIPE_ID},
        {'form': 'Risk Profile', 'pipe_id': RISK_PROFILE_PIPE_ID}
    ]

    status_list = []

    for form in forms:
        pipe_id = form['pipe_id']
        query = {
            'query': '''
            query {
                pipe(id: ''' + str(pipe_id) + ''') {
                    phases {
                        name
                        cards(first: 10) {
                            edges {
                                node {
                                    id
                                    title
                                    current_phase {
                                        id
                                        name
                                    }
                                }
                            }
                        }
                    }
                }
            }
            '''
        }

        response = requests.post(PIPEFY_API_URL, json=query, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and 'pipe' in data['data'] and data['data']['pipe']:
                phases = data['data']['pipe']['phases']
                for phase in phases:
                    for edge in phase['cards']['edges']:
                        card = edge['node']
                        if card['title'] == card_title:
                            if card['title'] != "Banker":
                                status_list.append({
                                    'form': form['form'],
                                    'status': card['current_phase']['name'] if card['current_phase'] and card['current_phase']['name'] else 'Empty',
                                    'id': card['id']
                                })

    return status_list

def format_status_list(status_list):
    formatted_status_list = []
    for status in status_list:
        if status['form'] != "Banker":
            formatted_status_list.append({
                'form': status['form'],
                'status': status['status'],
                'url': f"https://app.pipefy.com/open-cards/{status['id']}" if 'id' in status else None
            })
    return formatted_status_list

def get_child_card_details(parent_card_id):
    query_data = {
        'query': '''
        query {
            card(id: "''' + parent_card_id + '''") {
                child_relations {
                    cards {
                        id
                        title
                        current_phase {
                            id
                            name
                        }
                        pipe {
                            name
                        }
                    }
                }
            }
        }
        '''
    }

    response = requests.post(PIPEFY_API_URL, json=query_data, headers=HEADERS)
    if response.status_code != 200:
        print("Erro na requisição:", response.status_code)
        print("Resposta:", response.text)
        return []

    response_data = response.json()

    if 'errors' in response_data:
        return []

    card_data = response_data.get('data', {}).get('card', {})
    if not card_data or not card_data.get('child_relations'):
        return []

    child_details = []
    for relation in card_data.get('child_relations', []):
        for card in relation.get('cards', []):
            current_phase_name = card.get('current_phase', {}).get('name', 'Empty')
            pipe_name = card.get('pipe', {}).get('name', 'Unknown Pipe')

            if 'Beneficiaries' in pipe_name:
                form_name = f"Additional Beneficiary KYC: {card['title']}"
            elif 'Testamentary' in pipe_name:
                form_name = f"Testamentary KYC: {card['title']}"
            else:
                form_name = f"{pipe_name}: {card['title']}"

            child_details.append({
                'form': form_name,
                'status': current_phase_name,
                'id': card.get('id')
            })
    
    return child_details

def get_bankers():
    query = {
        'query': '''
        query {
            cards(pipe_id: 304612676) {
                edges {
                    node {
                        fields {
                            field {
                                id
                                label
                            }
                            value
                        }
                    }
                }
            }
        }
        '''
    }
    response = requests.post(PIPEFY_API_URL, json=query, headers=HEADERS)
    if response.status_code != 200:
        print("Erro na requisição:", response.status_code)
        print("Resposta:", response.text)
        return []
    
    data = response.json()
    bankers = []

    for edge in data['data']['cards']['edges']:
        for field in edge['node']['fields']:
            if field['field']['id'] == 'banker':
                banker_name = field['value']
                if isinstance(banker_name, str):
                    banker_name = banker_name.strip("[]\"")
                elif isinstance(banker_name, list):
                    banker_name = banker_name[0]
                
                bankers.append({'id': banker_name, 'name': banker_name})
    
    return bankers

def get_clients_related_to_banker(banker_id):
    query = {
        'query': '''
        query {
            cards(pipe_id: 304612676) {
                edges {
                    node {
                        title
                        fields {
                            field {
                                id
                                label
                            }
                            value
                        }
                    }
                }
            }
        }
        '''
    }
    response = requests.post(PIPEFY_API_URL, json=query, headers=HEADERS)
    if response.status_code != 200:
        print("Erro na requisição:", response.status_code)
        print("Resposta:", response.text)
        return []
    
    data = response.json()
    clients = []
    for edge in data['data']['cards']['edges']:
        client = {'id': edge['node']['title'], 'name': edge['node']['title']}
        for field in edge['node']['fields']:
            if field['field']['id'] == 'banker' and banker_id in field['value']:
                clients.append(client)
                break
    
    return clients