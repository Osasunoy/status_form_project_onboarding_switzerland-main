import os
from dotenv import load_dotenv

# carregando var env from .env
load_dotenv()

INITIAL_REGISTRATION_PIPE_ID = os.getenv("INITIAL_REGISTRATION_PIPE_ID")
BENEFICIARY_KYC_PIPE_ID = os.getenv("BENEFICIARY_KYC_PIPE_ID")
RISK_PROFILE_PIPE_ID = os.getenv("RISK_PROFILE_PIPE_ID")
PIPEFY_API_URL = os.getenv("PIPEFY_API_URL")
REGISTER_NEW_URL = os.getenv('REGISTER_NEW_URL')

# headers para req API
HEADERS = {
    'Authorization': f'Bearer {os.getenv("PIPEFY_API_TOKEN")}',
    'Content-Type': 'application/json'
}