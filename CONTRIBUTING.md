# Guia de Contribuição

Obrigado por considerar contribuir para o Extrator XML Fiscal! Sua contribuição é muito valiosa para melhorar este projeto.

## Como Contribuir

### Reportando Bugs

Antes de reportar um bug, verifique se ele já não foi reportado nas [Issues](https://github.com/luizelias8/extrator-xml-fiscal/issues). Se não encontrar, crie uma nova issue incluindo:

- **Título claro**: Descreva o problema de forma concisa
- **Descrição detalhada**: Explique o que aconteceu e o que era esperado
- **Passos para reproduzir**: Liste os passos exatos para reproduzir o problema
- **Ambiente**: Versão do Python, sistema operacional, versão do pacote
- **Exemplo de código**: Se possível, inclua um exemplo mínimo que reproduza o problema
- **Arquivo XML**: Se o problema for específico de um XML, considere incluir um exemplo (removendo dados sensíveis)

### Sugerindo Melhorias

Para sugerir melhorias ou novas funcionalidades:

- Verifique se a sugestão já não existe nas Issues
- Crie uma nova issue com tag `enhancement`
- Descreva claramente o que você gostaria de ver implementado
- Explique por que essa funcionalidade seria útil
- Se possível, sugira uma implementação

### Contribuindo com Código

#### 1. Fork e Clone

```bash
# Fork o repositório no GitHub
# Clone seu fork localmente
git clone https://github.com/seu-usuario/extrator-xml-fiscal.git
cd extrator-xml-fiscal
```

#### 2. Configure o Ambiente de Desenvolvimento

```bash
# Instale Poetry se não tiver
pip install poetry

# Instale as dependências de desenvolvimento
poetry install

# Ative o ambiente virtual
poetry shell
```

#### 3. Configure o Git

```bash
# Configure seu nome e email
git config user.name "Seu Nome"
git config user.email "seu.email@exemplo.com"

# Adicione o repositório upstream
git remote add upstream https://github.com/luizelias8/extrator-xml-fiscal.git
```

#### 4. Crie uma Branch

```bash
# Atualize main com as últimas mudanças
git checkout main
git pull upstream main

# Crie uma nova branch para sua contribuição
git checkout -b feature/nome-da-feature
# ou
git checkout -b fix/nome-do-bug
```

#### 5. Faça suas Alterações

- Siga os padrões de código existentes
- Adicione docstrings para funções e classes
- Comente código complexo
- Mantenha commits pequenos e focados

#### 6. Commit e Push

```bash
# Adicione os arquivos modificados
git add .

# Faça commit com mensagem descritiva
git commit -m "feat: adiciona suporte para CTe"

# Faça push da branch
git push origin feature/nome-da-feature
```

#### 7. Crie um Pull Request

- Vá para seu fork no GitHub
- Clique em "New Pull Request"
- Selecione sua branch
- Preencha o template do PR (se existir)
- Descreva claramente as mudanças feitas

## Padrões de Código

### Estilo de Código

- Siga as convenções PEP 8
- Use type hints sempre que possível
- Nomes de variáveis e funções em português (seguindo o padrão do projeto)
- Nomes de classes em PascalCase
- Nomes de funções e variáveis em snake_case

### Estrutura de Commits

Use a convenção de commits semânticos:

- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Mudanças na documentação
- `style:` Mudanças de formatação (sem afetar a lógica)
- `refactor:` Refatoração de código
- `test:` Adição ou modificação de testes
- `chore:` Tarefas de manutenção

### Docstrings

Use o formato Google/Sphinx para docstrings:

```python
def extrair_dados(self, dados_xml: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extrai dados específicos do documento fiscal.

    Args:
        dados_xml (Dict[str, Any]): XML convertido para dicionário

    Returns:
        Dict[str, Any]: Dados estruturados extraídos

    Raises:
        ValueError: Se a estrutura XML for inválida
        KeyError: Se campos obrigatórios estiverem ausentes
    """
```

## Adicionando Suporte para Novos Documentos

Para adicionar suporte a um novo tipo de documento fiscal (ex: CTe, NFCe):

### 1. Crie uma nova classe extratora

```python
# extrator_cte.py
from .extrator_base import ExtratorBase

class ExtratorCTe(ExtratorBase):
    """
    Extrator específico para Conhecimento de Transporte Eletrônico (CTe).
    """

    def _extrair_dados(self, dados_xml: Dict[str, Any]) -> Dict[str, Any]:
        # Implementar extração específica
        pass
```

### 2. Implemente os métodos necessários

- `_encontrar_raiz()`: Localiza a estrutura principal do documento
- `_extrair_dados()`: Extrai todos os dados relevantes
- Métodos auxiliares específicos do documento

### 3. Adicione utilitários se necessário

Se precisar de novas funções utilitárias, adicione em `utils.py`.

### 4. Atualize a documentação

- Adicione exemplos de uso no README.md
- Documente campos suportados
- Inclua na seção de roadmap se aplicável

## Dependências

### Adicionando Novas Dependências

```bash
# Para dependências de produção
poetry add nome-da-biblioteca

# Para dependências de desenvolvimento
poetry add --dev nome-da-biblioteca-dev
```

### Atualizando Dependências

```bash
# Atualizar todas as dependências
poetry update

# Atualizar dependência específica
poetry update nome-da-biblioteca
```

## Diretrizes Gerais

- **Seja respeitoso**: Trate todos os colaboradores com respeito
- **Seja paciente**: Reviews podem demorar, especialmente para mudanças grandes
- **Seja claro**: Descreva bem suas mudanças e o motivo delas
- **Seja consistente**: Siga os padrões existentes no projeto
- **Teste suas mudanças**: Certifique-se de que tudo funciona antes do PR

## Dúvidas?

- Abra uma Issue para perguntas sobre desenvolvimento
- Entre em contato via email: luizelias8@gmail.com
- Consulte a documentação existente no código

Obrigado por ajudar a tornar o Extrator XML Fiscal ainda melhor! 🚀
