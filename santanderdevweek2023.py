# -*- coding: utf-8 -*-
import os
import logging
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
from typing import Optional

# Configuração de Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-d %H:%M:%S'
)

# Carrega variáveis de ambiente
load_dotenv()

class MarketingGenerator:
    """
    Classe responsável por gerenciar a interação com a API de LLM
    para gerar mensagens de marketing.
    """
    
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        self.model = "openai/gpt-4o-mini"
        
        if not self.api_key:
            raise ValueError("A chave da API (OPENROUTER_API_KEY) não foi encontrada nas variáveis de ambiente.")

        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
            default_headers={
                "HTTP-Referer": "https://example.com", 
                "X-Title": "Santander ETL Project"
            }
        )

    def generate_message(self, customer_name: str) -> Optional[str]:
        """
        Gera uma mensagem curta sobre investimentos para um cliente específico.
        """
        try:
            prompt = f"Crie uma mensagem curta (máx. 100 caracteres) sobre a importância dos investimentos para o cliente {customer_name}."
            
            logging.info(f"Gerando mensagem para: {customer_name}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=80,
                temperature=0.7,
            )

            message = response.choices[0].message.content.strip()
            
            # Truncar mensagem se exceder 100 caracteres para manter consistência
            if len(message) > 100:
                message = message[:97] + "..."
            
            return message

        except Exception as error:
            logging.error(f"Falha ao gerar mensagem para {customer_name}. Erro: {error}")
            return None

def extract_data(file_path: str) -> pd.DataFrame:
    """
    Carrega os dados dos usuários a partir de um arquivo CSV.
    """
    try:
        df = pd.read_csv(file_path)
        # Validação básica de colunas
        if 'id' not in df.columns or 'name' not in df.columns:
            raise ValueError("O arquivo CSV deve conter as colunas 'id' e 'name'.")
        logging.info(f"Dados carregados com sucesso. Total de registros: {len(df)}")
        return df
    except FileNotFoundError:
        logging.critical(f"Arquivo não encontrado: {file_path}")
        raise
    except Exception as e:
        logging.critical(f"Erro ao ler CSV: {e}")
        raise

def transform_data(df: pd.DataFrame, generator: MarketingGenerator) -> pd.DataFrame:
    """
    Aplica a geração de IA para cada usuário no DataFrame.
    """
    # Cria uma lista para armazenar os resultados
    news_list = []
    
    for _, row in df.iterrows():
        message = generator.generate_message(row['name'])
        
        if message:
            news_item = {
                "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
                "description": message
            }
            news_list.append(news_item)
        else:
            news_list.append(None)
    
    df['news'] = news_list
    return df

def load_data(df: pd.DataFrame, output_path: str):
    """
    Salva os dados processados em um novo arquivo JSON ou CSV.
    Neste caso, salvando em JSON para preservar a estrutura do objeto 'news'.
    """
    try:
        # Filtra apenas quem teve mensagem gerada com sucesso
        processed_data = df.dropna(subset=['news'])
        
        # Converte para dict orientado a registros para output limpo
        result_list = processed_data.to_dict(orient='records')
        
        import json
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result_list, f, ensure_ascii=False, indent=4)
            
        logging.info(f"Processo finalizado. Dados salvos em: {output_path}")
        
    except Exception as e:
        logging.error(f"Erro ao salvar os dados: {e}")

def main():
    input_file = 'SDW2023.csv'
    output_file = 'SDW2023_processed.json'
    
    try:
        # Inicialização
        generator = MarketingGenerator()
        
        # 1. Extract
        users_df = extract_data(input_file)
        
        # 2. Transform
        users_df_transformed = transform_data(users_df, generator)
        
        # 3. Load
        load_data(users_df_transformed, output_file)
        
    except Exception as e:
        logging.critical(f"A execução do pipeline falhou: {e}")

if __name__ == "__main__":
    main()
