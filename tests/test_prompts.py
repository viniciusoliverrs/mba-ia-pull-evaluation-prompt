import pytest
import yaml
import os

PROMPT_PATH = "prompts/bug_to_user_story_v2.yml"

def load_prompt():
    """Carrega o arquivo YAML do prompt."""
    assert os.path.exists(PROMPT_PATH), f"Arquivo {PROMPT_PATH} não encontrado."
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def test_prompt_has_system_prompt():
    """Verifica se existe conteúdo no template."""
    data = load_prompt()
    assert data.get("template"), "O campo 'template' está vazio."

def test_prompt_has_role_definition():
    """Verifica se define persona (Product Manager)."""
    data = load_prompt()
    template = data["template"].lower()
    roles = ["product manager", "pm", "product owner"]
    assert any(role in template for role in roles), "Faltou definir a Persona (Role)."

def test_prompt_mentions_format():
    """Verifica se exige formato Markdown ou User Story."""
    data = load_prompt()
    template = data["template"]
    assert "User Story" in template, "Não mencionou o termo 'User Story'."

def test_prompt_has_few_shot_examples():
    """Verifica se contém exemplos (Few-shot)."""
    data = load_prompt()
    template = data["template"]
    assert "EXEMPLO" in template or "Example" in template, "Faltaram exemplos (Few-shot)."

def test_prompt_no_todos():
    """Garante que não esqueceu [TODO]."""
    data = load_prompt()
    template = data["template"]
    assert "[TODO]" not in template, "Existem placeholders [TODO] não preenchidos."

def test_minimum_techniques():
    """Verifica metadados de técnicas."""
    data = load_prompt()
    techniques = data.get("metadata", {}).get("techniques", [])
    assert len(techniques) >= 2, "Liste pelo menos 2 técnicas nos metadados."