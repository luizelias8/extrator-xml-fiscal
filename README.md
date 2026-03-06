# Extrator XML Fiscal

Um pacote Python para extração de dados de **documentos fiscais eletrônicos** brasileiros (NFe, CTe) e seus **eventos associados** em formato XML.

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

# Itere sobre os produtos
for produto in dados['produtos']:
    print(f"Produto: {produto['descricao_produto']} - Valor: {produto['valor_total_bruto']}")
```

### Estrutura dos dados extraídos (NFe)

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

---

### Extraindo dados de um Cancelamento de NFe

```python
from extrator_xml_fiscal import ExtratorCancelamento

# Inicialize o extrator
extrator = ExtratorCancelamento()

# Processe o arquivo XML de cancelamento
dados = extrator.processar_arquivo('caminho/para/cancelamento.xml')

# Acesse os dados extraídos
print(f"Chave da NFe: {dados['dados_evento']['chave_nfe']}")
print(f"Descrição do evento: {dados['dados_especificos']['descricao_evento']}")
print(f"Justificativa: {dados['dados_especificos']['justificativa']}")
print(f"Protocolo: {dados['dados_especificos']['numero_protocolo_nfe']}")
```

### Estrutura dos dados extraídos (Cancelamento)

```python
{
    'arquivo_origem': '/caminho/para/cancelamento.xml',
    'processado_em': '2024-01-15T11:45:12.123456',
    'tipo_documento': 'EVENTO',
    'dados_evento': {
        'id_evento': 'ID110111352001142001660001875500100000000461234567890',
        'codigo_orgao': '35',
        'ambiente': '1',
        'cnpj_emissor': '14200166000187',
        'chave_nfe': '35200114200166000187550010000000046',
        'data_evento': '2024-01-15T11:40:00',
        'tipo_evento': '110111',
        'numero_sequencia': '1',
        'versao_evento': '1.00'
    },
    'dados_protocolo': {
        'ambiente_protocolo': '1',
        'codigo_status': '135',
        'motivo': 'Evento registrado e vinculado a NFe',
        'numero_protocolo': '135240000123456'
    },
    'dados_especificos': {
        'descricao_evento': 'Cancelamento',
        'numero_protocolo_nfe': '135240000123456',
        'justificativa': 'Erro de emissão da nota',
        'versao_layout': '1.00'
    }
}
```

---

### Extraindo dados de uma Carta de Correção (CCe)

```python
from extrator_xml_fiscal import ExtratorCartaCorrecao

# Inicialize o extrator
extrator = ExtratorCartaCorrecao()

# Processe o arquivo XML de CCe
dados = extrator.processar_arquivo('caminho/para/cce.xml')

# Acesse os dados extraídos
print(f"Chave da NFe: {dados['dados_evento']['chave_nfe']}")
print(f"Descrição do evento: {dados['dados_especificos']['descricao_evento']}")
print(f"Texto da correção: {dados['dados_especificos']['texto_correcao']}")
print(f"Condições de uso: {dados['dados_especificos']['condicoes_uso']}")
```

### Estrutura dos dados extraídos (CCe)

```python
{
    'arquivo_origem': '/caminho/para/cce.xml',
    'processado_em': '2024-01-15T12:00:00.123456',
    'tipo_documento': 'EVENTO',
    'dados_evento': {
        'id_evento': 'ID110110352001142001660001875500100000000461234567890',
        'codigo_orgao': '35',
        'ambiente': '1',
        'cnpj_emissor': '14200166000187',
        'chave_nfe': '35200114200166000187550010000000046',
        'data_evento': '2024-01-15T11:50:00',
        'tipo_evento': '110110',
        'numero_sequencia': '1',
        'versao_evento': '1.00'
    },
    'dados_protocolo': {
        'ambiente_protocolo': '1',
        'codigo_status': '135',
        'motivo': 'Evento registrado e vinculado a NFe',
        'numero_protocolo': '135240000654321'
    },
    'dados_especificos': {
        'descricao_evento': 'Carta de Correcao',
        'texto_correcao': 'Correção do CFOP informado incorretamente',
        'condicoes_uso': 'A Carta de Correção não pode ser utilizada para corrigir valores fiscais',
        'versao_layout': '1.00'
    }
}
```

---

### Extraindo dados de um CTe

```python
from extrator_xml_fiscal import ExtratorCTe

