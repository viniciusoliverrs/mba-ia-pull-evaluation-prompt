"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()


def pull_prompts_from_langsmith():
    """
    Faz pull do prompt inicial do LangSmith Prompt Hub.
    
    Returns:
        int: 0 se sucesso, 1 se erro
    """
    print_section_header("📥 PULL DE PROMPTS DO LANGSMITH")
    
    # Verificar variáveis de ambiente necessárias
    required_vars = ["LANGSMITH_API_KEY", "LANGSMITH_PROJECT"]
    if not check_env_vars(required_vars):
        return 1
    
    try:
        # Nome do prompt no LangSmith Hub
        prompt_name = "leonanluppi/bug_to_user_story_v1"
        
        print(f"🔍 Buscando prompt: {prompt_name}")
        
        # Pull do prompt do LangSmith Hub
        prompt = hub.pull(prompt_name)
        
        print(f"✅ Prompt baixado com sucesso!")
        
        # Extrair informações do prompt
        prompt_data = {
            "bug_to_user_story_v1": {
                "description": "Prompt para converter relatos de bugs em User Stories",
                "system_prompt": str(prompt.messages[0].prompt.template) if hasattr(prompt.messages[0], 'prompt') else str(prompt.messages[0].content),
                "user_prompt": str(prompt.messages[1].prompt.template) if len(prompt.messages) > 1 and hasattr(prompt.messages[1], 'prompt') else "{bug_report}",
                "version": "v1",
                "created_at": "2025-01-15",
                "tags": ["bug-analysis", "user-story", "product-management"]
            }
        }
        
        # Salvar localmente
        output_path = "prompts/bug_to_user_story_v1.yml"
        
        # Garantir que o diretório existe
        Path("prompts").mkdir(exist_ok=True)
        
        if save_yaml(prompt_data, output_path):
            print(f"💾 Prompt salvo em: {output_path}")
            print(f"\n📋 Preview do prompt:")
            print(f"   System: {prompt_data['bug_to_user_story_v1']['system_prompt'][:100]}...")
            return 0
        else:
            print(f"❌ Erro ao salvar prompt")
            return 1
            
    except Exception as e:
        print(f"❌ Erro ao fazer pull do prompt: {e}")
        print(f"   Certifique-se de que suas credenciais do LangSmith estão corretas no .env")
        return 1


def main():
    """Função principal"""
    return pull_prompts_from_langsmith()


if __name__ == "__main__":
    sys.exit(main())
