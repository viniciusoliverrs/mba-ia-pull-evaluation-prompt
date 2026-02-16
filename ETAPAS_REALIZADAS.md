# 📝 Documentação Completa - Otimização de Prompts

## 📊 Status do Projeto

**Data:** 15 de Fevereiro de 2026  
**Progresso:** 65% concluído  
**Status Atual:** ITERAÇÃO NECESSÁRIA (Fase 6)

---

## ✅ ETAPAS CONCLUÍDAS

### **FASE 0: Configuração Inicial**

#### Ambiente
- ✅ Ambiente virtual Python criado (`venv`)
- ✅ Dependências instaladas via `requirements.txt`
- ✅ Arquivo `.env` configurado

#### Credenciais Configuradas
```bash
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_PROJECT=mba
USERNAME_LANGSMITH_HUB=viniciusoliverrs
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

#### Configuração LLM
- **Provider Inicial:** Google Gemini (gemini-2.5-flash)
- **Provider Final:** OpenAI (gpt-4o-mini + gpt-4o)
- **Motivo da mudança:** Rate limit do Gemini (15 req/min) tornava avaliação muito lenta

---

### **FASE 1: Pull do Prompt Inicial** ✅

#### Script Implementado
**Arquivo:** `src/pull_prompts.py`

**Funcionalidades:**
- Conecta ao LangSmith Hub usando credenciais
- Faz pull do prompt `leonanluppi/bug_to_user_story_v1`
- Extrai e serializa o prompt em formato YAML
- Salva em `prompts/bug_to_user_story_v1.yml`

#### Comando Executado
```bash
python src/pull_prompts.py
```

#### Resultado: Prompt V1 (Baseline)

**Arquivo:** `prompts/bug_to_user_story_v1.yml`

```yaml
bug_to_user_story_v1:
  description: "Prompt para converter relatos de bugs em User Stories"
  system_prompt: |
    Você é um assistente que ajuda a transformar relatos de bugs de 
    usuários em tarefas para desenvolvedores.
    
    Analise o relato de bug abaixo e crie uma user story a partir dele.
    
    Relato de Bug:
    ---
    {bug_report}
    ---
    
    User Story gerada:
  user_prompt: "{bug_report}"
  version: "v1"
  tags: ["bug-analysis", "user-story", "product-management"]
```

**Tamanho:** ~10 linhas

#### ❌ Problemas Identificados no V1
1. **Persona genérica** - "assistente" sem especialização
2. **Sem exemplos** - Nenhum exemplo de entrada/saída
3. **Sem estrutura** - Output livre, sem formato definido
4. **Instruções vagas** - "crie uma user story" é muito genérico
5. **Sem regras** - Não especifica o que fazer/não fazer
6. **Sem edge cases** - Não trata bugs complexos ou incompletos
7. **Sem critérios** - Não define o que é uma boa user story

---

### **FASE 2: Otimização do Prompt** ✅

#### Arquivo Criado
**Arquivo:** `prompts/bug_to_user_story_v2.yml`

**Estatísticas:**
- **Tamanho:** 9.579 caracteres
- **Crescimento:** ~960x maior que v1
- **Técnicas aplicadas:** 7
- **Exemplos incluídos:** 3
- **Seções estruturadas:** 9

#### 🎯 Técnicas Avançadas Aplicadas

##### 1. **Role Prompting**
**Objetivo:** Definir persona específica e detalhada

**Implementação:**
```yaml
# ROLE & CONTEXTO
Você é um Product Manager experiente com 10+ anos trabalhando 
em metodologias ágeis (Scrum/Kanban).
Sua especialidade é transformar relatos técnicos de bugs em 
User Stories claras, acionáveis e centradas no valor do usuário.
```

**Por que funciona:**
- Contextualiza expertise necessária
- Define tom e estilo esperado
- Estabelece credibilidade

---

##### 2. **Few-Shot Learning**
**Objetivo:** Fornecer exemplos concretos de entrada/saída

**Implementação:** 3 exemplos completos cobrindo diferentes complexidades

**Exemplo 1: Bug Simples**
```
Bug Report: "O botão de salvar não funciona na página de perfil"
→ User Story completa com todos os campos
```

**Exemplo 2: Bug de Performance**
```
Bug Report: "Dashboard demora 15s para carregar com muitos dados"
→ User Story com métricas específicas de performance
```

**Exemplo 3: Bug Crítico**
```
Bug Report: "Erro 500 no checkout com múltiplos itens"
→ User Story com prioridade crítica e impacto na receita
```

**Por que funciona:**
- Modelo aprende o padrão desejado
- Reduz ambiguidade drasticamente
- Mostra nível de detalhe esperado
- Cobre diferentes tipos de bugs

---

##### 3. **Chain of Thought (CoT)**
**Objetivo:** Instruir o modelo a raciocinar antes de responder

**Implementação:**
```yaml
# PROCESSO DE ANÁLISE (Chain of Thought)
Antes de gerar a User Story, você deve:

