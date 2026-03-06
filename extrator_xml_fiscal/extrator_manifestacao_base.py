from typing import Dict, Any
from abc import abstractmethod
from .extrator_evento_base import ExtratorEventoBase


# Mapeamento de todos os tipos de eventos de manifestação do destinatário
TIPOS_MANIFESTACAO = {
    '210200': 'Confirmação da Operação',
    '210210': 'Ciência da Operação',
    '210220': 'Desconhecimento da Operação',
    '210240': 'Operação não Realizada',
}


class ExtratorManifestacaoBase(ExtratorEventoBase):
    """
    Classe base para extração de eventos de Manifestação do Destinatário.

    Implementa a estrutura comum de processamento dos eventos de manifestação
    e delega a extração de dados específicos para as subclasses.

    Tipos de eventos cobertos:
        - 210200: Confirmação da Operação
        - 210210: Ciência da Operação
        - 210220: Desconhecimento da Operação
        - 210240: Operação não Realizada
    """

    # Deve ser definido por cada subclasse
    TIPO_EVENTO_ESPERADO: str = None

    def _extrair_dados(self, dados_xml: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extrai dados da Manifestação do Destinatário com validação de tipo
        ANTES do processamento.

        Args:
            dados_xml (Dict[str, Any]): XML do evento convertido para dicionário

        Returns:
            Dict[str, Any]: Dados estruturados do evento

        Raises:
            ValueError: Se o tipo de evento não corresponder ao esperado pela subclasse
        """
        # VALIDA TIPO PRIMEIRO - antes de processar qualquer coisa
        raiz_evento = self._encontrar_raiz_evento(dados_xml)
        tipo_evento = raiz_evento.get('tpEvento')

        if tipo_evento != self.TIPO_EVENTO_ESPERADO:
            descricao_esperada = TIPOS_MANIFESTACAO.get(self.TIPO_EVENTO_ESPERADO, self.TIPO_EVENTO_ESPERADO)
            raise ValueError(
                f'Tipo de evento {tipo_evento} não é uma {descricao_esperada} '
                f'(esperado: {self.TIPO_EVENTO_ESPERADO})'
            )

        # Se chegou até aqui, é o tipo correto - processa normalmente
        return {
            'dados_evento': self._extrair_dados_evento(raiz_evento),
            'dados_protocolo': self._extrair_protocolo(dados_xml),
            'dados_especificos': self._extrair_dados_especificos(raiz_evento)
        }

    def _extrair_protocolo(self, dados_xml: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sobrescreve o método da classe pai para incluir campos adicionais
        presentes no retorno dos eventos de manifestação do destinatário:
        xEvento e CNPJDest.

        Args:
            dados_xml (Dict[str, Any]): XML completo do evento

        Returns:
            Dict[str, Any]: Dados do protocolo com campos estendidos
        """
        protocolo = super()._extrair_protocolo(dados_xml)

        if not protocolo:
            return None

        # Extrai os dados brutos do retEvento para capturar campos adicionais
        protocolo_dados = {}
        if 'procEventoNFe' in dados_xml and 'retEvento' in dados_xml['procEventoNFe']:
            protocolo_dados = dados_xml['procEventoNFe']['retEvento'].get('infEvento', {})

        # Adiciona campos específicos dos eventos de manifestação
        protocolo['descricao_evento'] = protocolo_dados.get('xEvento')
        protocolo['cnpj_destinatario'] = protocolo_dados.get('CNPJDest')

        return protocolo

    @abstractmethod
    def _extrair_dados_especificos(self, raiz_evento: Dict[str, Any]) -> Dict[str, Any]:
        """
        Método abstrato para extração de dados específicos de cada tipo
        de manifestação do destinatário.

        Args:
            raiz_evento (Dict[str, Any]): Dados do infEvento

        Returns:
            Dict[str, Any]: Dados específicos do tipo de manifestação
        """
        raise NotImplementedError('Subclasses devem implementar _extrair_dados_especificos()')
