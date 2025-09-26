from typing import Dict, Any, List, Optional
from .extrator_base import ExtratorBase
from . import utils


class ExtratorCTe(ExtratorBase):
    """
    Extrator específico para Conhecimento de Transporte Eletrônico (CTe).

    Processa arquivo XML de CTe e extrai dados estruturados incluindo
    informações de identificação, emitente, remetente, destinatário,
    valores de prestação, impostos e dados específicos do transporte.
    """

    def _extrair_dados(self, dados_xml: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extrai dados específicos do CTe.

        Args:
            dados_xml: XML do CTe convertido para dicionário

        Returns:
            Dict: Dados estruturados do CTe
        """
        raiz_cte = self._encontrar_raiz(dados_xml)

        dados_cte = {
            'identificacao': {},
            'emitente': {},
            'remetente': {},
            'expedidor': {},
            'recebedor': {},
            'destinatario': {},
            'valores_prestacao': {},
            'impostos': {},
            'informacoes_carga': {},
            'informacoes_documentos': {},
            'informacoes_modais': {},
            'complementares': {},
            'responsavel_tecnico': {}
        }

        # Extrai cada seção do CTe
        dados_cte['identificacao'] = self._extrair_identificacao(raiz_cte)

        if 'emit' in raiz_cte:
            dados_cte['emitente'] = self._extrair_emitente(raiz_cte['emit'])

        if 'rem' in raiz_cte:
            dados_cte['remetente'] = self._extrair_remetente(raiz_cte['rem'])

        if 'exped' in raiz_cte:
            dados_cte['expedidor'] = self._extrair_expedidor(raiz_cte['exped'])

        if 'receb' in raiz_cte:
            dados_cte['recebedor'] = self._extrair_recebedor(raiz_cte['receb'])

        if 'dest' in raiz_cte:
            dados_cte['destinatario'] = self._extrair_destinatario(raiz_cte['dest'])

        if 'vPrest' in raiz_cte:
            dados_cte['valores_prestacao'] = self._extrair_valores_prestacao(raiz_cte['vPrest'])

        if 'imp' in raiz_cte:
            dados_cte['impostos'] = self._extrair_impostos(raiz_cte['imp'])

        if 'infCTeNorm' in raiz_cte:
            inf_cte_norm = raiz_cte['infCTeNorm']
            
            if 'infCarga' in inf_cte_norm:
                dados_cte['informacoes_carga'] = self._extrair_informacoes_carga(inf_cte_norm['infCarga'])

            if 'infDoc' in inf_cte_norm:
                dados_cte['informacoes_documentos'] = self._extrair_informacoes_documentos(inf_cte_norm['infDoc'])

            if 'infModal' in inf_cte_norm:
                dados_cte['informacoes_modais'] = self._extrair_informacoes_modais(inf_cte_norm['infModal'])

        if 'compl' in raiz_cte:
            dados_cte['complementares'] = self._extrair_complementares(raiz_cte['compl'])

        if 'infRespTec' in raiz_cte:
            dados_cte['responsavel_tecnico'] = self._extrair_responsavel_tecnico(raiz_cte['infRespTec'])

        return dados_cte

    def _encontrar_raiz(self, dados_xml: Dict[str, Any]) -> Dict[str, Any]:
        """
        Encontra a raiz do CTe no XML, lidando com diferentes estruturas.
        """
        try:
            estruturas_cte = ['cteProc', 'CTe', 'infCte']
            estrutura_encontrada = utils.validar_estrutura_xml(dados_xml, estruturas_cte)

            if estrutura_encontrada == 'cteProc':
                return dados_xml['cteProc']['CTe']['infCte']
            elif estrutura_encontrada == 'CTe':
                return dados_xml['CTe']['infCte']
            else:  # infCte
                return dados_xml['infCte']

        except KeyError as e:
            raise ValueError(f'XML não possui estrutura válida de CTe. Campo ausente: {str(e)}')

    def _extrair_identificacao(self, raiz_cte: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai dados gerais de identificação do CTe."""
        ide = raiz_cte.get('ide', {})

        return {
            'versao_layout_cte': raiz_cte.get('@versao'),
            'chave_acesso': raiz_cte.get('@Id', '').replace('CTe', ''),
            'codigo_uf': ide.get('cUF'),
            'codigo_ct': ide.get('cCT'),
            'cfop': ide.get('CFOP'),
            'natureza_operacao': ide.get('natOp'),
            'modelo': ide.get('mod'),
            'serie': ide.get('serie'),
            'numero_ct': ide.get('nCT'),
            'data_emissao': ide.get('dhEmi'),
            'tipo_impressao': ide.get('tpImp'),
            'tipo_emissao': ide.get('tpEmis'),
            'codigo_dv': ide.get('cDV'),
            'ambiente': ide.get('tpAmb'),
            'tipo_cte': ide.get('tpCTe'),
            'processo_emissao': ide.get('procEmi'),
            'versao_processo': ide.get('verProc'),
            'codigo_municipio_envio': ide.get('cMunEnv'),
            'municipio_envio': ide.get('xMunEnv'),
            'uf_envio': ide.get('UFEnv'),
            'modal': ide.get('modal'),
            'tipo_servico': ide.get('tpServ'),
            'codigo_municipio_inicio': ide.get('cMunIni'),
            'municipio_inicio': ide.get('xMunIni'),
            'uf_inicio': ide.get('UFIni'),
            'codigo_municipio_fim': ide.get('cMunFim'),
            'municipio_fim': ide.get('xMunFim'),
            'uf_fim': ide.get('UFFim'),
            'retira': ide.get('retira'),
            'indicador_ie_tomador': ide.get('indIEToma'),
            'tomador': self._extrair_tomador(ide)
        }

    def _extrair_tomador(self, ide: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai informações do tomador do serviço."""
        tomador_info = {}
        
        # Tomador pode estar em diferentes estruturas: toma3, toma4, etc.
        if 'toma3' in ide:
            tomador_info['tipo'] = 'toma3'
            tomador_info['codigo'] = ide['toma3'].get('toma')
        elif 'toma4' in ide:
            toma4 = ide['toma4']
            tomador_info['tipo'] = 'toma4'
            tomador_info['codigo'] = toma4.get('toma')
            
            # Adiciona dados do tomador quando for tipo 4 (outros)
            identificacao = utils.extrair_identificacao_condicional(toma4)
            tomador_info.update(identificacao)
            
            tomador_info.update({
                'razao_social': toma4.get('xNome'),
                'inscricao_estadual': toma4.get('IE'),
                'telefone': toma4.get('fone'),
                'endereco': self._extrair_endereco_tomador(toma4.get('enderToma', {}))
            })

        return tomador_info

    def _extrair_endereco_tomador(self, dados_endereco: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai endereço do tomador (estrutura específica do CTe)."""
        return utils.extrair_endereco_padrao(dados_endereco)

    def _extrair_emitente(self, dados_emit: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai dados do emitente do CTe."""
        endereco = dados_emit.get('enderEmit', {})

        dados_emitente = {
            'razao_social': dados_emit.get('xNome'),
            'inscricao_estadual': dados_emit.get('IE'),
            'regime_tributario': dados_emit.get('CRT'),
            'telefone': dados_emit.get('fone'),
            'endereco': utils.extrair_endereco_padrao(endereco)
        }

        # Adiciona CNPJ ou CPF condicionalmente
        identificacao = utils.extrair_cnpj_cpf_condicional(dados_emit)
        dados_emitente.update(identificacao)

        return dados_emitente

    def _extrair_remetente(self, dados_rem: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai dados do remetente."""
        endereco = dados_rem.get('enderReme', {})

        dados_remetente = {
            'razao_social': dados_rem.get('xNome'),
            'inscricao_estadual': dados_rem.get('IE'),
            'telefone': dados_rem.get('fone'),
            'endereco': utils.extrair_endereco_padrao(endereco)
        }

        # Adiciona identificação (CNPJ, CPF ou ID estrangeiro)
        identificacao = utils.extrair_identificacao_condicional(dados_rem)
        dados_remetente.update(identificacao)

        return dados_remetente

    def _extrair_expedidor(self, dados_exped: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai dados do expedidor."""
        endereco = dados_exped.get('enderExped', {})

        dados_expedidor = {
            'razao_social': dados_exped.get('xNome'),
            'inscricao_estadual': dados_exped.get('IE'),
            'telefone': dados_exped.get('fone'),
            'endereco': utils.extrair_endereco_padrao(endereco)
        }

        # Adiciona identificação (CNPJ, CPF ou ID estrangeiro)
        identificacao = utils.extrair_identificacao_condicional(dados_exped)
        dados_expedidor.update(identificacao)

        return dados_expedidor

    def _extrair_recebedor(self, dados_receb: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai dados do recebedor."""
        endereco = dados_receb.get('enderReceb', {})

        dados_recebedor = {
            'razao_social': dados_receb.get('xNome'),
            'inscricao_estadual': dados_receb.get('IE'),
            'telefone': dados_receb.get('fone'),
            'endereco': utils.extrair_endereco_padrao(endereco)
        }

        # Adiciona identificação (CNPJ, CPF ou ID estrangeiro)
        identificacao = utils.extrair_identificacao_condicional(dados_receb)
        dados_recebedor.update(identificacao)

        return dados_recebedor

    def _extrair_destinatario(self, dados_dest: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai dados do destinatário."""
        endereco = dados_dest.get('enderDest', {})

        dados_destinatario = {
            'razao_social': dados_dest.get('xNome'),
            'inscricao_estadual': dados_dest.get('IE'),
            'telefone': dados_dest.get('fone'),
            'endereco': utils.extrair_endereco_padrao(endereco)
        }

        # Adiciona identificação (CNPJ, CPF ou ID estrangeiro)
        identificacao = utils.extrair_identificacao_condicional(dados_dest)
        dados_destinatario.update(identificacao)

        return dados_destinatario

    def _extrair_valores_prestacao(self, dados_vprest: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai valores da prestação do serviço."""
        componentes = []
        
        # Extrai componentes do valor
        if 'Comp' in dados_vprest:
            comps_dados = utils.normalizar_para_lista(dados_vprest['Comp'])
            
            for comp in comps_dados:
                componente = {
                    'nome': comp.get('xNome'),
                    'valor': comp.get('vComp')
                }
                componentes.append(componente)

        return {
            'valor_total_prestacao': dados_vprest.get('vTPrest'),
            'valor_receber': dados_vprest.get('vRec'),
            'componentes': componentes
        }

    def _extrair_impostos(self, dados_imp: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai informações dos impostos do CTe."""
        impostos = {
            'valor_total_tributos': dados_imp.get('vTotTrib')
        }

        # ICMS
        if 'ICMS' in dados_imp:
            impostos['icms'] = self._extrair_icms_cte(dados_imp['ICMS'])

        # ICMS UF Fim (partilha interestadual)
        if 'ICMSUFFim' in dados_imp:
            impostos['icms_uf_fim'] = self._extrair_icms_uf_fim(dados_imp['ICMSUFFim'])

        return impostos

    def _extrair_icms_cte(self, dados_icms: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai dados do ICMS específico do CTe."""
        # Encontra o tipo de ICMS
        icms_tipo = {}
        chave_icms = None

        for chave, valor in dados_icms.items():
            if chave.startswith('ICMS'):
                icms_tipo = valor
                chave_icms = chave
                break

        return {
            'modalidade': chave_icms,
            'cst': icms_tipo.get('CST'),
            'valor_bc': icms_tipo.get('vBC'),
            'aliquota': icms_tipo.get('pICMS'),
            'valor_icms': icms_tipo.get('vICMS'),
            'percentual_reducao_bc': icms_tipo.get('pRedBC')
        }

    def _extrair_icms_uf_fim(self, dados_uf_fim: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai dados de partilha ICMS UF destino para CTe."""
        return {
            'valor_bc_uf_fim': dados_uf_fim.get('vBCUFFim'),
            'percentual_fcp_uf_fim': dados_uf_fim.get('pFCPUFFim'),
            'percentual_icms_uf_fim': dados_uf_fim.get('pICMSUFFim'),
            'percentual_icms_inter': dados_uf_fim.get('pICMSInter'),
            'valor_fcp_uf_fim': dados_uf_fim.get('vFCPUFFim'),
            'valor_icms_uf_fim': dados_uf_fim.get('vICMSUFFim'),
            'valor_icms_uf_ini': dados_uf_fim.get('vICMSUFIni')
        }

    def _extrair_informacoes_carga(self, dados_carga: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai informações da carga transportada."""
        quantidades = []
        
        # Extrai informações de quantidade
        if 'infQ' in dados_carga:
            inf_q_dados = utils.normalizar_para_lista(dados_carga['infQ'])
            
            for inf_q in inf_q_dados:
                quantidade = {
                    'codigo_unidade': inf_q.get('cUnid'),
                    'tipo_medida': inf_q.get('tpMed'),
                    'quantidade': inf_q.get('qCarga')
                }
                quantidades.append(quantidade)

        return {
            'valor_carga': dados_carga.get('vCarga'),
            'produto_predominante': dados_carga.get('proPred'),
            'valor_carga_averbacao': dados_carga.get('vCargaAverb'),
            'quantidades': quantidades
        }

    def _extrair_informacoes_documentos(self, dados_doc: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai informações dos documentos fiscais relacionados."""
        documentos = {
            'nfes': [],
            'nfs': [],
            'outros': []
        }

        # NFe
        if 'infNFe' in dados_doc:
            nfes_dados = utils.normalizar_para_lista(dados_doc['infNFe'])
            
            for nfe in nfes_dados:
                doc_nfe = {
                    'chave': nfe.get('chave'),
                    'pin': nfe.get('PIN'),
                    'data_prevista_entrega': nfe.get('dPrev')
                }
                documentos['nfes'].append(doc_nfe)

        # NF (Nota Fiscal modelo 1/1A)
        if 'infNF' in dados_doc:
            nfs_dados = utils.normalizar_para_lista(dados_doc['infNF'])
            
            for nf in nfs_dados:
                doc_nf = {
                    'numero_romaneio': nf.get('nRoma'),
                    'numero_pedido': nf.get('nPed'),
                    'modelo': nf.get('mod'),
                    'serie': nf.get('serie'),
                    'numero_nf': nf.get('nDoc'),
                    'data_emissao': nf.get('dEmi'),
                    'valor_bc_icms': nf.get('vBC'),
                    'valor_icms': nf.get('vICMS'),
                    'valor_bc_icms_st': nf.get('vBCST'),
                    'valor_st': nf.get('vST'),
                    'valor_produtos': nf.get('vProd'),
                    'valor_nf': nf.get('vNF'),
                    'cfop': nf.get('nCFOP'),
                    'peso_bruto': nf.get('nPeso')
                }
                documentos['nfs'].append(doc_nf)

        # Outros documentos
        if 'infOutros' in dados_doc:
            outros_dados = utils.normalizar_para_lista(dados_doc['infOutros'])
            
            for outro in outros_dados:
                doc_outro = {
                    'tipo_documento': outro.get('tpDoc'),
                    'descricao': outro.get('descOutros'),
                    'numero_documento': outro.get('nDoc'),
                    'data_emissao': outro.get('dEmi'),
                    'valor_documento': outro.get('vDocFisc'),
                    'data_prevista_entrega': outro.get('dPrev')
                }
                documentos['outros'].append(doc_outro)

        return documentos

    def _extrair_informacoes_modais(self, dados_modal: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai informações específicas do modal de transporte."""
        modal_info = {
            'versao': dados_modal.get('@versaoModal')
        }

        # Modal Rodoviário
        if 'rodo' in dados_modal:
            modal_info['rodoviario'] = self._extrair_modal_rodoviario(dados_modal['rodo'])

        # Modal Aéreo
        if 'aereo' in dados_modal:
            modal_info['aereo'] = self._extrair_modal_aereo(dados_modal['aereo'])

        # Modal Aquaviário
        if 'aquav' in dados_modal:
            modal_info['aquaviario'] = self._extrair_modal_aquaviario(dados_modal['aquav'])

        # Modal Ferroviário
        if 'ferrov' in dados_modal:
            modal_info['ferroviario'] = self._extrair_modal_ferroviario(dados_modal['ferrov'])

        # Modal Dutoviário
        if 'duto' in dados_modal:
            modal_info['dutoviario'] = self._extrair_modal_dutoviario(dados_modal['duto'])

        return modal_info

    def _extrair_modal_rodoviario(self, dados_rodo: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai informações específicas do modal rodoviário."""
        return {
            'rntrc': dados_rodo.get('RNTRC'),
            'codigo_agendamento': dados_rodo.get('codAgPorto'),
            'veiculo_tracao': self._extrair_veiculo(dados_rodo.get('veicTracao', {})),
            'veiculos_reboque': self._extrair_veiculos_reboque(dados_rodo.get('veicReboque', [])),
            'lacres_rodo': self._extrair_lacres_rodo(dados_rodo.get('lacRodo', [])),
            'motoristas': self._extrair_motoristas(dados_rodo.get('moto', []))
        }

    def _extrair_veiculo(self, dados_veiculo: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai dados de veículo de tração ou reboque."""
        if not dados_veiculo:
            return {}

        veiculo = {
            'codigo_interno': dados_veiculo.get('cInt'),
            'placa': dados_veiculo.get('placa'),
            'tara': dados_veiculo.get('tara'),
            'capacidade_kg': dados_veiculo.get('capKG'),
            'capacidade_m3': dados_veiculo.get('capM3'),
            'tipo_rodado': dados_veiculo.get('tpRod'),
            'tipo_carroceria': dados_veiculo.get('tpCar'),
            'uf': dados_veiculo.get('UF')
        }

        # Adiciona proprietário se presente
        if 'prop' in dados_veiculo:
            prop = dados_veiculo['prop']
            proprietario = utils.extrair_identificacao_condicional(prop)
            proprietario.update({
                'razao_social': prop.get('xNome'),
                'inscricao_estadual': prop.get('IE'),
                'uf': prop.get('UF'),
                'tipo_proprietario': prop.get('tpProp')
            })
            veiculo['proprietario'] = proprietario

        return veiculo

    def _extrair_veiculos_reboque(self, dados_reboques: List[Dict]) -> List[Dict[str, Any]]:
        """Extrai dados dos veículos reboque."""
        if not dados_reboques:
            return []

        reboques = []
        dados_normalizados = utils.normalizar_para_lista(dados_reboques)

        for reboque in dados_normalizados:
            dados_reboque = self._extrair_veiculo(reboque)
            if dados_reboque:
                reboques.append(dados_reboque)

        return reboques

    def _extrair_lacres_rodo(self, dados_lacres: List[Dict]) -> List[str]:
        """Extrai números dos lacres rodoviários."""
        if not dados_lacres:
            return []

        lacres = []
        dados_normalizados = utils.normalizar_para_lista(dados_lacres)

        for lacre in dados_normalizados:
            numero_lacre = lacre.get('nLacre')
            if numero_lacre:
                lacres.append(numero_lacre)

        return lacres

    def _extrair_motoristas(self, dados_motoristas: List[Dict]) -> List[Dict[str, Any]]:
        """Extrai dados dos motoristas."""
        if not dados_motoristas:
            return []

        motoristas = []
        dados_normalizados = utils.normalizar_para_lista(dados_motoristas)

        for moto in dados_normalizados:
            motorista = {
                'nome': moto.get('xNome'),
                'numero_cnh': moto.get('CNH')
            }
            
            # Adiciona CPF
            identificacao = utils.extrair_cnpj_cpf_condicional(moto)
            motorista.update(identificacao)
            
            motoristas.append(motorista)

        return motoristas

    def _extrair_modal_aereo(self, dados_aereo: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai informações do modal aéreo."""
        return {
            'numero_operacional_voo': dados_aereo.get('nOCA'),
            'data_prevista_voo': dados_aereo.get('dPrevAereo'),
            'natureza_carga': dados_aereo.get('natCarga'),
            'tarifa_classe': dados_aereo.get('tarifa'),
            'codigo_classe_tarifa': dados_aereo.get('cCl'),
            'codigo_tarifa': dados_aereo.get('cTar'),
            'valor_tarifa': dados_aereo.get('vTar')
        }

    def _extrair_modal_aquaviario(self, dados_aquav: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai informações do modal aquaviário."""
        return {
            'valor_prestacao_basica': dados_aquav.get('vPrest'),
            'valor_afrmm': dados_aquav.get('vAFRMM'),
            'numero_booking': dados_aquav.get('xNavio'),
            'numero_conhecimento': dados_aquav.get('nViag'),
            'direcao': dados_aquav.get('direc'),
            'irin': dados_aquav.get('irin'),
            'balsa': self._extrair_balsa(dados_aquav.get('balsa', [])),
            'detalhamento_containers': self._extrair_containers(dados_aquav.get('detCont', []))
        }

    def _extrair_balsa(self, dados_balsa: List[Dict]) -> List[Dict[str, Any]]:
        """Extrai dados das balsas."""
        if not dados_balsa:
            return []

        balsas = []
        dados_normalizados = utils.normalizar_para_lista(dados_balsa)

        for balsa in dados_normalizados:
            dados_balsa_item = {
                'numero_identificacao': balsa.get('xBalsa')
            }
            balsas.append(dados_balsa_item)

        return balsas

    def _extrair_containers(self, dados_containers: List[Dict]) -> List[Dict[str, Any]]:
        """Extrai detalhamento dos containers."""
        if not dados_containers:
            return []

        containers = []
        dados_normalizados = utils.normalizar_para_lista(dados_containers)

        for container in dados_normalizados:
            dados_container = {
                'numero_container': container.get('nContainer'),
                'lacres_container': self._extrair_lacres_container(container.get('lacre', []))
            }
            containers.append(dados_container)

        return containers

    def _extrair_lacres_container(self, dados_lacres: List[Dict]) -> List[str]:
        """Extrai lacres do container."""
        if not dados_lacres:
            return []

        lacres = []
        dados_normalizados = utils.normalizar_para_lista(dados_lacres)

        for lacre in dados_normalizados:
            numero_lacre = lacre.get('nLacre')
            if numero_lacre:
                lacres.append(numero_lacre)

        return lacres

    def _extrair_modal_ferroviario(self, dados_ferrov: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai informações do modal ferroviário."""
        return {
            'tipo_trafego': dados_ferrov.get('tpTraf'),
            'responsavel_faturamento': dados_ferrov.get('respFat'),
            'ferrovia_origem': dados_ferrov.get('ferrOrig'),
            'ferrovia_destino': dados_ferrov.get('ferrDest'),
            'vagoes': self._extrair_vagoes(dados_ferrov.get('detVag', []))
        }

    def _extrair_vagoes(self, dados_vagoes: List[Dict]) -> List[Dict[str, Any]]:
        """Extrai dados dos vagões."""
        if not dados_vagoes:
            return []

        vagoes = []
        dados_normalizados = utils.normalizar_para_lista(dados_vagoes)

        for vagao in dados_normalizados:
            dados_vagao = {
                'numero_vagao': vagao.get('nVag'),
                'capacidade': vagao.get('cap'),
                'tipo_vagao': vagao.get('tpVag'),
                'peso_real': vagao.get('pesoR'),
                'peso_base_calculo': vagao.get('pesoBC')
            }
            vagoes.append(dados_vagao)

        return vagoes

    def _extrair_modal_dutoviario(self, dados_duto: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai informações do modal dutoviário."""
        return {
            'valor_tarifa': dados_duto.get('vTar'),
            'data_inicio_operacao': dados_duto.get('dIni'),
            'data_fim_operacao': dados_duto.get('dFim')
        }

    def _extrair_complementares(self, dados_compl: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai informações complementares do CTe."""
        complementares = {
            'observacoes_gerais': utils.limpar_texto(dados_compl.get('xObs')),
            'observacoes_contribuinte': [],
            'observacoes_fisco': [],
            'entrega': {},
            'origem_prestacao': {},
            'destino_prestacao': {}
        }

        # Observações do contribuinte
        if 'ObsCont' in dados_compl:
            obs_cont_dados = utils.normalizar_para_lista(dados_compl['ObsCont'])
            
            for obs in obs_cont_dados:
                observacao = {
                    'campo': obs.get('@xCampo'),
                    'texto': utils.limpar_texto(obs.get('xTexto'))
                }
                complementares['observacoes_contribuinte'].append(observacao)

        # Observações do fisco
        if 'ObsFisco' in dados_compl:
            obs_fisco_dados = utils.normalizar_para_lista(dados_compl['ObsFisco'])
            
            for obs in obs_fisco_dados:
                observacao = {
                    'campo': obs.get('@xCampo'),
                    'texto': utils.limpar_texto(obs.get('xTexto'))
                }
                complementares['observacoes_fisco'].append(observacao)

        # Informações de entrega
        if 'Entrega' in dados_compl:
            complementares['entrega'] = self._extrair_entrega(dados_compl['Entrega'])

        # Origem da prestação
        if 'origCalc' in dados_compl:
            complementares['origem_prestacao'] = dados_compl.get('origCalc')

        # Destino da prestação
        if 'destCalc' in dados_compl:
            complementares['destino_prestacao'] = dados_compl.get('destCalc')

        return complementares

    def _extrair_entrega(self, dados_entrega: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai informações de entrega."""
        entrega = {}

        # Entrega com data
        if 'comData' in dados_entrega:
            com_data = dados_entrega['comData']
            entrega['com_data'] = {
                'tipo_periodo': com_data.get('tpPer'),
                'data_programada': com_data.get('dProg'),
                'data_inicial': com_data.get('dIni'),
                'data_final': com_data.get('dFim')
            }

        # Entrega sem data
        if 'semData' in dados_entrega:
            sem_data = dados_entrega['semData']
            entrega['sem_data'] = {
                'tipo_periodo': sem_data.get('tpPer')
            }

        # Entrega com hora
        if 'comHora' in dados_entrega:
            com_hora = dados_entrega['comHora']
            entrega['com_hora'] = {
                'tipo_hora': com_hora.get('tpHor'),
                'hora_programada': com_hora.get('hProg'),
                'hora_inicial': com_hora.get('hIni'),
                'hora_final': com_hora.get('hFim')
            }

        # Entrega sem hora
        if 'semHora' in dados_entrega:
            sem_hora = dados_entrega['semHora']
            entrega['sem_hora'] = {
                'tipo_hora': sem_hora.get('tpHor')
            }

        # No domicílio
        if 'noDom' in dados_entrega:
            entrega['no_domicilio'] = dados_entrega['noDom']

        # Sem data definida
        if 'semData' in dados_entrega:
            entrega['sem_data_definida'] = True

        return entrega

    def _extrair_responsavel_tecnico(self, dados_resp_tec: Dict[str, Any]) -> Dict[str, Any]:
        """Extrai dados do responsável técnico pela emissão."""
        resp_tecnico = {
            'razao_social': dados_resp_tec.get('xContato'),
            'email': dados_resp_tec.get('email'),
            'telefone': dados_resp_tec.get('fone'),
            'codigo_crt': dados_resp_tec.get('CSRT'),
            'hash_csrt': dados_resp_tec.get('hashCSRT')
        }

        # Adiciona CNPJ
        identificacao = utils.extrair_cnpj_cpf_condicional(dados_resp_tec)
        resp_tecnico.update(identificacao)

        return resp_tecnico