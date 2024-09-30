from flask import Blueprint, render_template, request, jsonify
from app.services import get_clients_related_to_banker, get_card_titles_from_pipe, get_bankers, get_forms_status_for_card, get_child_card_details, format_status_list
import os

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    # url initial registratio 
    register_link = os.getenv('REGISTER_NEW_URL')
    
    # url para o template
    return render_template('index.html', register_link=register_link)

@bp.route('/status')
def status_page():
    return render_template('status.html')

@bp.route('/get_bankers')
def get_bankers_route():
    bankers = get_bankers()
    return jsonify(bankers)

@bp.route('/get_clients')
def get_clients():
    banker_id = request.args.get('banker_id')
    if banker_id:
        clients = get_clients_related_to_banker(banker_id)
        return jsonify(clients)
    return jsonify([])

@bp.route('/get_status')
def get_status():
    card_title = request.args.get('card_title')
    if card_title:
        forms_status = get_forms_status_for_card(card_title)
        formatted_statuses = format_status_list(forms_status)

        all_statuses = []

        # add info formatadas dos forms principais
        for status in formatted_statuses:
            all_statuses.append({
                'form': status['form'],
                'status': status['status'],
                'url': status['url']  # add URL formatada
            })

        # add info dos cards filhos
        if forms_status:  # verifica se existem itens em forms_status
            parent_card_id = forms_status[0].get('id')  # select ID do primeiro form como parent_card_id
            if parent_card_id:
                child_cards = get_child_card_details(parent_card_id)
                for child in child_cards:
                    all_statuses.append({
                        'form': child['form'],
                        'status': child['status'],
                        'url': f"https://app.pipefy.com/open-cards/{child['id']}" if child.get('id') else None  # add URL do card filho
                    })
        
        return jsonify(all_statuses)
    return jsonify([])