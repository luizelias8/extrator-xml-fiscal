from typing import Dict, Any
from .extrator_evento_base import ExtratorEventoBase
from . import utils


class ExtratorCTeAutorizado(ExtratorEventoBase):
    """
    Extrator específico para o evento CT-e Autorizado (610600).

    Registrado na NFe pelo destinatário para informar que um CT-e
    vinculado à operação foi autorizado pela SEFAZ.

    Processa arquivos XML do evento e extrai os dados do CT-e
    autorizado e do emitente do transporte.
    """

    def _extrair_dados(self, dados_xml: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extrai dados do evento CT-e Autorizado com validação de tipo
        ANTES do processamento.

        Args:
            dados_xml (Dict[str, Any]): XML do evento convertido para dicionário

        Returns:
            Dict[str, Any]: Dados estruturados do evento

        Raises:
            ValueError: Se não for um evento de CT-e Autorizado
        """
        # VALIDA TIPO PRIMEIRO - antes de processar qualquer coisa
        raiz_evento = self._encontrar_raiz_evento(dados_xml)
        tipo_evento = raiz_evento.get('tpEvento')

        if tipo_evento != '610600':
            raise ValueError(
                f'Tipo de evento {tipo_evento} não é um CT-e Autorizado (esperado: 610600)'
            )

        # Se chegou até aqui, é realmente um CT-e Autorizado - processa normalmente
        return {
            'dados_evento': self._extrair_dados_evento(raiz_evento),
            'dados_protocolo': self._extrair_protocolo(dados_xml),
            'dados_especificos': self._extrair_dados_especificos(raiz_evento)
        }

    def _extrair_protocolo(self, dados_xml: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sobrescreve o método da classe pai para incluir CNPJDest,
        presente no retEvento deste tipo de evento.

        Args:
            dados_xml (Dict[str, Any]): XML completo do evento

        Returns:
            Dict[str, Any]: Dados do protocolo com campos estendidos
        """
        protocolo = super()._extrair_protocolo(dados_xml)

        if not protocolo:
            return None

        protocolo_dados = {}
        if 'procEventoNFe' in dados_xml and 'retEvento' in dados_xml['procEventoNFe']:
            protocolo_dados = dados_xml['procEventoNFe']['retEvento'].get('infEvento', {})

        protocolo['cnpj_destinatario'] = protocolo_dados.get('CNPJDest')

        return protocolo

    def _extrair_dados_especificos(self, raiz_evento: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extrai dados específicos do evento CT-e Autorizado.

        Captura os dados do CT-e vinculado (chave, modal, protocolo,
        datas) e os dados do emitente do transporte.

        Args:
            raiz_evento (Dict[str, Any]): Dados do infEvento

        Returns:
            Dict[str, Any]: Dados específicos do evento
        """
        det_evento = raiz_evento.get('detEvento', {})
        dados_cte = det_evento.get('CTe', {})
        dados_emit = det_evento.get('emit', {})

        return {
            'descricao_evento': det_evento.get('descEvento'),
            'versao_layout': det_evento.get('@versao'),
            'cte': {
                'chave_cte': dados_cte.get('chCTe'),
                'modal': dados_cte.get('modal'),
                'data_emissao': dados_cte.get('dhEmi'),
                'numero_protocolo': dados_cte.get('nProt'),
                'data_recebimento': dados_cte.get('dhRecbto'),
            },
            'emitente_cte': {
                'cnpj': dados_emit.get('CNPJ'),
                'inscricao_estadual': dados_emit.get('IE'),
                'razao_social': utils.limpar_texto(dados_emit.get('xNome')),
            }
        }
