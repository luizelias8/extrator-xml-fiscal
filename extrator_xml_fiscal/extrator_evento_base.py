from typing import Dict, Any, Optional
from abc import abstractmethod
from .extrator_base import ExtratorBase
from . import utils


class ExtratorEventoBase(ExtratorBase):
    """
    Classe base para extração de eventos fiscais.

    Implementa a estrutura comum de processamento de eventos e delega
    a extração de dados específicos para as subclasses.
    """

    def _extrair_dados(self, dados_xml: Dict[str, Any]) -> Dict[str, Any]:
        """
        Template method para extração de dados de eventos fiscais.

        Args:
            dados_xml (Dict[str, Any]): XML do evento convertido para dicionário

        Returns:
            Dict[str, Any]: Dados estruturados do evento
        """
        raiz_evento = self._encontrar_raiz_evento(dados_xml)

        return {
            'dados_evento': self._extrair_dados_evento(raiz_evento),
            'dados_protocolo': self._extrair_protocolo(dados_xml),
            'dados_especificos': self._extrair_dados_especificos(raiz_evento)
        }

    def _encontrar_raiz_evento(self, dados_xml: Dict[str, Any]) -> Dict[str, Any]:
        """
        Encontra a raiz do evento no XML, lidando com diferentes estruturas.

        Args:
            dados_xml (Dict[str, Any]): XML convertido para dicionário

        Returns:
            Dict[str, Any]: Dados do evento (infEvento)

        Raises:
            ValueError: Se estrutura não for reconhecida como evento fiscal
        """
        try:
            # Tenta estrutura padrão de eventos (CCe, etc.)
            if 'procEventoNFe' in dados_xml:
                return dados_xml['procEventoNFe']['evento']['infEvento']

            # Tenta estrutura específica de cancelamento
            elif 'procCancNFe' in dados_xml:
                return dados_xml['procCancNFe']['envEvento']['evento']['infEvento']

            # Tenta evento simples (sem protocolo)
            elif 'evento' in dados_xml:
                return dados_xml['evento']['infEvento']

            else:
                raise ValueError('Estrutura XML não reconhecida como evento fiscal')

        except KeyError as e:
            raise ValueError(f'XML não possui estrutura válida de evento fiscal. Campo ausente: {str(e)}')

    def _extrair_dados_evento(self, raiz_evento: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extrai dados comuns do evento fiscal.

        Args:
            raiz_evento (Dict[str, Any]): Dados do infEvento

        Returns:
            Dict[str, Any]: Dados comuns do evento
        """
        return {
            'id_evento': raiz_evento.get('@Id', ''),
            'codigo_orgao': raiz_evento.get('cOrgao'),
            'ambiente': raiz_evento.get('tpAmb'),
            'cnpj_emissor': raiz_evento.get('CNPJ'),
            'cpf_emissor': raiz_evento.get('CPF'),
            'chave_nfe': raiz_evento.get('chNFe'),
            'data_evento': raiz_evento.get('dhEvento'),
            'tipo_evento': raiz_evento.get('tpEvento'),
            'numero_sequencia': raiz_evento.get('nSeqEvento'),
            'versao_evento': raiz_evento.get('verEvento')
        }

    def _extrair_protocolo(self, dados_xml: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Extrai dados do protocolo de retorno do evento.

        Args:
            dados_xml (Dict[str, Any]): XML completo do evento

        Returns:
            Optional[Dict[str, Any]]: Dados do protocolo se existir
        """
        protocolo_dados = None

        # Tenta encontrar protocolo em procEventoNFe (CCe e outros eventos)
        if 'procEventoNFe' in dados_xml and 'retEvento' in dados_xml['procEventoNFe']:
            protocolo_dados = dados_xml['procEventoNFe']['retEvento'].get('infEvento', {})

        # Tenta encontrar protocolo em procCancNFe (cancelamentos)
        elif 'procCancNFe' in dados_xml and 'retEnvEvento' in dados_xml['procCancNFe']:
            ret_env_evento = dados_xml['procCancNFe']['retEnvEvento']
            if 'retEvento' in ret_env_evento:
                protocolo_dados = ret_env_evento['retEvento'].get('infEvento', {})

        if not protocolo_dados:
            return None

        return {
            'ambiente_protocolo': protocolo_dados.get('tpAmb'),
            'versao_aplicativo': protocolo_dados.get('verAplic'),
            'codigo_orgao': protocolo_dados.get('cOrgao'),
            'codigo_status': protocolo_dados.get('cStat'),
            'motivo': protocolo_dados.get('xMotivo'),
            'chave_nfe': protocolo_dados.get('chNFe'),
            'tipo_evento': protocolo_dados.get('tpEvento'),
            'numero_sequencia': protocolo_dados.get('nSeqEvento'),
            'data_registro': protocolo_dados.get('dhRegEvento'),
            'numero_protocolo': protocolo_dados.get('nProt')
        }

    @abstractmethod
    def _extrair_dados_especificos(self, raiz_evento: Dict[str, Any]) -> Dict[str, Any]:
        """
        Método abstrato para extração de dados específicos do tipo de evento.

        Deve ser implementado por cada subclasse conforme o tipo específico
        de evento fiscal (CCe, Cancelamento, etc.).

        Args:
            raiz_evento (Dict[str, Any]): Dados do infEvento

        Returns:
            Dict[str, Any]: Dados específicos do tipo de evento
        """
        raise NotImplementedError('Subclasses devem implementar _extrair_dados_especificos()')
