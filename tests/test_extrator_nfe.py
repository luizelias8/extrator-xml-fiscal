from extrator_xml_fiscal.extrator_nfe import ExtratorNFe

extrator = ExtratorNFe()

CHAVES_GRUPOS_OPCIONAIS = [
    'veiculo',
    'medicamento',
    'armamentos',
    'combustivel',
    'creditos_presumidos',
    'detalhes_exportacao',
    'rastreabilidade',
    'informacoes_nff',
    'informacoes_embalagem',
    'observacoes_item',
    'dfe_referenciado',
    'tributos_devolvidos',
]


def _det_base(prod_extra=None, det_extra=None):
    """Monta um det/prod mínimo, no mesmo formato produzido pelo xmltodict."""
    prod = {
        'cProd': '001',
        'cEAN': '7891234567890',
        'xProd': 'Produto de teste',
        'NCM': '12345678',
        'CFOP': '5102',
        'uCom': 'UN',
        'qCom': '1.0000',
        'vUnCom': '10.00',
        'vProd': '10.00',
        'uTrib': 'UN',
        'qTrib': '1.0000',
        'vUnTrib': '10.00',
        'indTot': '1'
    }
    if prod_extra:
        prod.update(prod_extra)

    det = {'@nItem': '1', 'prod': prod, 'imposto': {}}
    if det_extra:
        det.update(det_extra)

    return det


def test_extrair_produtos_sem_grupos_opcionais_nao_adiciona_chaves():
    det = _det_base()

    produtos = extrator._extrair_produtos([det])

    assert len(produtos) == 1
    produto = produtos[0]
    for chave in CHAVES_GRUPOS_OPCIONAIS:
        assert chave not in produto


def test_extrair_produtos_com_veiculo():
    det = _det_base(prod_extra={
        'veicProd': {
            'tpOp': '1',
            'chassi': '9BWZZZ377VT004251',
            'cCor': '01',
            'xCor': 'PRETA',
            'pot': '120',
            'cilin': '2000',
            'pesoL': '1200',
            'pesoB': '1300',
            'nSerie': '001',
            'tpComb': '01',
            'nMotor': 'MOTOR123',
            'CMT': '1500',
            'dist': '2500',
            'anoMod': '2026',
            'anoFab': '2025',
            'tpPint': '1',
            'tpVeic': '01',
            'espVeic': '1',
            'VIN': 'N',
            'condVeic': '1',
            'cMod': '123456',
            'cCorDENATRAN': '11',
            'lota': '5',
            'tpRest': '0'
        }
    })

    produtos = extrator._extrair_produtos([det])
    veiculo = produtos[0]['veiculo']

    assert veiculo['chassi'] == '9BWZZZ377VT004251'
    assert veiculo['descricao_cor'] == 'PRETA'
    assert veiculo['ano_modelo'] == '2026'
    for chave in CHAVES_GRUPOS_OPCIONAIS:
        if chave != 'veiculo':
            assert chave not in produtos[0]


def test_extrair_produtos_com_medicamento():
    det = _det_base(prod_extra={
        'med': {
            'cProdANVISA': '1234567890123',
            'xMotivoIsencao': 'Isento',
            'vPMC': '25.90'
        }
    })

    produtos = extrator._extrair_produtos([det])
    medicamento = produtos[0]['medicamento']

    assert medicamento['codigo_produto_anvisa'] == '1234567890123'
    assert medicamento['preco_maximo_consumidor'] == '25.90'


def test_extrair_produtos_com_armamento():
    det = _det_base(prod_extra={
        'arma': {
            'tpArma': '0',
            'nSerie': 'ARMA001',
            'nCano': 'CANO001',
            'descr': 'Arma de uso permitido'
        }
    })

    produtos = extrator._extrair_produtos([det])
    armamentos = produtos[0]['armamentos']

    assert len(armamentos) == 1
    assert armamentos[0]['numero_serie'] == 'ARMA001'
    assert armamentos[0]['descricao'] == 'Arma de uso permitido'


def test_extrair_produtos_com_combustivel():
    det = _det_base(prod_extra={
        'comb': {
            'cProdANP': '210203001',
            'descANP': 'GASOLINA C',
            'pGLP': '0.0000',
            'UFCons': 'SP'
        }
    })

    produtos = extrator._extrair_produtos([det])
    combustivel = produtos[0]['combustivel']

    assert combustivel['codigo_produto_anp'] == '210203001'
    assert combustivel['uf_consumo'] == 'SP'


