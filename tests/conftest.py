import os

import pytest
from dotenv import load_dotenv

from cf_workers_ai_model import CloudflareWorkersAI

load_dotenv()


@pytest.fixture
def base_url():
    return os.getenv("WORKER_BASE_URL", "http://localhost:8787")


@pytest.fixture
def ai_chat_url(base_url):
    return f"{base_url}/ai/chat"


@pytest.fixture
def ai_summarize_url(base_url):
    return f"{base_url}/ai/summarize"


@pytest.fixture
def eval_model():
    account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
    api_token = os.getenv("CLOUDFLARE_API_TOKEN")
    if not account_id or not api_token:
        pytest.skip("CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN required for evaluation")
    return CloudflareWorkersAI(account_id=account_id, api_token=api_token)
