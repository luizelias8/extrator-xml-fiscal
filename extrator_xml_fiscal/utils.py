import re
from typing import Dict, Any, List, Optional, Union


def limpar_texto(texto: Optional[str]) -> Optional[str]:
    """
    Remove quebras de linha, espaços extras e normaliza espaçamento

    Args:
        texto: (Optional[str]): Texto a ser limpo

    Returns:
        Optional[str]: Texto limpo ou None se entrada for None/vazia
    """
    if not texto:
        return texto

    # Remove quebras de linha e normaliza espaços
    texto_limpo = texto.replace('\n', '').replace('\r', '').strip()

    # Remove espaços duplos/triplos
    return re.sub(r'\s+', ' ', texto_limpo)

def normalizar_para_lista(dados: Union[Dict, List, None]) -> List[Dict]: # Union[Dict, List, None] significa que o valor pode ser de um entre vários tipos (Dict=dicionário, List=lista ou None=ausência de valor).
    """
    Converte dados para lista, tratando casos onde XML retorna
    dict para item único e list para múltiplos itens.

    Args:
        dados (Union[Dict, List, None]): Dados do XML

    Returns:
        List[Dict]: Lista normaizada (vazia se dados for None)
    """
    if not dados:
        return []

    if isinstance(dados, list):
        return dados
    if isinstance(dados, dict):
        return [dados]
    else:
        return []

def extrair_cnpj_cpf_condicional(dados: Dict[str, Any]) -> Dict[str, str]:
    """
    Extrai CNPJ ou CPF de forma condicional, incluindo apenas
    os campos que existem e têm valor.

    Args:
        dados (Dict[str, Any]): Dicionário contendo possíveis CNPJ/CPF

    Returns:
        Dict[str, str]: Dicionário com cnpj ou cpf (não ambos)
    """
    resultado = {}

    if dados.get('CNPJ'):
        resultado['cnpj'] = dados['CNPJ']
    elif dados.get('CPF'):
        resultado['cpf'] = dados['CPF']

    return resultado

def extrair_identificacao_condicional(dados: Dict[str, Any]) -> Dict[str, str]:
    """
    Extrai CNPJ, CPF ou ID estrangeiro de forma condicional,
    seguindo a regra de escolha exclusiva do XSD da NFe.

    Prioridade: CNPJ > CPF > idEstrangeiro

    Args:
        dados (Dict[str, Any]): Dicionário contendo possíveis identificadores

    Returns:
        Dict[str, str]: Dicionário com apenas um tipo de identificador
    """
    resultado = {}

    # Seguir a ordem de prioridade conforme aparece no XSD
    if dados.get('CNPJ'):
        resultado['cnpj'] = dados['CNPJ']
    elif dados.get('CPF'):
        resultado['cpf'] = dados['CPF']
    elif dados.get('idEstrangeiro'):
        resultado['id_estrangeiro'] = dados['idEstrangeiro']

    return resultado

def extrair_endereco_padrao(dados_endereco: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extrai dados de endereço seguindo estrutura padrão da SEFAZ.

    Args:
        dados_endereco (Dict[str, any]): Dados do endereço do XML

    Returns:
        Dict[str, Any]: Endereço estruturado
    """
    return {
        'logradouro': dados_endereco.get('xLgr'),
        'numero': dados_endereco.get('nro'),
        'complemento': dados_endereco.get('xCpl'),
        'bairro': dados_endereco.get('xBairro'),
        'codigo_municipio': dados_endereco.get('cMun'),
        'municipio': dados_endereco.get('xMun'),
        'uf': dados_endereco.get('UF'),
        'cep': dados_endereco.get('CEP'),
        'codigo_pais': dados_endereco.get('cPais'),
        'pais': dados_endereco.get('xPais'),
        'telefone': dados_endereco.get('fone')
    }

def validar_estrutura_xml(dados_xml: Dict[str, Any], estruturas_esperadas: List[str]) -> str:
    """
    Valida se o XML possui uma das estruturas esperadas.

    Args:
        dados_xml: XML convertido para dicionário
        estruturas_esperadas: Lista de estruturas válidas

    Returns:
        str: Nome da estrutura encontrada

    Raises:
        ValueError: Se nenhuma estrutura válida for encontrada
    """
    for estrutura in estruturas_esperadas:
        if estrutura in dados_xml:
            return estrutura

    estruturas_str = ', '.join(estruturas_esperadas)
    raise ValueError(f'Estrutura XML não reconhecida. Esperadas: {estruturas_str}')