def test_extrair_produtos_com_creditos_presumidos():
    det = _det_base(prod_extra={
        'gCred': [
            {
                'cCredPresumido': 'SP123456',
                'pCredPresumido': '5.00',
                'vCredPresumido': '0.50'
            }
        ]
    })

    produtos = extrator._extrair_produtos([det])
    creditos = produtos[0]['creditos_presumidos']

    assert len(creditos) == 1
    assert creditos[0]['codigo_credito_presumido'] == 'SP123456'
    assert creditos[0]['valor_credito_presumido'] == '0.50'


def test_extrair_produtos_com_detalhes_exportacao():
    det = _det_base(prod_extra={
        'detExport': {
            'nDraw': '123456',
            'exportInd': {
                'nRE': '987654321',
                'chNFe': '3' * 44,
                'qExport': '10.0000'
            }
        }
    })

    produtos = extrator._extrair_produtos([det])
    exportacoes = produtos[0]['detalhes_exportacao']

    assert len(exportacoes) == 1
    assert exportacoes[0]['numero_drawback'] == '123456'
    assert exportacoes[0]['exportacao_indireta']['numero_re'] == '987654321'


def test_extrair_produtos_com_rastreabilidade():
    det = _det_base(prod_extra={
        'rastro': {
            'nLote': 'LOTE001',
            'qLote': '100.000',
            'dFab': '2026-01-01',
            'dVal': '2027-01-01',
            'cAgreg': 'AGR001'
        }
    })

    produtos = extrator._extrair_produtos([det])
    rastreabilidade = produtos[0]['rastreabilidade']

    assert len(rastreabilidade) == 1
    assert rastreabilidade[0]['numero_lote'] == 'LOTE001'
    assert rastreabilidade[0]['data_validade'] == '2027-01-01'


def test_extrair_produtos_com_informacoes_nff():
    det = _det_base(prod_extra={
        'infProdNFF': {
            'cProdFisco': '12345678901234',
            'cOperNFF': '123'
        }
    })

    produtos = extrator._extrair_produtos([det])
    nff = produtos[0]['informacoes_nff']

    assert nff['codigo_produto_fisco'] == '12345678901234'
    assert nff['codigo_operacao_nff'] == '123'


def test_extrair_produtos_com_informacoes_embalagem():
    det = _det_base(prod_extra={
        'infProdEmb': {
            'xEmb': 'CX',
            'qVolEmb': '10.0000',
            'uEmb': 'CX10'
        }
    })

    produtos = extrator._extrair_produtos([det])
    embalagem = produtos[0]['informacoes_embalagem']

    assert embalagem['descricao_embalagem'] == 'CX'
    assert embalagem['unidade_embalagem'] == 'CX10'


def test_extrair_produtos_com_observacoes_item():
    det = _det_base(det_extra={
        'obsItem': {
            'obsCont': {'@xCampo': 'campo1', 'xTexto': 'Observação do contribuinte'},
            'obsFisco': {'@xCampo': 'campo2', 'xTexto': 'Observação do fisco'}
        }
    })

    produtos = extrator._extrair_produtos([det])
    observacoes = produtos[0]['observacoes_item']

    assert observacoes['contribuinte']['texto'] == 'Observação do contribuinte'
    assert observacoes['fisco']['campo'] == 'campo2'


def test_extrair_produtos_com_dfe_referenciado():
    det = _det_base(det_extra={
        'DFeReferenciado': {
            'chaveAcesso': '4' * 44,
            'nItem': '2'
        }
    })

    produtos = extrator._extrair_produtos([det])
    referencia = produtos[0]['dfe_referenciado']

    assert referencia['chave_acesso'] == '4' * 44
    assert referencia['numero_item'] == '2'


def test_extrair_produtos_com_tributos_devolvidos():
    det = _det_base(det_extra={
        'impostoDevol': {
            'pDevol': '50.00',
            'IPI': {'vIPIDevol': '1.50'}
        }
    })

    produtos = extrator._extrair_produtos([det])
    devolvidos = produtos[0]['tributos_devolvidos']

    assert devolvidos['percentual_devolucao'] == '50.00'
    assert devolvidos['ipi_devolvido'] == '1.50'
