from src.rag.prompt_builder import build_rag_prompt


def test_prompt_contains_question():
    question = "Where should I store passwords?"
    context = ["Azure Key Vault securely stores secrets."]

    prompt = build_rag_prompt(question, context)

    assert question in prompt


def test_prompt_contains_context():
    question = "Where should I store passwords?"
    context = ["Azure Key Vault securely stores secrets."]

    prompt = build_rag_prompt(question, context)

    assert context[0] in prompt


def test_prompt_contains_grounding_instruction():
    question = "What is AKS?"
    context = ["AKS is Azure Kubernetes Service."]

    prompt = build_rag_prompt(question, context)

    assert "ONLY" in prompt