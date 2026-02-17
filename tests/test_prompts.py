import pytest
import yaml
import os

PROMPT_PATH = "prompts/bug_to_user_story_v2.yml"
PROMPT_KEY = "bug_to_user_story_v2"

def load_prompt():
    """Carrega o arquivo YAML do prompt."""
    assert os.path.exists(PROMPT_PATH), f"Arquivo {PROMPT_PATH} não encontrado."
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        return data.get(PROMPT_KEY, {})

def test_prompt_has_system_prompt():
    """Verifica se existe system_prompt no template."""
    data = load_prompt()
    assert data.get("system_prompt"), "O campo 'system_prompt' está vazio ou ausente."

def test_prompt_has_role_definition():
    """Verifica se define persona (Product Manager/Solutions Architect)."""
    data = load_prompt()
    system_prompt = data.get("system_prompt", "").lower()
    roles = ["product manager", "pm", "product owner", "solutions architect"]
    assert any(role in system_prompt for role in roles), f"Faltou definir a Persona (Role). Encontrado: {system_prompt[:100]}..."

def test_prompt_mentions_format():
    """Verifica se exige formato Markdown ou User Story."""
    data = load_prompt()
    system_prompt = data.get("system_prompt", "")
    assert "User Story" in system_prompt or "Gherkin" in system_prompt, "Não mencionou o termo 'User Story' ou 'Gherkin'."

def test_prompt_has_few_shot_examples():
    """Verifica se contém exemplos (Few-shot)."""
    data = load_prompt()
    system_prompt = data.get("system_prompt", "")
    assert "EXEMPLO" in system_prompt or "Example" in system_prompt, "Faltaram exemplos (Few-shot)."

def test_prompt_no_todos():
    """Garante que não esqueceu [TODO]."""
    data = load_prompt()
    system_prompt = data.get("system_prompt", "")
    assert "[TODO]" not in system_prompt, "Existem placeholders [TODO] não preenchidos."

def test_minimum_techniques():
    """Verifica metadados de técnicas."""
    data = load_prompt()
    techniques = data.get("techniques", [])
    assert len(techniques) >= 2, "Liste pelo menos 2 técnicas nos metadados."