# Inicialize o extrator
extrator = ExtratorCTe()

# Processe o arquivo XML de CTe
dados = extrator.processar_arquivo('caminho/para/cte.xml')

# Acesse os dados extraídos
print(f"Chave do CTe: {dados['identificacao']['chave_acesso']}")
print(f"Emitente: {dados['emitente']['razao_social']}")
print(f"Valor total da prestação: {dados['valores_prestacao']['valor_total_prestacao']}")
```

### Estrutura dos dados extraídos (CTe)

```python
{
    'arquivo_origem': '/caminho/para/cte.xml',
    'processado_em': '2024-01-15T12:15:00.123456',
    'tipo_documento': 'CTE',
    'identificacao': {
        'chave_acesso': '35200114200166000187570010000000046',
        'numero_ct': '123',
        'serie': '1',
        'data_emissao': '2024-01-15T12:00:00',
        'modal': '01',
        'tipo_servico': '0',
        'municipio_inicio': 'São Paulo',
        'municipio_fim': 'Rio de Janeiro',
        # ... outros campos
    },
    'emitente': {
        'razao_social': 'Transportadora LTDA',
        'cnpj': '14200166000187',
        'endereco': { /* ... */ }
    },
    'remetente': { /* ... */ },
    'destinatario': { /* ... */ },
    'valores_prestacao': {
        'valor_total_prestacao': '1500.00',
        'valor_receber': '1500.00',
        'componentes': [
            {'nome': 'Frete peso', 'valor': '1200.00'},
            {'nome': 'Pedágio', 'valor': '300.00'}
        ]
    },
    'impostos': {
        'valor_total_tributos': '200.00',
        'icms': { /* ... */ }
    },
    'informacoes_carga': {
        'valor_carga': '50000.00',
        'produto_predominante': 'Eletrodomésticos',
        'quantidades': [
            {'codigo_unidade': '01', 'tipo_medida': 'KG', 'quantidade': '5000'}
        ]
    },
    'informacoes_documentos': { /* ... */ },
    'informacoes_modais': {
        'rodoviario': { /* ... */ }
    },
    'complementares': { /* ... */ },
    'responsavel_tecnico': { /* ... */ }
}
```

---

### Extraindo dados de um evento CT-e Autorizado

```python
from extrator_xml_fiscal import ExtratorCTeAutorizado

extrator = ExtratorCTeAutorizado()
dados = extrator.processar_arquivo('caminho/para/cte_autorizado.xml')

print(f"Chave da NFe: {dados['dados_evento']['chave_nfe']}")
print(f"Chave do CTe: {dados['dados_especificos']['cte']['chave_cte']}")
print(f"Transportadora: {dados['dados_especificos']['emitente_cte']['razao_social']}")
print(f"Protocolo do CTe: {dados['dados_especificos']['cte']['numero_protocolo']}")
```

### Estrutura dos dados extraídos (CT-e Autorizado)

```python
{
    'arquivo_origem': '/caminho/para/cte_autorizado.xml',
    'processado_em': '2026-01-02T11:54:19.123456',
    'tipo_documento': 'CTEAUTORIZADO',
    'dados_evento': {
        'id_evento': 'ID6106002626010000351600027055006000017876150987331901',
        'codigo_orgao': '91',
        'ambiente': '1',
        'cnpj_emissor': '33683111000107',
        'chave_nfe': '26260100003516000270550060000178761509873319',
        'data_evento': '2026-01-02T11:54:19-03:00',
        'tipo_evento': '610600',
        'numero_sequencia': '1',
        'versao_evento': '1.00'
    },
    'dados_protocolo': {
        'ambiente_protocolo': '1',
        'versao_aplicativo': 'AN_1.6.4',
        'codigo_orgao': '91',
        'codigo_status': '135',
        'motivo': 'Evento registrado e vinculado a NF-e',
        'chave_nfe': '26260100003516000270550060000178761509873319',
        'tipo_evento': '610600',
        'numero_sequencia': '1',
        'data_registro': '2026-01-02T11:54:19-03:00',
        'numero_protocolo': '891260021945661',
        'cnpj_destinatario': '33683111000107'  # campo adicional
    },
    'dados_especificos': {
        'descricao_evento': 'CT-e Autorizado',
        'versao_layout': '1.00',
        'cte': {
            'chave_cte': '41260159197158000146570010000017931000028865',
            'modal': '01',
            'data_emissao': '2026-01-02T11:21:19-03:00',
            'numero_protocolo': '141260000476508',
            'data_recebimento': '2026-01-02T11:21:20'
        },
        'emitente_cte': {
            'cnpj': '59197158000146',
            'inscricao_estadual': '9112272906',
            'razao_social': 'TRANSPORTE EXPRESSO PHL LTDA'
        }
    }
}
```

---

### Extraindo dados de um evento Registro de Passagem de NFe

```python
from extrator_xml_fiscal import ExtratorRegistroPassagem