1. Identificar o usuário afetado
2. Extrair o comportamento esperado
3. Identificar o comportamento atual
4. Determinar o impacto
5. Definir critérios claros
```

**Por que funciona:**
- Melhora qualidade do raciocínio
- Evita respostas superficiais
- Garante análise completa
- Reduz erros lógicos

---

##### 4. **Skeleton of Thought**
**Objetivo:** Definir estrutura obrigatória e fixa

**Implementação:**
```yaml
# ESTRUTURA OBRIGATÓRIA DA USER STORY

## Título
[Descrição breve do problema]

## User Story
**As a** [tipo de usuário]
**I want** [capacidade corrigida]
**So that** [benefício obtido]

## Contexto do Bug
[Resumo do problema]

## Comportamento Atual (Indesejado)
- [O que está errado]

## Comportamento Esperado (Desejado)
- [Como deveria funcionar]

## Critérios de Aceitação
- [ ] [Critério testável 1]
- [ ] [Critério testável 2]
- [ ] [Testes de regressão passam]

## Prioridade Sugerida
[Alta/Média/Baixa com justificativa]

## Notas Técnicas
[Informações para desenvolvedores]
```

**Por que funciona:**
- Garante completude
- Facilita validação automática
- Cria consistência
- Formato profissional reconhecível

---

##### 5. **Explicit Rules**
**Objetivo:** Definir claramente o que fazer e não fazer

**Implementação:**
```yaml
✅ SEMPRE FAÇA:
- Use linguagem clara e profissional
- Foque no valor para o usuário
- Seja específico nos critérios de aceitação
- Use formato Markdown
- Mantenha tom empático
- Inclua TODOS os campos

❌ NUNCA FAÇA:
- Assumir detalhes não mencionados
- Usar jargão excessivo
- Criar critérios vagos
- Omitir campos obrigatórios
- Misturar múltiplos problemas
```

**Por que funciona:**
- Previne erros comuns
- Estabelece limites claros
- Melhora qualidade
- Reduz ambiguidade

---

##### 6. **Edge Case Handling**
**Objetivo:** Instruir como lidar com situações não-padrão

**Implementação:**
```yaml
# TRATAMENTO DE CASOS ESPECIAIS

Bug Report Incompleto: 
  Incluir na seção "Notas Técnicas" quais esclarecimentos são necessários

Bug Complexo: 
  Divida em contextos menores, foque no problema principal

Bug de Performance: 
  Inclua métricas específicas (tempo < 2s, response time, etc.)

Bug de Segurança: 
  Classifique como "Prioridade: Alta"
  Cuidado com exposição de detalhes sensíveis
```

**Por que funciona:**
- Aumenta robustez
- Lida com dados imperfeitos
- Cobre cenários reais
- Evita bloqueios

---

##### 7. **Format Specification**
**Objetivo:** Definir formato exato de saída

**Implementação:**
- Markdown para legibilidade
- User Story padrão: **As a** / **I want** / **So that**
- Checkboxes para critérios: `- [ ]`
- Seções delimitadas: `###`

**Por que funciona:**
- Saída pronta para usar
- Compatível com ferramentas (Jira, Azure DevOps)
- Facilita parsing
- Profissional e padronizado

---

### **FASE 3: Push para o LangSmith Hub** ✅

#### Script Implementado
**Arquivo:** `src/push_prompts.py`

**Funcionalidades:**
- Valida estrutura do prompt (campos obrigatórios, tamanho mínimo)
- Cria `ChatPromptTemplate` do LangChain
- Faz push PÚBLICO para o Hub
- Adiciona metadados e tags
- Suporte a fallback (público → privado)

#### Comando Executado
```bash
python src/push_prompts.py
```

