import os
from extrator_xml_fiscal.extrator_nfe import ExtratorNFe

CAMINHO_FIXTURE = os.path.join(os.path.dirname(__file__), 'fixtures', 'nfe_entrega.xml')


def test_extrai_local_entrega_quando_diferente_do_destinatario():
    extrator = ExtratorNFe()
    dados = extrator.processar_arquivo(CAMINHO_FIXTURE)
    entrega = dados['local_entrega']

    assert entrega['cpf'] == '36969545865'
    assert entrega['razao_social'] == 'Lara Conti'
    assert entrega['endereco']['logradouro'] == 'Rua Cinco'
    assert entrega['endereco']['numero'] == '63'
    assert entrega['endereco']['bairro'] == 'Terras Alpha'
    assert entrega['endereco']['municipio'] == 'Resende'
    assert entrega['endereco']['uf'] == 'RJ'
    assert entrega['endereco']['cep'] == '27516389'
    assert entrega['endereco']['telefone'] == '21998060245'


def test_extrair_entrega_sem_grupo_retorna_dict_vazio():
    extrator = ExtratorNFe()

    assert extrator._extrair_entrega({}) == {}
    assert extrator._extrair_entrega(None) == {}
