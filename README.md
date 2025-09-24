# Extrator XML Fiscal

Um pacote Python para extração de dados de documentos fiscais eletrônicos brasileiros (NFe) em formato XML.

## Instalação

### Via Poetry (Recomendado)

```bash
# Clone o repositório
git clone https://github.com/luizelias8/extrator-xml-fiscal.git
cd extrator-xml-fiscal

# Instale as dependências
poetry install

# Ative o ambiente virtual
poetry shell
```

### Via pip

```bash
# Clone o repositório
git clone https://github.com/luizelias8/extrator-xml-fiscal.git
cd extrator-xml-fiscal

# Instale o pacote em modo de desenvolvimento
pip install -e .
```

### Dependências

- Python 3.13+
- xmltodict 1.0.2+

## Uso Básico

### Extraindo dados de uma NFe

```python
from extrator_xml_fiscal import ExtratorNFe

# Inicialize o extrator
extrator = ExtratorNFe()

# Processe o arquivo XML
dados = extrator.processar_arquivo('caminho/para/nfe.xml')

# Acesse os dados extraídos
print(f"Número da NF: {dados['identificacao']['numero_nf']}")
print(f"Emitente: {dados['emitente']['razao_social']}")
print(f"Valor total: {dados['totais']['valor_total_nota_fiscal']}")

# Iterate sobre os produtos
for produto in dados['produtos']:
    print(f"Produto: {produto['descricao_produto']} - Valor: {produto['valor_total_bruto']}")
```

### Estrutura dos dados extraídos

```python
{
    'arquivo_origem': '/caminho/para/arquivo.xml',
    'processado_em': '2024-01-15T10:30:45.123456',
    'tipo_documento': 'NFE',
    'identificacao': {
        'chave_acesso': '35200114200166000187550010000000046',
        'numero_nf': '46',
        'serie': '1',
        'data_emissao': '2024-01-15T10:30:00',
        # ... outros campos
    },
    'emitente': {
        'razao_social': 'Empresa Emitente LTDA',
        'cnpj': '14200166000187',
        'endereco': {
            'logradouro': 'Rua das Empresas, 123',
            'municipio': 'São Paulo',
            # ... outros campos
        }
    },
    'destinatario': { /* ... */ },
    'produtos': [
        {
            'descricao_produto': 'Produto A',
            'valor_total_bruto': '100.00',
            'impostos': {
                'icms': { /* ... */ },
                'ipi': { /* ... */ }
            }
        }
        # ... outros produtos
    ],
    'totais': {
        'valor_total_nota_fiscal': '1000.00',
        'valor_total_produtos': '900.00',
        # ... outros totais
    }
}
```

## Campos Suportados

### NFe (Nota Fiscal Eletrônica)

- **Identificação**: Chave de acesso, número, série, datas, tipo de operação, etc.
- **Emitente**: Dados completos incluindo endereço e identificação fiscal
- **Destinatário**: Dados completos incluindo endereço e identificação fiscal
- **Produtos/Serviços**: Descrição, valores, impostos, produtos específicos (veículos, medicamentos, combustíveis, armamentos)
- **Impostos**: ICMS, IPI, PIS, COFINS, II, Imposto Seletivo, IBS/CBS
- **Transporte**: Dados da transportadora e volumes
- **Totais**: Todos os valores totalizadores da nota
- **Informações Adicionais**: Informações complementares e do fisco

## Extensibilidade

Para criar um extrator para outros tipos de documentos fiscais:

```python
from extrator_xml_fiscal import ExtratorBase

class ExtratorCTe(ExtratorBase):
    def _extrair_dados(self, dados_xml):
        # Implementar extração específica do CTe
        return dados_estruturados
```

## Tratamento de Erros

O extrator trata automaticamente os seguintes cenários:
- Arquivo não encontrado
- XML malformado
- Estrutura XML inválida
- Campos opcionais ausentes
- Normalização de listas/dicionários

## Contribuindo

Contribuições são bem-vindas! Por favor, leia nosso [guia de contribuição](CONTRIBUTING.md) para mais detalhes sobre como contribuir para este projeto.