extrator = ExtratorRegistroPassagem()
dados = extrator.processar_arquivo('caminho/para/registro_passagem.xml')

print(f"Chave da NFe: {dados['dados_evento']['chave_nfe']}")
print(f"Posto fiscal: {dados['dados_especificos']['posto_fiscal']['nome_posto']}")
print(f"Operador: {dados['dados_especificos']['operador']['nome']}")
print(f"Data da passagem: {dados['dados_especificos']['passagem']['data_passagem']}")
print(f"Placa do veículo: {dados['dados_especificos']['veiculo']['placa']}")
```

### Estrutura dos dados extraídos (Registro de Passagem de NFe)

```python
{
    'arquivo_origem': '/caminho/para/registro_passagem.xml',
    'processado_em': '2026-01-05T06:34:01.123456',
    'tipo_documento': 'REGISTROPASSAGEM',
    'dados_evento': {
        'id_evento': 'ID6105002626010000351600027055006000017880173763418401',
        'codigo_orgao': '91',
        'ambiente': '1',
        'cnpj_emissor': '12200192000169',
        'chave_nfe': '26260100003516000270550060000178801737634184',
        'data_evento': '2026-01-05T06:34:01-03:00',
        'tipo_evento': '610500',
        'numero_sequencia': '1',
        'versao_evento': '1.00'
    },
    'dados_protocolo': { /* ... */ },
    'dados_especificos': {
        'descricao_evento': 'Registro Passagem NFe',
        'versao_layout': '1.00',
        'posto_fiscal': {
            'codigo_orgao_autor': '27',
            'codigo_posto': '0001',
            'nome_posto': 'NOVOLINO'
        },
        'operador': {
            'cpf': '65724780410',
            'nome': 'REJANE MARIA DA SILVA'
        },
        'passagem': {
            'data_passagem': '2026-01-05T06:33:01-03:00',
            'offline': '1',       # 1 = offline, 0 = online
            'sentido_via': 'I',   # I = entrada, S = saída
            'indicador_retorno': 'R'
        },
        'veiculo': {
            'placa': 'SOZ6E10',
            'uf': 'PE'
        }
    }
}
```

---

### Extraindo dados de eventos de Manifestação do Destinatário

O pacote suporta os quatro tipos de manifestação do destinatário. Cada um possui sua própria classe extratora.

#### Confirmação da Operação (210200)

```python
from extrator_xml_fiscal import ExtratorConfirmacaoOperacao

extrator = ExtratorConfirmacaoOperacao()
dados = extrator.processar_arquivo('caminho/para/confirmacao_operacao.xml')

print(f"Chave da NFe: {dados['dados_evento']['chave_nfe']}")
print(f"Descrição: {dados['dados_especificos']['descricao_evento']}")
print(f"Protocolo: {dados['dados_protocolo']['numero_protocolo']}")
```

#### Ciência da Operação (210210)

```python
from extrator_xml_fiscal import ExtratorCienciaOperacao

extrator = ExtratorCienciaOperacao()
dados = extrator.processar_arquivo('caminho/para/ciencia_operacao.xml')

print(f"Chave da NFe: {dados['dados_evento']['chave_nfe']}")
print(f"Descrição: {dados['dados_especificos']['descricao_evento']}")
print(f"Protocolo: {dados['dados_protocolo']['numero_protocolo']}")
```

#### Desconhecimento da Operação (210220)

```python
from extrator_xml_fiscal import ExtratorDesconhecimentoOperacao

extrator = ExtratorDesconhecimentoOperacao()
dados = extrator.processar_arquivo('caminho/para/desconhecimento_operacao.xml')

