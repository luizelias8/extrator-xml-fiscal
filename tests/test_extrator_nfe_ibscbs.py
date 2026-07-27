import os
from extrator_xml_fiscal.extrator_nfe import ExtratorNFe

CAMINHO_FIXTURE = os.path.join(os.path.dirname(__file__), 'fixtures', 'nfe_ibscbs.xml')


def _produtos_da_fixture():
    extrator = ExtratorNFe()
    dados = extrator.processar_arquivo(CAMINHO_FIXTURE)
    return dados['produtos']


def test_extrai_ibs_cbs_do_primeiro_item():
    produtos = _produtos_da_fixture()
    ibs_cbs = produtos[0]['impostos']['ibs_cbs']

    assert ibs_cbs['cst'] == '000'
    assert ibs_cbs['classificacao_tributaria'] == '000001'
    assert ibs_cbs['valor_bc'] == '471.64'
    assert ibs_cbs['valor_ibs'] == '0.47'
    assert ibs_cbs['ibs_uf'] == {'aliquota': '0.10', 'valor': '0.47'}
    assert ibs_cbs['ibs_mun'] == {'aliquota': '0.00', 'valor': '0.00'}
    assert ibs_cbs['aliquota_cbs'] == '0.90'
    assert ibs_cbs['valor_cbs'] == '4.24'


def test_extrai_ibs_cbs_do_segundo_item():
    produtos = _produtos_da_fixture()
    ibs_cbs = produtos[1]['impostos']['ibs_cbs']

    assert ibs_cbs['valor_bc'] == '315.90'
    assert ibs_cbs['ibs_uf'] == {'aliquota': '0.10', 'valor': '0.32'}
    assert ibs_cbs['valor_cbs'] == '2.84'