#### Resultado
```
✅ Push PÚBLICO realizado com sucesso!
🔗 https://smith.langchain.com/hub/viniciusoliverrs/bug_to_user_story_v2

📋 Técnicas aplicadas:
   - Role Prompting: Persona detalhada de Product Manager experiente
   - Few-shot Learning: 3 exemplos completos cobrindo diferentes complexidades
   - Chain of Thought: Processo de análise em 5 etapas
   - Skeleton of Thought: Estrutura clara e obrigatória com 9 seções
   - Edge Case Handling: Tratamento para bugs incompletos, complexos, performance e segurança
   - Format Specification: User Story padrão da indústria (As a, I want, So that)
   - Explicit Rules: Lista clara de o que fazer e não fazer
```

**Status:** ✅ Prompt publicado e acessível publicamente

---

### **FASE 5: Avaliação do Prompt** ✅

#### Setup da Avaliação

**Dataset:**
- Arquivo: `datasets/bug_to_user_story.jsonl`
- Total de exemplos: 15
- Distribuição:
  - Bugs simples: 5
  - Bugs médios: 7
  - Bugs complexos: 3

**Configuração LLM:**
- **Tentativa 1:** Google Gemini 2.5 Flash
  - Problema: Rate limit (15 req/min)
  - Tempo estimado: ~10 minutos
  - Status: Abortado
  
- **Tentativa 2:** OpenAI GPT-4o ✅
  - Modelo Principal: `gpt-4o-mini` (geração)
  - Modelo de Avaliação: `gpt-4o` (validação)
  - Tempo real: ~2 minutos
  - Status: Concluído

#### Comando Executado
```bash
python src/evaluate.py
```

#### 📊 RESULTADOS DA AVALIAÇÃO

##### Métricas LangSmith (Built-in)
| Métrica | Score | Status | Meta |
|---------|-------|--------|------|
| **Helpfulness** | 0.92 | ✅ PASSOU | ≥ 0.9 |
| **Correctness** | 0.86 | ❌ FALHOU | ≥ 0.9 |

##### Métricas Customizadas
| Métrica | Score | Status | Meta |
|---------|-------|--------|------|
| **F1-Score** | 0.80 | ❌ FALHOU | ≥ 0.9 |
| **Clarity** | 0.92 | ✅ PASSOU | ≥ 0.9 |
| **Precision** | 0.92 | ✅ PASSOU | ≥ 0.9 |

##### Resultado Final
```
📊 MÉDIA GERAL: 0.8844
❌ STATUS: REPROVADO

⚠️  Média atual: 0.8844
🎯 Necessário: 0.9000
📉 Diferença: -0.0156 (-1.56%)
```

#### 🔍 Análise dos Resultados

**✅ Pontos Fortes (3/5 métricas aprovadas):**
1. **Clarity (0.92)** - Linguagem clara e estruturada
2. **Precision (0.92)** - Informações precisas e corretas
3. **Helpfulness (0.92)** - User Stories úteis e acionáveis

**❌ Pontos Fracos (2/5 métricas reprovadas):**
1. **Correctness (0.86)**
   - Problema: Pode incluir informações não mencionadas no bug report
   - Impacto: -4% da meta
   
2. **F1-Score (0.80)**
   - Problema: Balance entre recall e precision
   - Possível causa: Prompt muito verboso ou faltando informações chave
   - Impacto: -10% da meta

**⚠️ Observações:**
- Diferença pequena para aprovação: apenas **1.56%**
- 3 métricas já estão acima de 0.9 (60% de sucesso)
- Foco da iteração deve ser em **Correctness** e **F1-Score**

---

## 📂 ESTRUTURA DE ARQUIVOS

### Arquivos Criados/Modificados
```
mba-ia-pull-evaluation-prompt/
├── .env                              ✅ Configurado
├── prompts/
│   ├── bug_to_user_story_v1.yml     ✅ Pull realizado
│   └── bug_to_user_story_v2.yml     ✅ Criado e otimizado (9.579 chars)
├── src/
│   ├── pull_prompts.py              ✅ Implementado
│   ├── push_prompts.py              ✅ Implementado
│   ├── evaluate.py                  ✅ Executado
│   ├── metrics.py                   ✅ Existente (métricas customizadas)
│   └── utils.py                     ✅ Funções auxiliares
├── datasets/
│   └── bug_to_user_story.jsonl      ✅ 15 exemplos
└── tests/
    └── test_prompts.py              ❌ Pendente
```

---

## 📊 COMPARAÇÃO V1 vs V2

