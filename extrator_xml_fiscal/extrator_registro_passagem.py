from typing import Dict, Any
from .extrator_evento_base import ExtratorEventoBase
from . import utils


class ExtratorRegistroPassagem(ExtratorEventoBase):
    """
    Extrator específico para o evento Registro de Passagem de NFe (610500).

    Registrado por postos fiscais de fronteira estadual quando uma carga
    em trânsito é detectada, contendo dados do posto, do operador,
    indicadores da passagem e informações do veículo transportador.
    """

    def _extrair_dados(self, dados_xml: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extrai dados do Registro de Passagem com validação de tipo
        ANTES do processamento.

        Args:
            dados_xml (Dict[str, Any]): XML do evento convertido para dicionário

        Returns:
            Dict[str, Any]: Dados estruturados do evento

        Raises:
            ValueError: Se não for um evento de Registro de Passagem
        """
        # VALIDA TIPO PRIMEIRO - antes de processar qualquer coisa
        raiz_evento = self._encontrar_raiz_evento(dados_xml)
        tipo_evento = raiz_evento.get('tpEvento')

        if tipo_evento != '610500':
            raise ValueError(
                f'Tipo de evento {tipo_evento} não é um Registro de Passagem de NFe '
                f'(esperado: 610500)'
            )

        # Se chegou até aqui, é realmente um Registro de Passagem - processa normalmente
        return {
            'dados_evento': self._extrair_dados_evento(raiz_evento),
            'dados_protocolo': self._extrair_protocolo(dados_xml),
            'dados_especificos': self._extrair_dados_especificos(raiz_evento)
        }

    def _extrair_dados_especificos(self, raiz_evento: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extrai dados específicos do Registro de Passagem de NFe.

        Captura os dados do posto fiscal, do operador responsável pelo
        registro, os indicadores da passagem e as informações do veículo
        no modal rodoviário.

        Args:
            raiz_evento (Dict[str, Any]): Dados do infEvento

        Returns:
            Dict[str, Any]: Dados específicos do evento
        """
        det_evento = raiz_evento.get('detEvento', {})
        modal_rodov = det_evento.get('modalRodov', {})

        return {
            'descricao_evento': det_evento.get('descEvento'),
            'versao_layout': det_evento.get('@versao'),
            'posto_fiscal': {
                'codigo_orgao_autor': det_evento.get('cOrgaoAutor'),
                'codigo_posto': det_evento.get('cPostoUF'),
                'nome_posto': utils.limpar_texto(det_evento.get('xPostoUF')),
            },
            'operador': {
                'cpf': det_evento.get('CPFOper'),
                'nome': utils.limpar_texto(det_evento.get('xNomeOper')),
            },
            'passagem': {
                'data_passagem': det_evento.get('dhPas'),
                'offline': det_evento.get('indOffline'),
                'sentido_via': det_evento.get('sentidoVia'),
                'indicador_retorno': det_evento.get('indRet'),
            },
            'veiculo': {
                'placa': det_evento.get('modalRodov', {}).get('placaVeic'),
                'uf': modal_rodov.get('UFVeic'),
            }
        }
