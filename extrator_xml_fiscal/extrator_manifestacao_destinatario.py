from typing import Dict, Any
from .extrator_manifestacao_base import ExtratorManifestacaoBase
from . import utils


class ExtratorConfirmacaoOperacao(ExtratorManifestacaoBase):
    """
    Extrator específico para Confirmação da Operação (210200).

    O destinatário confirma que a operação descrita na NFe ocorreu
    efetivamente conforme informado pelo emitente.
    """

    TIPO_EVENTO_ESPERADO = '210200'

    def _extrair_dados_especificos(self, raiz_evento: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extrai dados específicos da Confirmação da Operação.

        Args:
            raiz_evento (Dict[str, Any]): Dados do infEvento

        Returns:
            Dict[str, Any]: Dados específicos do evento
        """
        det_evento = raiz_evento.get('detEvento', {})

        return {
            'descricao_evento': det_evento.get('descEvento'),
            'versao_layout': det_evento.get('@versao')
        }


class ExtratorCienciaOperacao(ExtratorManifestacaoBase):
    """
    Extrator específico para Ciência da Operação (210210).

    O destinatário declara ter ciência de uma operação, sem confirmá-la,
    geralmente utilizado para consultar a NFe antes de sua chegada.
    """

    TIPO_EVENTO_ESPERADO = '210210'

    def _extrair_dados_especificos(self, raiz_evento: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extrai dados específicos da Ciência da Operação.

        Args:
            raiz_evento (Dict[str, Any]): Dados do infEvento

        Returns:
            Dict[str, Any]: Dados específicos do evento
        """
        det_evento = raiz_evento.get('detEvento', {})

        return {
            'descricao_evento': det_evento.get('descEvento'),
            'versao_layout': det_evento.get('@versao')
        }


class ExtratorDesconhecimentoOperacao(ExtratorManifestacaoBase):
    """
    Extrator específico para Desconhecimento da Operação (210220).

    O destinatário declara não ter conhecimento de uma operação
    vinculada ao seu CNPJ, podendo indicar emissão indevida.
    """

    TIPO_EVENTO_ESPERADO = '210220'

    def _extrair_dados_especificos(self, raiz_evento: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extrai dados específicos do Desconhecimento da Operação.

        Args:
            raiz_evento (Dict[str, Any]): Dados do infEvento

        Returns:
            Dict[str, Any]: Dados específicos do evento
        """
        det_evento = raiz_evento.get('detEvento', {})

        return {
            'descricao_evento': det_evento.get('descEvento'),
            'versao_layout': det_evento.get('@versao')
        }


class ExtratorOperacaoNaoRealizada(ExtratorManifestacaoBase):
    """
    Extrator específico para Operação não Realizada (210240).

    O destinatário declara que a operação descrita na NFe não foi
    realizada, informando obrigatoriamente uma justificativa.
    """

    TIPO_EVENTO_ESPERADO = '210240'

    def _extrair_dados_especificos(self, raiz_evento: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extrai dados específicos da Operação não Realizada.

        Diferente dos demais eventos de manifestação, este tipo exige
        o campo xJust (justificativa) preenchido pelo destinatário.

        Args:
            raiz_evento (Dict[str, Any]): Dados do infEvento

        Returns:
            Dict[str, Any]: Dados específicos do evento
        """
        det_evento = raiz_evento.get('detEvento', {})

        return {
            'descricao_evento': det_evento.get('descEvento'),
            'justificativa': utils.limpar_texto(det_evento.get('xJust')),
            'versao_layout': det_evento.get('@versao')
        }