print(f"Chave da NFe: {dados['dados_evento']['chave_nfe']}")
print(f"Descrição: {dados['dados_especificos']['descricao_evento']}")
print(f"Protocolo: {dados['dados_protocolo']['numero_protocolo']}")
```

#### Operação não Realizada (210240)

```python
from extrator_xml_fiscal import ExtratorOperacaoNaoRealizada

extrator = ExtratorOperacaoNaoRealizada()
dados = extrator.processar_arquivo('caminho/para/operacao_nao_realizada.xml')

print(f"Chave da NFe: {dados['dados_evento']['chave_nfe']}")
print(f"Descrição: {dados['dados_especificos']['descricao_evento']}")
print(f"Justificativa: {dados['dados_especificos']['justificativa']}")
print(f"Protocolo: {dados['dados_protocolo']['numero_protocolo']}")
```

### Estrutura dos dados extraídos (Manifestação do Destinatário)

A estrutura é comum a todos os tipos de manifestação. A diferença está nos `dados_especificos`, onde apenas a Operação não Realizada possui o campo `justificativa`.

```python
{
    'arquivo_origem': '/caminho/para/confirmacao_operacao.xml',
    'processado_em': '2024-01-15T13:00:00.123456',
    'tipo_documento': 'CONFIRMACAOOPERACAO',  # varia conforme o tipo
    'dados_evento': {
        'id_evento': 'ID210200262601000035160002705500600001787714895943010',
        'codigo_orgao': '91',
        'ambiente': '1',
        'cnpj_emissor': '10656452007001',
        'chave_nfe': '26260100003516000270550060000178771489594301',
        'data_evento': '2026-01-14T11:48:16-03:00',
        'tipo_evento': '210200',
        'numero_sequencia': '1',
        'versao_evento': '1.00'
    },
    'dados_protocolo': {
        'ambiente_protocolo': '1',
        'versao_aplicativo': 'AN_1.8.7',
        'codigo_orgao': '91',
        'codigo_status': '135',
        'motivo': 'Evento registrado e vinculado a NF-e',
        'chave_nfe': '26260100003516000270550060000178771489594301',
        'tipo_evento': '210200',
        'numero_sequencia': '1',
        'data_registro': '2026-01-14T11:48:16-03:00',
        'numero_protocolo': '891260595761963',
        'descricao_evento': 'Confirmacao da Operacao',  # campo adicional
        'cnpj_destinatario': '10656452007001'           # campo adicional
    },
    'dados_especificos': {
        'descricao_evento': 'Confirmacao da Operacao',
        'versao_layout': '1.00'
        # apenas ExtratorOperacaoNaoRealizada inclui 'justificativa' aqui
    }
}
```

---

## Campos Suportados

### Documentos

- **NFe (Nota Fiscal Eletrônica)**
  - Identificação, emitente, destinatário, produtos/serviços, impostos, transporte, totais, informações adicionais

- **CTe (Conhecimento de Transporte Eletrônico)**
  - Identificação: chave de acesso, série, número, datas, tipo de serviço, modais, origem/destino
  - Emitente, remetente, expedidor, recebedor, destinatário
  - Valores da prestação: valor total, valor a receber, componentes
  - Impostos: ICMS, ICMS partilha UF destino, valor total de tributos
  - Informações da carga: produto predominante, valor da carga, quantidades
  - Documentos relacionados: NFes, NFs modelo 1/1A, outros documentos
  - Informações modais: rodoviário, aéreo, aquaviário, ferroviário, dutoviário
  - Informações complementares e observações
  - Responsável técnico

### Eventos

- **Cancelamento (110111)**
- **Carta de Correção (110110)**
- **CT-e Autorizado (610600)**
- **Registro de Passagem de NFe (610500)**
- **Confirmação da Operação (210200)**
- **Ciência da Operação (210210)**
- **Desconhecimento da Operação (210220)**
- **Operação não Realizada (210240)**

---

## Tratamento de Erros

O extrator trata automaticamente os seguintes cenários:
- Arquivo não encontrado
- XML malformado
- Estrutura XML inválida
- Tipo de evento incompatível com o extrator utilizado
- Campos opcionais ausentes
- Normalização de listas/dicionários

---

## Contribuindo

Contribuições são bem-vindas! Por favor, leia nosso [guia de contribuição](CONTRIBUTING.md) para mais detalhes sobre como contribuir para este projeto.