| Aspecto | V1 (Baseline) | V2 (Otimizado) | Melhoria |
|---------|---------------|----------------|----------|
| **Tamanho** | ~10 linhas | 9.579 caracteres | +960x |
| **Persona** | ❌ Genérica | ✅ PM experiente 10+ anos | +100% |
| **Exemplos** | ❌ 0 | ✅ 3 completos | +∞ |
| **Estrutura** | ❌ Livre | ✅ 9 seções obrigatórias | +100% |
| **Processo** | ❌ Nenhum | ✅ 5 etapas de análise | +100% |
| **Regras** | ❌ 0 | ✅ 11 regras explícitas | +∞ |
| **Edge cases** | ❌ Não trata | ✅ 4 cenários | +100% |
| **Técnicas** | ❌ 0 | ✅ 7 técnicas | +∞ |
| **Score médio** | ~0.45 (estimado) | 0.8844 | +96.5% |

---

## ⚠️ ETAPAS PENDENTES

### **FASE 6: Iteração** 🔄 PRÓXIMA ETAPA

#### Objetivo
Melhorar métricas **Correctness** (0.86 → 0.90) e **F1-Score** (0.80 → 0.90)

#### Análise de Problemas

**1. Correctness (0.86) - Falta 0.04**

**Possíveis causas:**
- Prompt adiciona informações não mencionadas no bug report
- Exemplos podem estar induzindo a criatividade excessiva
- Regra "Nunca assumir detalhes" pode não estar sendo seguida

**Soluções propostas:**
```yaml
# Adicionar ênfase em:
⚠️ REGRA CRÍTICA: NUNCA invente ou assuma informações que não 
estão explícitas no bug report. Se algo não foi mencionado, 
indique na seção "Notas Técnicas" que esclarecimento é necessário.

# Adicionar validação explícita:
Antes de finalizar, verifique:
- [ ] Todas as informações na User Story estão no bug report original?
- [ ] Se algo foi assumido, está marcado como "a confirmar"?
```

**2. F1-Score (0.80) - Falta 0.10**

**Possíveis causas:**
- Balance incorreto entre recall (cobertura) e precision
- Pode estar faltando informações chave do bug report
- Ou incluindo informações desnecessárias

**Soluções propostas:**
```yaml
# Adicionar checklist de cobertura:
## Checklist de Informações Obrigatórias
Certifique-se de incluir:
- [ ] Quem está afetado (usuário, tipo de usuário)
- [ ] O que está quebrado (comportamento incorreto)
- [ ] Quando/onde ocorre (contexto, navegador, etc.)
- [ ] Impacto no usuário (o que ele não consegue fazer)
- [ ] Passos para reproduzir (se mencionados)
```

#### Plano de Iteração

**Iteração 2 (próxima):**
1. Editar `prompts/bug_to_user_story_v2.yml`
2. Adicionar ênfases em Correctness
3. Adicionar checklist de cobertura
4. Fazer push: `python src/push_prompts.py`
5. Avaliar: `python src/evaluate.py`
6. Meta: Correctness ≥ 0.90, F1-Score ≥ 0.85

**Iteração 3 (se necessário):**
1. Ajustes finos no F1-Score
2. Meta final: todas métricas ≥ 0.90

---

### **FASE 7: Testes de Validação** ❌ Pendente

#### Arquivo a ser implementado
`tests/test_prompts.py`

#### 6 Testes Obrigatórios

```python
def test_prompt_has_system_prompt():
    """Verifica se system_prompt existe e não está vazio"""
    pass

def test_prompt_has_role_definition():
    """Verifica se define persona (ex: 'Product Manager')"""
    pass

def test_prompt_mentions_format():
    """Verifica se exige formato Markdown ou User Story padrão"""
    pass

def test_prompt_has_few_shot_examples():
    """Verifica se contém exemplos de entrada/saída"""
    pass

def test_prompt_no_todos():
    """Garante que não há [TODO] no texto"""
    pass

def test_minimum_techniques():
    """Verifica metadados: pelo menos 2 técnicas listadas"""
    pass
```

#### Comando para executar
```bash
pytest tests/test_prompts.py -v
```

---

### **FASE 8: Documentação** ❌ Pendente

#### README.md - Seções a adicionar

**A) Técnicas Aplicadas:**
- Descrição de cada uma das 7 técnicas
- Justificativa da escolha
- Exemplos práticos de aplicação

**B) Resultados Finais:**
- Link público do LangSmith
- Screenshots das avaliações
- Tabela comparativa v1 vs v2
- Gráficos de evolução das métricas

