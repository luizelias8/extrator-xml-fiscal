from typing import Dict, Any
from .extrator_evento_base import ExtratorEventoBase
from . import utils


class ExtratorMDFeAutorizado(ExtratorEventoBase):
    """
    Extrator específico para o evento MDF-e Autorizado (610610).

    Registrado na NFe para informar que um MDF-e (Manifesto Eletrônico
    de Documentos Fiscais) vinculado à operação foi autorizado pela SEFAZ.

    Processa arquivos XML do evento e extrai os dados do MDF-e
    autorizado e do emitente do manifesto.
    """

    def _extrair_dados(self, dados_xml: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extrai dados do evento MDF-e Autorizado com validação de tipo
        ANTES do processamento.

        Args:
            dados_xml (Dict[str, Any]): XML do evento convertido para dicionário

        Returns:
            Dict[str, Any]: Dados estruturados do evento

        Raises:
            ValueError: Se não for um evento de MDF-e Autorizado
        """
        # VALIDA TIPO PRIMEIRO - antes de processar qualquer coisa
        raiz_evento = self._encontrar_raiz_evento(dados_xml)
        tipo_evento = raiz_evento.get('tpEvento')

        if tipo_evento != '610610':
            raise ValueError(
                f'Tipo de evento {tipo_evento} não é um MDF-e Autorizado '
                f'(esperado: 610610)'
            )

        # Se chegou até aqui, é realmente um MDF-e Autorizado - processa normalmente
        return {
            'dados_evento': self._extrair_dados_evento(raiz_evento),
            'dados_protocolo': self._extrair_protocolo(dados_xml),
            'dados_especificos': self._extrair_dados_especificos(raiz_evento)
        }

    def _extrair_dados_especificos(self, raiz_evento: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extrai dados específicos do evento MDF-e Autorizado.

        Captura os dados do autor do evento, do MDF-e vinculado
        (chave, modal, protocolo, datas) e os dados do emitente
        do manifesto.

        Args:
            raiz_evento (Dict[str, Any]): Dados do infEvento

        Returns:
            Dict[str, Any]: Dados específicos do evento
        """
        det_evento = raiz_evento.get('detEvento', {})
        dados_mdfe = det_evento.get('MDFe', {})
        dados_emit = det_evento.get('emit', {})

        return {
            'descricao_evento': det_evento.get('descEvento'),
            'versao_layout': det_evento.get('@versao'),
            'autor': {
                'codigo_orgao_autor': det_evento.get('cOrgaoAutor'),
                'tipo_autor': det_evento.get('tpAutor'),
                'versao_aplicativo': det_evento.get('verAplic'),
            },
            'mdfe': {
                'chave_mdfe': dados_mdfe.get('chMDFe'),
                'modal': dados_mdfe.get('modal'),
                'data_emissao': dados_mdfe.get('dhEmi'),
                'numero_protocolo': dados_mdfe.get('nProt'),
                'data_recebimento': dados_mdfe.get('dhRecbto'),
            },
            'emitente_mdfe': {
                'cnpj': dados_emit.get('CNPJ'),
                'inscricao_estadual': dados_emit.get('IE'),
                'razao_social': utils.limpar_texto(dados_emit.get('xNome')),
            }
        }
