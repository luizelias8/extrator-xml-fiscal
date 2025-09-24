import xmltodict
import os
from datetime import datetime
from typing import Dict, Any
from abc import ABC, abstractmethod


class ExtratorBase(ABC):
    """
    Classe base para extração de documentos XML fiscais.

    Implementa o Template Method Pattern, definindo o fluxo principal
    de processamento e delegando partes específicas para as subclasses.
    """

    def __init__(self):
        """Inicializa o extrator base."""
        pass

    def processar_arquivo(self, caminho_arquivo: str) -> Dict[str, Any]: # Dict[str, Any] significa que retorna um dicionário cujas chaves são strings (str) e os valores podem ser de qualquer tipo (Any).
        """
        Processa um arquivo XML fiscal seguindo o template method pattern.

        Args:
            caminho_arquivo (str): Caminho para o arquivo XML

        Returns:
            Dict[str, Any]: Dados extraídos e estruturados

        Raises:
            FileNotFoundError: Se o arquivo não for encontrado
            ValueError: Se o arquivo não for um XML válido
            Exception: Para outros erros durante o processamento
        """
        # 1. Validar arquivo
        self._validar_arquivo(caminho_arquivo)

        # 2. Ler e parsear XML
        dados_xml = self._ler_e_parsear_xml(caminho_arquivo)

        # 3. Extrair dados (implemetado pelas subclasses)
        dados_extraidos = self._extrair_dados(dados_xml)

        # 4. Adicionar metadados comuns
        return self._adicionar_metadados(dados_extraidos, caminho_arquivo)

    def _validar_arquivo(self, caminho_arquivo: str) -> None:
        """
        Valida se o arquivo existe e tem extensão XML.

        Args:
            caminho_arquivo (str): Caminho do arquivo

        Raises:
            FileNotFoundError: Se o arquivo não existir
            ValueError: Se extensão não for .xml
        """
        if not os.path.exists(caminho_arquivo):
            raise FileNotFoundError(f'Arquivo não encontrado: {caminho_arquivo}')

        if not caminho_arquivo.lower().endswith('.xml'):
            raise ValueError(f'Arquivo deve ter extensão .xml: {caminho_arquivo}')

    def _ler_e_parsear_xml(self, caminho_arquivo: str) -> Dict[str, Any]:
        """
        Lê e converte o arquivo XML em dicionário Python

        Args:
            caminho_arquivo (str): Caminho do arquivo

        Returns:
            Dict[str, Any]: XML convertido para dicionário

        Raises:
            Exception: Se houver erro na leitura ou parse do XML
        """
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                conteudo_xml = arquivo.read()

            return xmltodict.parse(conteudo_xml)

        except Exception as e:
            raise Exception(f'Erro ao processar arquivo XML: {str(e)}')

    @abstractmethod
    def _extrair_dados(self, dados_xml: Dict[str, Any]) -> Dict[str, Any]:
        """
        Método abstrato para extração de dados específicos do documento.

        Deve ser implementado por cada subclasse conforme a estrutura
        específica do tipo de documento fiscal.

        Args:
            dados_xml: XML convertido para dicionário

        Returns:
            Dict[str, Any]: Dados estruturados extraídos do XML
        """
        raise NotImplementedError('Subclassess devem implementar _extrair_dados()')

    def _adicionar_metadados(self, dados_extraidos: Dict[str, Any], caminho_arquivo: str) -> Dict[str, Any]:
        """
        Adiciona metadados padrão aos dados extraídos

        Args:
            dados_extraidos (Dict[str, Any]): Dados já extraídos
            caminho_arquivo (str): Caminho do arquivo original

        Returns:
            Dict[str, Any]: Dados com metadados adicionados
        """
        return {
            'arquivo_origem': caminho_arquivo,
            'processado_em': datetime.now().isoformat(),
            'tipo_documento': self.__class__.__name__.replace('Extrator', '').upper(),
            **dados_extraidos
        }