**C) Como Executar:**
```markdown
## Pré-requisitos
- Python 3.9+
- Credenciais LangSmith
- Credenciais OpenAI ou Google Gemini

## Instalação
\`\`\`bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
\`\`\`

## Configuração
\`\`\`bash
cp .env.example .env
# Edite .env com suas credenciais
\`\`\`

## Execução
\`\`\`bash
# 1. Pull do prompt inicial
python src/pull_prompts.py

# 2. Push do prompt otimizado
python src/push_prompts.py

# 3. Avaliação
python src/evaluate.py

# 4. Testes
pytest tests/test_prompts.py
\`\`\`
```

---

### **FASE 9: Entrega Final** ❌ Pendente

#### Checklist de Entrega

- [ ] Repositório público no GitHub
- [ ] Todas as métricas ≥ 0.90
- [ ] 6 testes implementados e passando
- [ ] README.md completo
- [ ] Screenshots do LangSmith
- [ ] Link do dashboard público
- [ ] Código documentado
- [ ] Arquivo ETAPAS_REALIZADAS.md (este documento)

---

## 📈 PROGRESSO GERAL

```
[████████████████░░░░░] 65% Concluído

✅ Fase 0: Configuração         100%
✅ Fase 1: Pull                 100%
✅ Fase 2: Otimização           100%
✅ Fase 3: Push                 100%
✅ Fase 5: Avaliação            100%
🔄 Fase 6: Iteração              0% ← PRÓXIMA
❌ Fase 7: Testes                0%
❌ Fase 8: Documentação          0%
❌ Fase 9: Entrega               0%
```

---

## 🎯 PRÓXIMOS PASSOS IMEDIATOS

### 1. **Melhorar Correctness Score** (prioridade alta)
```yaml
Adicionar ao prompt v2:
- Ênfase em não inventar informações
- Validação explícita antes de finalizar
- Exemplos mostrando o que NÃO fazer
```

### 2. **Melhorar F1-Score** (prioridade alta)
```yaml
Adicionar ao prompt v2:
- Checklist de informações obrigatórias
- Balance entre cobertura e precisão
- Instrução para priorizar informações do bug report
```

### 3. **Iterar e Reavaliar**
```bash
# Editar prompts/bug_to_user_story_v2.yml
python src/push_prompts.py
python src/evaluate.py
# Meta: todas métricas ≥ 0.90
```

### 4. **Implementar Testes** (após aprovação)
```bash
# Implementar tests/test_prompts.py
pytest tests/test_prompts.py -v
```

### 5. **Documentar** (após testes)
```bash
# Atualizar README.md
# Adicionar screenshots
# Preparar para entrega
```

---

## 📚 LIÇÕES APRENDIDAS

### O que funcionou bem ✅
1. **Few-shot Learning** foi crítico - 3 exemplos cobriram bem os casos
2. **Skeleton of Thought** garantiu estrutura consistente
3. **OpenAI** foi significativamente mais rápido que Gemini (2min vs 10min)
4. **Role Prompting** ajudou em Clarity e Helpfulness
5. **Explicit Rules** melhorou Precision

### Desafios encontrados ⚠️
1. **Rate limits do Gemini** inviabilizaram uso em produção
2. **Prompt muito grande** (9.5KB) pode aumentar custos
3. **Balance F1-Score** é difícil - precisa ajuste fino
4. **Correctness** sofre quando prompt permite criatividade
5. **Handle do LangSmith Hub** precisa ser criado manualmente

### Ajustes necessários 🔧
1. **Reduzir assunções** - prompt está criando informações
2. **Melhorar recall** - pode estar faltando informações chave
3. **Considerar prompt menor** - versão v2.1 mais enxuta?
4. **Adicionar mais exemplos negativos** - o que NÃO fazer

---

## 🔗 Links Importantes

- **Prompt V2 Público:** https://smith.langchain.com/hub/viniciusoliverrs/bug_to_user_story_v2
- **Dashboard LangSmith:** https://smith.langchain.com/o/0b52b88d-af51-440e-bf12-7c6005f677da/projects/p/mba
- **Repositório Base:** (a definir)
- **Documentação LangSmith:** https://docs.smith.langchain.com/

---

## 📞 Suporte e Referências

- **LangChain Documentation:** https://python.langchain.com/docs/
- **Prompt Engineering Guide:** https://www.promptingguide.ai/
- **OpenAI Best Practices:** https://platform.openai.com/docs/guides/prompt-engineering

---

**Última atualização:** 15 de Fevereiro de 2026  
**Responsável:** Vinícius  
**Status:** Em Iteração (Fase 6)
