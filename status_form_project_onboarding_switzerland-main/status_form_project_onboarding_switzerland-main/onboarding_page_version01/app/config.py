import os
from dotenv import load_dotenv

# carrega variáveis de ambiente file .env
load_dotenv()

PIPEFY_API_URL = 'https://api.pipefy.com/graphql'
HEADERS = {
    'Authorization': f'Bearer {os.getenv("PIPEFY_API_TOKEN")}'
}

# ids dos pipes carregado file .env
INITIAL_REGISTRATION_PIPE_ID = os.getenv("INITIAL_REGISTRATION_PIPE_ID")
BENEFICIARY_KYC_PIPE_ID = os.getenv("BENEFICIARY_KYC_PIPE_ID")
RISK_PROFILE_PIPE_ID = os.getenv("RISK_PROFILE_PIPE_ID")

# url do initial registration carregado file .env
REGISTER_NEW_URL = os.getenv('REGISTER_NEW_URL')