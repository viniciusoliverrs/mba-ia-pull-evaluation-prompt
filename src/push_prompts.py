"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header

load_dotenv()


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).
    Suporta dois formatos:
    1. Formato antigo: system_prompt + user_prompt (strings)
    2. Formato novo: messages (array conversacional)

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """
    try:
        username = os.getenv("USERNAME_LANGSMITH_HUB")

        # Se não tem username, fazer push sem prefixo para descobrir o handle
        if not username or username.strip() == "":
            print("⚠️  USERNAME_LANGSMITH_HUB não configurado")
            print("   Fazendo push SEM username para descobrir seu handle automático...")
            full_prompt_name = prompt_name
        else:
            # Nome completo no formato: username/prompt-name
            full_prompt_name = f"{username}/{prompt_name}"

        print(f"📤 Preparando push do prompt: {full_prompt_name}")

        # Detectar formato do prompt
        if "messages" in prompt_data:
            # Formato novo: messages array (formato nativo LangChain)
            print(f"✓ Detectado formato conversacional (messages)")
            messages = prompt_data.get("messages", [])

            if not messages:
                print("❌ Array 'messages' está vazio")
                return False

            # Construir lista de tuplas (role, content) para ChatPromptTemplate
            message_tuples = []
            for msg in messages:
                role = msg.get("role", "")
                content = msg.get("content", "")

                if not role or not content:
                    print(f"⚠️  Mensagem inválida detectada (role ou content vazio)")
                    continue

                # Mapear roles para formato LangChain
                if role == "system":
                    message_tuples.append(("system", content))
                elif role == "human" or role == "user":
                    message_tuples.append(("human", content))
                elif role == "ai" or role == "assistant":
                    message_tuples.append(("assistant", content))
                else:
                    print(f"⚠️  Role desconhecido: {role}, usando 'human'")
                    message_tuples.append(("human", content))

            if not message_tuples:
                print("❌ Nenhuma mensagem válida encontrada")
                return False

            # Criar ChatPromptTemplate com messages
            prompt_template = ChatPromptTemplate.from_messages(message_tuples)

        else:
            # Formato antigo: system_prompt + user_prompt (strings)
            print(f"✓ Detectado formato legado (system_prompt + user_prompt)")
            system_prompt = prompt_data.get("system_prompt", "")
            user_prompt = prompt_data.get("user_prompt", "{bug_report}")

            if not system_prompt:
                print("❌ system_prompt não encontrado nos dados do prompt")
                return False

            # Criar ChatPromptTemplate do LangChain
            prompt_template = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", user_prompt)
            ])

        print(f"✅ Template criado com sucesso")

        # Fazer push para o LangSmith Hub
        print(f"🚀 Fazendo push para o LangSmith Hub...")

        # Tentar fazer push público primeiro
        try:
            hub.push(
                full_prompt_name,
                prompt_template,
                new_repo_is_public=True  # IMPORTANTE: tornar público
            )
            print(f"✅ Push PÚBLICO realizado com sucesso!")
        except Exception as e:
            if "Hub handle" in str(e) or "public prompt" in str(e):
                # Fallback: fazer push privado
                print(f"⚠️  Push público falhou (handle não configurado). Fazendo push privado...")
                hub.push(
                    full_prompt_name,
                    prompt_template,
                    new_repo_is_public=False
                )
                print(f"✅ Push PRIVADO realizado com sucesso!")
                print(f"💡 Para tornar público: https://smith.langchain.com/prompts/{full_prompt_name}")
            else:
                raise  # Re-raise se for outro tipo de erro

        print(f"🔗 Acesse em: https://smith.langchain.com/hub/{full_prompt_name}")

        # Exibir metadados
        metadata = prompt_data.get("metadata", prompt_data)  # Suportar ambos metadata e root level
        techniques = metadata.get("techniques", [])

        if techniques:
            print(f"\n📋 Técnicas aplicadas:")
            if isinstance(techniques, list):
                for tech in techniques:
                    print(f"   - {tech}")
            elif isinstance(techniques, dict):
                for tech in techniques.values():
                    print(f"   - {tech}")

        return True

    except Exception as e:
        print(f"❌ Erro ao fazer push do prompt: {e}")
        import traceback
        traceback.print_exc()
        return False


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt.
    Suporta dois formatos:
    1. Formato antigo: system_prompt + user_prompt
    2. Formato novo: messages array

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    errors = []

    # Validar descrição (obrigatório em ambos formatos)
    if "description" not in prompt_data:
        errors.append("description ausente")

    # Detectar formato e validar de acordo
    if "messages" in prompt_data:
        # Formato novo: messages array
        messages = prompt_data.get("messages", [])

        if not messages or len(messages) == 0:
            errors.append("messages array ausente ou vazio")
            return (False, errors)

        # Verificar se tem pelo menos uma mensagem com {bug_report}
        has_bug_report_var = False
        total_content_length = 0

        for msg in messages:
            content = msg.get("content", "")
            total_content_length += len(content)

            if "{bug_report}" in content:
                has_bug_report_var = True

        if not has_bug_report_var:
            errors.append("Nenhuma mensagem contém a variável {bug_report}")

        # Verificar tamanho mínimo total (prompt otimizado deve ser elaborado)
        if total_content_length < 500:
            errors.append(f"Conteúdo total das mensagens muito curto ({total_content_length} chars). Esperado: > 500 chars")

    else:
        # Formato antigo: system_prompt + user_prompt
        if "system_prompt" not in prompt_data or not prompt_data["system_prompt"]:
            errors.append("system_prompt ausente ou vazio")

        if "user_prompt" not in prompt_data or not prompt_data["user_prompt"]:
            errors.append("user_prompt ausente ou vazio")

        # Validar se contém {bug_report}
        system_prompt = prompt_data.get("system_prompt", "")
        user_prompt = prompt_data.get("user_prompt", "")

        if "{bug_report}" not in system_prompt and "{bug_report}" not in user_prompt:
            errors.append("Nenhum prompt contém a variável {bug_report}")

        # Verificar tamanho mínimo
        if len(system_prompt) < 500:
            errors.append(f"system_prompt muito curto ({len(system_prompt)} chars). Esperado: > 500 chars")

    return (len(errors) == 0, errors)


def main():
    """Função principal"""
    print_section_header("📤 PUSH DE PROMPTS OTIMIZADOS PARA O LANGSMITH")
    
    # Verificar variáveis de ambiente
    required_vars = ["LANGSMITH_API_KEY"]
    if not check_env_vars(required_vars):
        return 1
    
    # Carregar prompts otimizados
    # Usar argumento da linha de comando ou fallback para v2.yml
    prompts_file = sys.argv[1] if len(sys.argv) > 1 else "prompts/bug_to_user_story_v2.yml"
    
    print(f"📂 Carregando prompts de: {prompts_file}")
    
    prompts_data = load_yaml(prompts_file)
    if not prompts_data:
        print(f"❌ Erro ao carregar arquivo {prompts_file}")
        return 1
    
    print(f"✅ Arquivo carregado com sucesso")

    # Detectar se é um único prompt ou múltiplos
    # Single prompt tem _type: prompt no root level
    if "_type" in prompts_data and prompts_data.get("_type") == "prompt":
        # Formato single prompt (LangChain native)
        print(f"✓ Detectado: Single prompt (formato nativo LangChain)")

        # Usar nome extraído do arquivo
        import os
        prompt_name = os.path.splitext(os.path.basename(prompts_file))[0]
        prompt_data = prompts_data

        print(f"\n{'='*60}")
        print(f"🔍 Processando: {prompt_name}")
        print(f"{'='*60}")

        # Validar prompt
        print(f"✓ Validando estrutura do prompt...")
        is_valid, errors = validate_prompt(prompt_data)

        if not is_valid:
            print(f"❌ Validação falhou:")
            for error in errors:
                print(f"   - {error}")
            return 1

        print(f"✅ Validação passou!")

        # Exibir resumo (código já existente será movido aqui)
        print(f"\n📋 Resumo do prompt:")
        print(f"   Descrição: {prompt_data.get('description', 'N/A')}")

        if "messages" in prompt_data:
            metadata = prompt_data.get('metadata', {})
            version = metadata.get('version', prompt_data.get('version', 'N/A'))
            messages = prompt_data.get('messages', [])
            total_chars = sum(len(msg.get('content', '')) for msg in messages)

            print(f"   Versão: {version}")
            print(f"   Formato: Conversacional (messages)")
            print(f"   Total de mensagens: {len(messages)}")
            print(f"   Total de caracteres: {total_chars}")
        else:
            version = prompt_data.get('version', 'N/A')
            system_prompt_len = len(prompt_data.get('system_prompt', ''))

            print(f"   Versão: {version}")
            print(f"   Formato: Legado (system_prompt)")
            print(f"   System prompt: {system_prompt_len} caracteres")

        # Fazer push
        if push_prompt_to_langsmith(prompt_name, prompt_data):
            success_count = 1
            fail_count = 0
        else:
            success_count = 0
            fail_count = 1

    else:
        # Formato multi-prompt (legado)
        print(f"✓ Detectado: Multi-prompt (formato legado)")

        # Processar cada prompt
        success_count = 0
        fail_count = 0

        for prompt_name, prompt_data in prompts_data.items():
            print(f"\n{'='*60}")
            print(f"🔍 Processando: {prompt_name}")
            print(f"{'='*60}")

            # Validar prompt
            print(f"✓ Validando estrutura do prompt...")
            is_valid, errors = validate_prompt(prompt_data)

            if not is_valid:
                print(f"❌ Validação falhou:")
                for error in errors:
                    print(f"   - {error}")
                fail_count += 1
                continue

            print(f"✅ Validação passou!")

            # Exibir resumo
            print(f"\n📋 Resumo do prompt:")
            print(f"   Descrição: {prompt_data.get('description', 'N/A')}")

            # Detectar formato para exibir informações corretas
            if "messages" in prompt_data:
                # Formato novo: messages
                metadata = prompt_data.get('metadata', {})
                version = metadata.get('version', prompt_data.get('version', 'N/A'))
                messages = prompt_data.get('messages', [])
                total_chars = sum(len(msg.get('content', '')) for msg in messages)

                print(f"   Versão: {version}")
                print(f"   Formato: Conversacional (messages)")
                print(f"   Total de mensagens: {len(messages)}")
                print(f"   Total de caracteres: {total_chars}")
            else:
                # Formato antigo: system_prompt
                version = prompt_data.get('version', 'N/A')
                system_prompt_len = len(prompt_data.get('system_prompt', ''))

                print(f"   Versão: {version}")
                print(f"   Formato: Legado (system_prompt)")
                print(f"   System prompt: {system_prompt_len} caracteres")

            # Fazer push
            if push_prompt_to_langsmith(prompt_name, prompt_data):
                success_count += 1
            else:
                fail_count += 1
    
    # Resumo final
    print(f"\n{'='*60}")
    print(f"📊 RESUMO FINAL")
    print(f"{'='*60}")
    print(f"✅ Sucesso: {success_count}")
    print(f"❌ Falhas: {fail_count}")
    print(f"📝 Total: {success_count + fail_count}")
    
    if fail_count > 0:
        print(f"\n⚠️  Alguns prompts falharam. Verifique os erros acima.")
        return 1
    
    print(f"\n🎉 Todos os prompts foram publicados com sucesso!")
    print(f"\n💡 Próximo passo: Execute 'python src/evaluate.py' para avaliar os prompts")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
