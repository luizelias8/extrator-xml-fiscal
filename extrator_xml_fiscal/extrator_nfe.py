from typing import Dict, Any, List, Optional
from .extrator_base import ExtratorBase
from . import utils


class ExtratorNFe(ExtratorBase):
    """
    Extrator específico para Nota Fiscal Eletrônica (NFe).

    Processa arquivo XML de NFe e extrai dados estruturados incluindo
    informações de emitente, destinatário, produtos, impostos e totais.
    """

    def _extrair_dados(self, dados_xml: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extrai dados específicos da NFe.

        Args:
            dados_xml: XML da NFe convertido para dicionário

        Returns:
            Dict: Dados estruturados da NFe
        """
        raiz_nfe = self._encontrar_raiz(dados_xml)

        dados_nfe = {
            'identificacao': {},
            'emitente': {},
            'destinatario': {},
            'autorizados_xml': [],
            'produtos': [],
            'transporte': {},
            'totais': {},
            'informacoes_adicionais': {}
        }

        # Extrai casa seção da NFe
        dados_nfe['identificacao'] = self._extrair_identificacao(raiz_nfe)

        if 'emit' in raiz_nfe:
            dados_nfe['emitente'] = self._extrair_emitente(raiz_nfe['emit'])

        if 'dest' in raiz_nfe:
            dados_nfe['destinatario'] = self._extrair_destinatario(raiz_nfe['dest'])

        if 'autXML' in raiz_nfe:
            dados_nfe['autorizados_xml'] = self._extrair_autorizados_xml(raiz_nfe['autXML'])

        if 'det' in raiz_nfe:
            dados_nfe['produtos'] = self._extrair_produtos(raiz_nfe['det'])

        if 'transp' in raiz_nfe:
            dados_nfe['transporte'] = self._extrair_dados_transporte(raiz_nfe['transp'])

        if 'total' in raiz_nfe:
            dados_nfe['totais'] = self._extrair_totais(raiz_nfe['total'])

        if 'infAdic' in raiz_nfe:
            dados_nfe['informacoes_adicionais'] = self._extrair_informacoes_adicionais(raiz_nfe['infAdic'])

        return dados_nfe

    def _encontrar_raiz(self, dados_xml: Dict[str, Any]) -> Dict[str, Any]:
        """
        Encontra a raiz da NFe no XML, lidando com diferentes estruturas.
        """
        try:
            estruturas_nfe = ['nfeProc', 'NFe', 'infNFe']
            estrutura_encontrada = utils.validar_estrutura_xml(dados_xml, estruturas_nfe)

            if estrutura_encontrada == 'nfeProc':
                return dados_xml['nfeProc']['NFe']['infNFe']
            if estrutura_encontrada == 'NFe':
                return dados_xml['NFe']['infNFe']
            else: # infNFe
                return dados_xml['infNFe']

        except KeyError as e:
            raise ValueError(f'XML não possui estrutura válida de NFe. Campo ausente: {str(e)}')

    def _extrair_identificacao(self, raiz_nfe: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai dados gerais da nota fiscal."""
        ide = raiz_nfe.get('ide', {})

        return {
            'versao_layout_nfe': raiz_nfe.get('@versao'),
            'chave_acesso': raiz_nfe.get('@Id').replace('NFe', ''),
            'codigo_uf': ide.get('cUF'),
            'codigo_nf': ide.get('cNF'),
            'natureza_operacao': ide.get('natOp'),
            'modelo': ide.get('mod'),
            'serie': ide.get('serie'),
            'numero_nf': ide.get('nNF'),
            'data_emissao': ide.get('dhEmi'),
            'data_saida': ide.get('dhSaiEnt'),
            'tipo_operacao': ide.get('tpNF'),
            'destino_operacao': ide.get('idDest'),
            'codigo_municipio': ide.get('cMunFG'),
            'codigo_municipio_ibs': ide.get('cMunFGIBS'),
            'tipo_impressao': ide.get('tpImp'),
            'tipo_emissao': ide.get('tpEmis'),
            'data_hora_contingencia': ide.get('dhCont'),
            'justificativa_contingencia': ide.get('xJust'),
            'codigo_dv': ide.get('cDV'),
            'ambiente': ide.get('tpAmb'),
            'finalidade_emissao': ide.get('finNFe'),
            'tipo_nf_debito': ide.get('tpNFDebito'),
            'tipo_nf_credito': ide.get('tpNFCredito'),
            'consumidor_final': ide.get('indFinal'),
            'indicador_presenca': ide.get('indPres'),
            'indicador_intermediador': ide.get('indIntermed'),
            'processo_emissao': ide.get('procEmi'),
            'versao_layout': ide.get('verProc'),
            'referencias': self._extrair_referencias(ide.get('NFref')),
            'compras_governamentais': self._extrair_compras_gov(ide.get('gCompraGov')),
            'pagamento_antecipado': self._extrair_pag_antecipado(ide.get('gPagAntecipado'))
        }

    def _extrair_compras_gov(self, dados_compra_gov: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai dados de compras governamentais."""
        if not dados_compra_gov:
            return {}

        return {
            'numero_empenho': dados_compra_gov.get('xNEmp'),
            'numero_pedido': dados_compra_gov.get('xPed'),
            'numero_contrato': dados_compra_gov.get('xCont')
        }

    def _extrair_pag_antecipado(self, dados_pag_ant: Dict[str, Any]) -> List[str]:
        """Extrai chaves de NFe de pagamento antecipado."""
        if not dados_pag_ant:
            return []

        refs = dados_pag_ant.get('refNFe', [])
        refs_normalizadas = utils.normalizar_para_lista(refs)

        return [ref for ref in refs_normalizadas if ref]

    def _extrair_referencias(self, dados_nfref: List[Dict]) -> List[Dict[str, Any]]:
        """Extrair as notas referenciadas (NFref) do grupo ide."""
        if not dados_nfref:
            return []

        referencias = []
        dados_normalizados = utils.normalizar_para_lista(dados_nfref)

        for ref in dados_normalizados:
            referencia = {}

            if 'refNFe' in ref:
                referencia['ref_nfe'] = ref['refNFe']
            if 'refNFeSig' in ref:
                referencia['ref_nfe_sigilosa'] = ref['refNFeSig']
            if 'refNF' in ref:
                referencia['ref_nf'] = ref['refNF']
            if 'refNFP' in ref:
                referencia['ref_nfp'] = ref['refNFP']
            if 'refCTe' in ref:
                referencia['ref_cte'] = ref['refCTe']
            if 'refECF' in ref:
                referencia['ref_ecf'] = ref['refECF']

            if referencia:
                referencias.append(referencia)

        return referencias

    def _extrair_emitente(self, dados_emit: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai dados do emitente."""
        endereco = dados_emit.get('enderEmit', {})

        dados_emitente = {
            'razao_social': dados_emit.get('xNome'),
            'nome_fantasia': dados_emit.get('xFant'),
            'inscricao_estadual': dados_emit.get('IE'),
            'inscricao_estadual_st': dados_emit.get('IEST'),
            'inscricao_municipal': dados_emit.get('IM'),
            'regime_tributario': dados_emit.get('CRT'),
            'cnae': dados_emit.get('CNAE'),
            'endereco': utils.extrair_endereco_padrao(endereco)
        }

        # Adiciona CNPJ ou CPF condicionalmente (emitente não tem ID estrangeiro)
        identificacao = utils.extrair_cnpj_cpf_condicional(dados_emit)
        dados_emitente.update(identificacao)

        return dados_emitente

    def _extrair_destinatario(self, dados_dest: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai dados do emitente."""
        endereco = dados_dest.get('enderDest', {})

        dados_destinatario = {
            'razao_social': dados_dest.get('xNome'),
            'inscricao_estadual': dados_dest.get('IE'),
            'inscricao_suframa': dados_dest.get('ISUF'),
            'inscricao_municipal': dados_dest.get('IM'),
            'ind_ie_dest': dados_dest.get('indIEDest'),
            'email': dados_dest.get('email'),
            'endereco': utils.extrair_endereco_padrao(endereco)
        }

        # Adiciona a identificação (CNPJ, CPF ou ID estrangeiro) de forma condicional
        identificacao = utils.extrair_identificacao_condicional(dados_dest)
        dados_destinatario.update(identificacao)

        return dados_destinatario

    def _extrair_autorizados_xml(self, dados_autxml: List[Dict]) -> List[Dict[str, Any]]:
        """Extrai dados dos autorizados para download do XML."""
        autorizados = []
        dados_normalizados = utils.normalizar_para_lista(dados_autxml)

        for item in dados_normalizados:
            dados_autorizado = utils.extrair_cnpj_cpf_condicional(item)
            if dados_autorizado:
                autorizados.append(dados_autorizado)

        return autorizados

    def _extrair_produtos(self, dados_det: List[Dict]) -> List[Dict[str, Any]]:
        """Extrai dados dos produtos/serviços."""
        produtos = []
        dados_normalizados = utils.normalizar_para_lista(dados_det)

        for item in dados_normalizados:
            prod = item.get('prod', {})
            imposto = item.get('imposto', {})

            produto = {
                'numero_item': item.get('@nItem'),
                'codigo_produto': prod.get('cProd'),
                'codigo_ean': prod.get('cEAN'),
                'descricao_produto': prod.get('xProd'),
                'ncm': prod.get('NCM'),
                'ex_tipi': prod.get('EXTIPI'),
                'cfop': prod.get('CFOP'),
                'unidade_comercial': prod.get('uCom'),
                'quantidade_comercial': prod.get('qCom'),
                'valor_unitario_comercial': prod.get('vUnCom'),
                'valor_total_bruto': prod.get('vProd'),
                'codigo_ean_tributavel': prod.get('cEANTrib'),
                'unidade_tributavel': prod.get('uTrib'),
                'quantidade_tributavel': prod.get('qTrib'),
                'valor_unitario_tributavel': prod.get('vUnTrib'),
                'valor_total_frete': prod.get('vFrete'),
                'valor_total_seguro': prod.get('vSeg'),
                'valor_desconto': prod.get('vDesc'),
                'outras_despesas_acessorias': prod.get('vOutro'),
                'indicador_totalizacao': prod.get('indTot'),
                'numero_pedido_compra': prod.get('xPed'),
                'item_pedido_compra': prod.get('nItemPed'),
                'numero_fci': prod.get('nFCI'),
                'nve': prod.get('NVE'),
                'cest': prod.get('CEST'),
                'indicador_escala': prod.get('indEscala'),
                'cnpj_fabricante': prod.get('CNPJFab'),
                'codigo_beneficio_fiscal': prod.get('cBenef'),
                'codigo_barra': prod.get('cBarra'),
                'codigo_barra_tributavel': prod.get('cBarraTrib'),
                'declaracoes_importacao': self._extrair_declaracoes_importacao(prod.get('DI', [])),
                'impostos': self._extrair_impostos_produto(imposto)
            }

            produtos.append(produto)

        return produtos

    def _extrair_declaracoes_importacao(self, dados_di: List[Dict]) -> List[Dict[str, Any]]:
        """Extrai declarações de importação do produto"""
        declaracoes = []
        dados_normalizados = utils.normalizar_para_lista(dados_di)

        for di in dados_normalizados:
            declaracao = {
                'numero_di': di.get('nDI'),
                'data_di': di.get('dDI'),
                'local_desembaraco': di.get('xLocDesemb'),
                'uf_desembaraco': di.get('UFDesemb'),
            }
            declaracoes.append(declaracao)

        return declaracoes

    def _extrair_creditos_presumidos(self, dados_gcred: List[Dict]) -> List[Dict[str, Any]]:
        """Extrai informações de crédito presumido (até 4 ocorrências)."""
        if not dados_gcred:
            return []

        creditos = []
        dados_normalizados = utils.normalizar_para_lista(dados_gcred)

        for cred in dados_normalizados:
            credito = {
                'codigo_credito_presumido': cred.get('cCredPresumido'),
                'percentual_credito_presumido': cred.get('pCredPresumido'),
                'valor_credito_presumido': cred.get('vCredPresumido')
            }
            if any(credito.values()):
                creditos.append(credito)

        return creditos

    def _extrair_detalhes_exportacao(self, dados_export: List[Dict]) -> List[Dict[str, Any]]:
        """Extrai detalhes de exportação (até 500 ocorrências)."""
        if not dados_export:
            return []

        exportacoes = []
        dados_normalizados = utils.normalizar_para_lista(dados_export)

        for exp in dados_normalizados:
            exportacao = {
                'numero_drawback': exp.get('nDraw'),
                'exportacao_indireta': None
            }

            if 'exportInd' in exp:
                export_ind = exp['exportInd']
                exportacao['exportacao_indireta'] = {
                    'numero_re': export_ind.get('nRE'),
                    'chave_nfe': export_ind.get('chNFe'),
                    'quantidade_exportada': export_ind.get('qExport')
                }

            exportacoes.append(exportacao)

        return exportacoes

    def _extrair_rastreabilidade(self, dados_rastro: List[Dict]) -> List[Dict[str, Any]]:
        """Extrai informações de rastreabilidade (até 500 ocorrências)."""
        if not dados_rastro:
            return []

        rastros = []
        dados_normalizados = utils.normalizar_para_lista(dados_rastro)

        for rastro in dados_normalizados:
            item_rastro = {
                'numero_lote': rastro.get('nLote'),
                'quantidade_lote': rastro.get('qLote'),
                'data_fabricacao': rastro.get('dFab'),
                'data_validade': rastro.get('dVal'),
                'codigo_agregacao': rastro.get('cAgreg')
            }
            if any(item_rastro.values()):
                rastros.append(item_rastro)

        return rastros

    def _extrair_informacoes_nff(self, dados_nff: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai informações específicas para NFF."""
        if not dados_nff:
            return {}

        return {
            'codigo_produto_fisco': dados_nff.get('cProdFisco'),
            'codigo_operacao_nff': dados_nff.get('cOperNFF')
        }

    def _extrair_informacoes_embalagem(self, dados_emb: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai informações de embalagem do produto."""
        if not dados_emb:
            return {}

        return {
            'descricao_embalagem': dados_emb.get('xEmb'),
            'quantidade_volume_embalagem': dados_emb.get('qVolEmb'),
            'unidade_embalagem': dados_emb.get('uEmb')
        }

    def _extrair_produto_especifico(self, prod: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai informações de produtos específicos (veículos, medicamentos, etc)."""
        produto_esp = {}

        # Veículos novos
        if 'veicProd' in prod:
            produto_esp['veiculo'] = self._extrair_veiculo(prod['veicProd'])

        # Medicamentos
        if 'med' in prod:
            produto_esp['medicamento'] = self._extrair_medicamento(prod['med'])

        # Armamentos
        if 'arma' in prod:
            produto_esp['armamentos'] = self._extrair_armamentos(prod['arma'])

        # Combustíveis
        if 'comb' in prod:
            produto_esp['combustivel'] = self._extrair_combustivel(prod['comb'])

        return produto_esp

    def _extrair_veiculo(self, dados_veic: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai dados específicos de veículos novos."""
        return {
            'tipo_operacao': dados_veic.get('tpOp'),
            'chassi': dados_veic.get('chassi'),
            'codigo_cor': dados_veic.get('cCor'),
            'descricao_cor': dados_veic.get('xCor'),
            'potencia': dados_veic.get('pot'),
            'cilindradas': dados_veic.get('cilin'),
            'peso_liquido': dados_veic.get('pesoL'),
            'peso_bruto': dados_veic.get('pesoB'),
            'numero_serie': dados_veic.get('nSerie'),
            'tipo_combustivel': dados_veic.get('tpComb'),
            'numero_motor': dados_veic.get('nMotor'),
            'capacidade_maxima_tracao': dados_veic.get('CMT'),
            'distancia_eixos': dados_veic.get('dist'),
            'ano_modelo': dados_veic.get('anoMod'),
            'ano_fabricacao': dados_veic.get('anoFab'),
            'tipo_pintura': dados_veic.get('tpPint'),
            'tipo_veiculo': dados_veic.get('tpVeic'),
            'especie_veiculo': dados_veic.get('espVeic'),
            'vin': dados_veic.get('VIN'),
            'condicao_veiculo': dados_veic.get('condVeic'),
            'codigo_marca_modelo': dados_veic.get('cMod'),
            'codigo_cor_denatran': dados_veic.get('cCorDENATRAN'),
            'lotacao': dados_veic.get('lota'),
            'tipo_restricao': dados_veic.get('tpRest')
        }

    def _extrair_medicamento(self, dados_med: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai dados específicos de medicamentos."""
        return {
            'codigo_produto_anvisa': dados_med.get('cProdANVISA'),
            'motivo_isencao': dados_med.get('xMotivoIsencao'),
            'preco_maximo_consumidor': dados_med.get('vPMC')
        }

    def _extrair_armamentos(self, dados_arma: List[Dict]) -> List[Dict[str, Any]]:
        """Extrai dados específicos de armamentos (até 500)."""
        if not dados_arma:
            return []

        armamentos = []
        dados_normalizados = utils.normalizar_para_lista(dados_arma)

        for arma in dados_normalizados:
            armamento = {
                'tipo_arma': arma.get('tpArma'),
                'numero_serie': arma.get('nSerie'),
                'numero_cano': arma.get('nCano'),
                'descricao': arma.get('descr')
            }
            if any(armamento.values()):
                armamentos.append(armamento)

        return armamentos

    def _extrair_combustivel(self, dados_comb: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai dados específicos de combustíveis."""
        combustivel = {
            'codigo_produto_anp': dados_comb.get('cProdANP'),
            'descricao_anp': dados_comb.get('descANP'),
            'percentual_glp': dados_comb.get('pGLP'),
            'percentual_gn_nacional': dados_comb.get('pGNn'),
            'percentual_gn_importado': dados_comb.get('pGNi'),
            'valor_partida': dados_comb.get('vPart'),
            'codigo_codif': dados_comb.get('CODIF'),
            'quantidade_temperatura': dados_comb.get('qTemp'),
            'uf_consumo': dados_comb.get('UFCons'),
            'percentual_biodiesel': dados_comb.get('pBio')
        }

        # CIDE Combustíveis
        if 'CIDE' in dados_comb:
            cide = dados_comb['CIDE']
            combustivel['cide'] = {
                'quantidade_bc': cide.get('qBCProd'),
                'aliquota': cide.get('vAliqProd'),
                'valor_cide': cide.get('vCIDE')
            }

        # Encerrante
        if 'encerrante' in dados_comb:
            enc = dados_comb['encerrante']
            combustivel['encerrante'] = {
                'numero_bico': enc.get('nBico'),
                'numero_bomba': enc.get('nBomba'),
                'numero_tanque': enc.get('nTanque'),
                'valor_encerrante_inicial': enc.get('vEncIni'),
                'valor_encerrante_final': enc.get('vEncFin')
            }

        # Origem do combustível
        if 'origComb' in dados_comb:
            combustivel['origens'] = self._extrair_origem_combustivel(dados_comb['origComb'])

        return combustivel

    def _extrair_origem_combustivel(self, dados_orig: List[Dict]) -> List[Dict[str, Any]]:
        """Extrai origem do combustível (até 30 ocorrências)."""
        if not dados_orig:
            return []

        origens = []
        dados_normalizados = utils.normalizar_para_lista(dados_orig)

        for orig in dados_normalizados:
            origem = {
                'indicador_importacao': orig.get('indImport'),
                'codigo_uf_origem': orig.get('cUFOrig'),
                'percentual_origem': orig.get('pOrig')
            }
            if any(origem.values()):
                origens.append(origem)

        return origens

    def _extrair_tributos_devolvidos(self, dados_devol: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai informações de tributos devolvidos."""
        if not dados_devol:
            return {}

        tributos = {
            'percentual_devolucao': dados_devol.get('pDevol')
        }

        if 'IPI' in dados_devol:
            tributos['ipi_devolvido'] = dados_devol['IPI'].get('vIPIDevol')

        return tributos

    def _extrair_observacoes_item(self, dados_obs: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai observações do item."""
        if not dados_obs:
            return {}

        observacoes = {}

        if 'obsCont' in dados_obs:
            obs_cont = dados_obs['obsCont']
            observacoes['contribuinte'] = {
                'campo': obs_cont.get('@xCampo'),
                'texto': obs_cont.get('xTexto')
            }

        if 'obsFisco' in dados_obs:
            obs_fisco = dados_obs['obsFisco']
            observacoes['fisco'] = {
                'campo': obs_fisco.get('@xCampo'),
                'texto': obs_fisco.get('xTexto')
            }

        return observacoes

    def _extrair_dfe_referenciado(self, dados_ref: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai referência a outros DFe."""
        if not dados_ref:
            return {}

        return {
            'chave_acesso': dados_ref.get('chaveAcesso'),
            'numero_item': dados_ref.get('nItem')
        }

    def _extrair_impostos_produto(self, dados_imposto: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai todos os impostos do produto de forma completa."""
        impostos = {}

        # Valor aproximado de tributos do item
        if 'vTotTrib' in dados_imposto:
            impostos['valor_total_tributos_item'] = dados_imposto['vTotTrib']

        # ICMS
        if 'ICMS' in dados_imposto:
            impostos['icms'] = self._extrair_icms(dados_imposto['ICMS'])

        # IPI
        if 'IPI' in dados_imposto:
            impostos['ipi'] = self._extrair_ipi(dados_imposto['IPI'])

        # II
        if 'II' in dados_imposto:
            impostos['ii'] = self._extrair_ii(dados_imposto['II'])

        # PIS
        if 'PIS' in dados_imposto:
            impostos['pis'] = self._extrair_pis(dados_imposto['PIS'])

        # PIS ST
        if 'PISST' in dados_imposto:
            impostos['pis_st'] = self._extrair_pis_st(dados_imposto['PISST'])

        # COFINS
        if 'COFINS' in dados_imposto:
            impostos['cofins'] = self._extrair_cofins(dados_imposto['COFINS'])

        # COFINS
        if 'COFINSST' in dados_imposto:
            impostos['cofins_st'] = self._extrair_cofins_st(dados_imposto['COFINSST'])

        # ICMS UF Destino
        if 'ICMSUFDest' in dados_imposto:
            impostos['icms_uf_dest'] = self._extrair_icms_uf_dest(dados_imposto['ICMSUFDest'])

        # Imposto Seletivo
        if 'IS' in dados_imposto:
            impostos['imposto_seletivo'] = self._extrair_imposto_seletivo(dados_imposto['IS'])

        # IBS/CBS (novos tributos da reforma tributária)
        if 'IBSCBS' in dados_imposto:
            impostos['ibs_cbs'] = self._extrair_ibs_cbs(dados_imposto['IBSCBS'])

        return impostos

    def _extrair_icms(self, dados_icms: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai dados do ICMS."""
        # Encontra o tipo de ICMS
        icms_tipo = {}
        chave_icms = None

        for chave, valor in dados_icms.items():
            if chave.startswith('ICMS'):
                icms_tipo = valor
                chave_icms = chave
                break

        icms_base = {
            'modalidade': chave_icms,
            'origem': icms_tipo.get('orig'),
            'cst': icms_tipo.get('CST'),
            'csosn': icms_tipo.get('CSOSN')  # Para Simples Nacional
        }

        # Campos específicos por modalidade
        # Base de cálculo e valor ICMS próprio
        if 'vBC' in icms_tipo:
            icms_base['valor_bc'] = icms_tipo.get('vBC')
        if 'pICMS' in icms_tipo:
            icms_base['aliquota'] = icms_tipo.get('pICMS')
        if 'vICMS' in icms_tipo:
            icms_base['valor_icms'] = icms_tipo.get('vICMS')
        if 'pRedBC' in icms_tipo:
            icms_base['percentual_reducao_bc'] = icms_tipo.get('pRedBC')

        # ICMS ST
        if 'vBCST' in icms_tipo:
            icms_base['valor_bc_st'] = icms_tipo.get('vBCST')
        if 'pICMSST' in icms_tipo:
            icms_base['aliquota_st'] = icms_tipo.get('pICMSST')
        if 'vICMSST' in icms_tipo:
            icms_base['valor_icms_st'] = icms_tipo.get('vICMSST')
        if 'pMVAST' in icms_tipo:
            icms_base['margem_valor_agregado_st'] = icms_tipo.get('pMVAST')
        if 'pRedBCST' in icms_tipo:
            icms_base['percentual_reducao_bc_st'] = icms_tipo.get('pRedBCST')

        # FCP (Fundo de Combate à Pobreza)
        if 'vBCFCP' in icms_tipo:
            icms_base['valor_bc_fcp'] = icms_tipo.get('vBCFCP')
        if 'pFCP' in icms_tipo:
            icms_base['percentual_fcp'] = icms_tipo.get('pFCP')
        if 'vFCP' in icms_tipo:
            icms_base['valor_fcp'] = icms_tipo.get('vFCP')

        # FCP ST
        if 'vBCFCPST' in icms_tipo:
            icms_base['valor_bc_fcp_st'] = icms_tipo.get('vBCFCPST')
        if 'pFCPST' in icms_tipo:
            icms_base['percentual_fcp_st'] = icms_tipo.get('pFCPST')
        if 'vFCPST' in icms_tipo:
            icms_base['valor_fcp_st'] = icms_tipo.get('vFCPST')

        # ICMS Monofásico (campos específicos)
        if 'qBCMono' in icms_tipo:
            icms_base['quantidade_bc_mono'] = icms_tipo.get('qBCMono')
        if 'adRemICMS' in icms_tipo:
            icms_base['aliquota_ad_rem'] = icms_tipo.get('adRemICMS')
        if 'vICMSMono' in icms_tipo:
            icms_base['valor_icms_mono'] = icms_tipo.get('vICMSMono')

        # Desoneração
        if 'vICMSDeson' in icms_tipo:
            icms_base['valor_icms_desoneracao'] = icms_tipo.get('vICMSDeson')
        if 'motDesICMS' in icms_tipo:
            icms_base['motivo_desoneracao'] = icms_tipo.get('motDesICMS')
        if 'indDeduzDeson' in icms_tipo:
            icms_base['indicador_deduz_desoneracao'] = icms_tipo.get('indDeduzDeson')

        # Simples Nacional - crédito
        if 'pCredSN' in icms_tipo:
            icms_base['percentual_credito_sn'] = icms_tipo.get('pCredSN')
        if 'vCredICMSSN' in icms_tipo:
            icms_base['valor_credito_icms_sn'] = icms_tipo.get('vCredICMSSN')

        # ST Retido
        if 'vBCSTRet' in icms_tipo:
            icms_base['valor_bc_st_retido'] = icms_tipo.get('vBCSTRet')
        if 'vICMSSTRet' in icms_tipo:
            icms_base['valor_icms_st_retido'] = icms_tipo.get('vICMSSTRet')

        return icms_base

    def _extrair_ipi(self, dados_ipi: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai dados específicos do IPI."""
        ipi_tipo = {}
        for chave, valor in dados_ipi.items():
            if chave.startswith('IPI'):
                ipi_tipo = valor
                break

        return {
            'cst': ipi_tipo.get('CST'),
            'valor_bc': ipi_tipo.get('vBC'),
            'aliquota': ipi_tipo.get('pIPI'),
            'valor_ipi': ipi_tipo.get('vIPI'),
            'codigo_enquadramento': dados_ipi.get('cEnq'),
        }

    def _extrair_pis(self, dados_pis: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai dados específicos do PIS."""
        pis_tipo = {}
        for chave, valor in dados_pis.items():
            if chave.startswith('PIS'):
                pis_tipo = valor
                break

        return {
            'cst': pis_tipo.get('CST'),
            'valor_bc': pis_tipo.get('vBC'),
            'aliquota': pis_tipo.get('pPIS'),
            'valor_pis': pis_tipo.get('vPIS')
        }

    def _extrair_cofins(self, dados_cofins: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai dados específicos do COFINS."""
        cofins_tipo = {}
        for chave, valor in dados_cofins.items():
            if chave.startswith('COFINS'):
                cofins_tipo = valor
                break

        return {
            'cst': cofins_tipo.get('CST'),
            'valor_bc': cofins_tipo.get('vBC'),
            'aliquota': cofins_tipo.get('pCOFINS'),
            'valor_pis': cofins_tipo.get('vCOFINS')
        }

    def _extrair_ii(self, dados_ii: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai dados do Imposto de Importação."""
        return {
            'valor_bc': dados_ii.get('vBC'),
            'valor_despesas_aduaneiras': dados_ii.get('vDespAdu'),
            'valor_ii': dados_ii.get('vII'),
            'valor_iof': dados_ii.get('vIOF'),
        }

    def _extrair_pis_st(self, dados_pis_st: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai dados do PIS Substituição Tributária."""
        pis_st = {}

        # Base de cálculo por valor ou quantidade
        if 'vBC' in dados_pis_st:
            pis_st['valor_bc'] = dados_pis_st.get('vBC')
            pis_st['percentual_pis'] = dados_pis_st.get('pPIS')
        elif 'qBCProd' in dados_pis_st:
            pis_st['quantidade_bc'] = dados_pis_st.get('qBCProd')
            pis_st['aliquota_reais'] = dados_pis_st.get('vAliqProd')

        pis_st['valor_pis'] = dados_pis_st.get('vPIS')
        pis_st['indicador_soma_total'] = dados_pis_st.get('indSomaPISST')

        return pis_st

    def _extrair_cofins_st(self, dados_cofins_st: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai dados do COFINS Substituição Tributária."""
        cofins_st = {}

        # Base de cálculo por valor ou quantidade
        if 'vBC' in dados_cofins_st:
            cofins_st['valor_bc'] = dados_cofins_st.get('vBC')
            cofins_st['percentual_cofins'] = dados_cofins_st.get('pCOFINS')
        elif 'qBCProd' in dados_cofins_st:
            cofins_st['quantidade_bc'] = dados_cofins_st.get('qBCProd')
            cofins_st['aliquota_reais'] = dados_cofins_st.get('vAliqProd')

        cofins_st['valor_cofins'] = dados_cofins_st.get('vCOFINS')
        cofins_st['indicador_soma_total'] = dados_cofins_st.get('indSomaCOFINSST')

        return cofins_st

    def _extrair_icms_uf_dest(self, dados_uf_dest: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai dados de partilha ICMS UF destino."""
        return {
            'valor_bc_uf_dest': dados_uf_dest.get('vBCUFDest'),
            'valor_bc_fcp_uf_dest': dados_uf_dest.get('vBCFCPUFDest'),
            'percentual_fcp_uf_dest': dados_uf_dest.get('pFCPUFDest'),
            'percentual_icms_uf_dest': dados_uf_dest.get('pICMSUFDest'),
            'percentual_icms_inter': dados_uf_dest.get('pICMSInter'),
            'percentual_icms_inter_part': dados_uf_dest.get('pICMSInterPart'),
            'valor_fcp_uf_dest': dados_uf_dest.get('vFCPUFDest'),
            'valor_icms_uf_dest': dados_uf_dest.get('vICMSUFDest'),
            'valor_icms_uf_remet': dados_uf_dest.get('vICMSUFRemet')
        }

    def _extrair_imposto_seletivo(self, dados_is: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai dados do Imposto Seletivo (novo tributo)."""
        # Este é um tributo novo da reforma tributária
        # A estrutura pode variar conforme implementação final
        return {
            'valor_bc': dados_is.get('vBC'),
            'aliquota': dados_is.get('pIS'),
            'valor_is': dados_is.get('vIS'),
            'quantidade_bc': dados_is.get('qBCProd'),
            'aliquota_especifica': dados_is.get('vAliqProd')
        }

    def _extrair_ibs_cbs(self, dados_ibs_cbs: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai dados dos tributos IBS/CBS (reforma tributária)."""
        # Tributos novos que substituirão vários tributos atuais
        # A estrutura pode variar conforme implementação final
        return {
            'valor_bc': dados_ibs_cbs.get('vBC'),
            'aliquota_ibs': dados_ibs_cbs.get('pIBS'),
            'valor_ibs': dados_ibs_cbs.get('vIBS'),
            'aliquota_cbs': dados_ibs_cbs.get('pCBS'),
            'valor_cbs': dados_ibs_cbs.get('vCBS'),
            'regime_apuracao': dados_ibs_cbs.get('regApuracao')
        }

    def _extrair_dados_transporte(self, dados_transp: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai dados do transporte da mercadoria."""
        transportadora = dados_transp.get('transporta', {})

        # Monta dados da transportadora
        dados_transportadora = {
            'razao_social': transportadora.get('xNome'),
            'inscricao_estadual': transportadora.get('IE'),
            'endereco_completo': transportadora.get('xEnder'),
            'municipio': transportadora.get('xMun'),
            'uf': transportadora.get('UF')
        }

        # Adiciona CNPJ ou CPF condicionalmente
        dados_transportadora.update(utils.extrair_cnpj_cpf_condicional(transportadora))

        return {
            'modalidade_frete': dados_transp.get('modFrete'),
            'transportadora': dados_transportadora,
            'volumes': self._extrair_volumes_transporte(dados_transp.get('vol', []))
        }

    def _extrair_volumes_transporte(self, dados_vol: List[Dict]) -> List[Dict[str, Any]]:
        """Extrai dados dos volumes transportados."""
        volumes = []
        dados_normalizados = utils.normalizar_para_lista(dados_vol)

        for vol in dados_normalizados:
            volume = {
                'quantidade': vol.get('qVol'),
                'especie': vol.get('esp'),
                'marca': vol.get('marca'),
                'numeracao': vol.get('nVol'),
                'peso_liquido': vol.get('pesoL'),
                'peso_bruto': vol.get('pesoB')
            }
            volumes.append(volume)

        return volumes

    def _extrair_totais(self, dados_total: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai os totais da nota fiscal."""
        icms_tot = dados_total.get('ICMSTot', {})

        return {
            'valor_base_calculo_icms': icms_tot.get('vBC'),
            'valor_total_icms': icms_tot.get('vICMS'),
            'valor_total_icms_desonerado': icms_tot.get('vICMSDeson'),
            'valor_base_calculo_icms_st': icms_tot.get('vBCST'),
            'valor_total_icms_st': icms_tot.get('vST'),
            'valor_total_produtos': icms_tot.get('vProd'),
            'valor_total_frete': icms_tot.get('vFrete'),
            'valor_total_seguro': icms_tot.get('vSeg'),
            'valor_total_desconto': icms_tot.get('vDesc'),
            'valor_total_ii': icms_tot.get('vII'),
            'valor_total_ipi': icms_tot.get('vIPI'),
            'valor_total_pis': icms_tot.get('vPIS'),
            'valor_total_cofins': icms_tot.get('vCOFINS'),
            'valor_total_outras_despesas': icms_tot.get('vOutro'),
            'valor_total_nota_fiscal': icms_tot.get('vNF'),
            'valor_total_tributos': icms_tot.get('vTotTrib')
        }

    def _extrair_informacoes_adicionais(self, dados_infadic: Dict[str, Any]) -> Dict[str, Any]:
        """Extrair informacoes adicionais da nota fiscal."""
        if not dados_infadic or dados_infadic is None:
            return {
                'informacoes_fisco': None,
                'informacoes_complementares': None
            }

        return {
            'informacoes_fisco': utils.limpar_texto(dados_infadic.get('infAdFisco')),
            'informacoes_complementares': utils.limpar_texto(dados_infadic.get('infCpl'))
        }
