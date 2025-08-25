#!/usr/bin/env python3
"""
Simple ENTSO-E Data Fetcher - CSV Version
Busca dados da ENTSO-E e salva em CSV para evitar problemas de timezone
"""

import pandas as pd
from entsoe import EntsoePandasClient
from datetime import datetime, timedelta
import os
import logging
from dotenv import load_dotenv

load_dotenv('config.env')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Main function to fetch ENTSO-E data and save to CSV"""
    
    try:
        API_KEY = os.getenv('ENTSOE_API_KEY')
        if not API_KEY:
            print("❌ ERRO: Configure ENTSOE_API_KEY no arquivo config.env")
            return
    
        client = EntsoePandasClient(api_key=API_KEY)
        
        #10/08/2025 to 16/08/2025
        start = pd.Timestamp('2025-08-10', tz='Europe/Madrid')
        end = pd.Timestamp('2025-08-16', tz='Europe/Madrid')
        
        countries = {'Portugal': 'PT', 'Spain': 'ES'}
        
        output_dir = 'entsoe_data'
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"🌍 Buscando dados da ENTSO-E para o período: {start.date()} a {end.date()}")
        print("="*60)
        
        all_files = []
        
        for country_name, country_code in countries.items():
            print(f"\n🇪🇸🇵🇹 Processando: {country_name} ({country_code})")
            
            try:
                print(f"💰 Buscando preços day-ahead...")
                prices = client.query_day_ahead_prices(country_code, start=start, end=end)
                
                if prices is not None and not prices.empty:
                    prices_df = pd.DataFrame(prices, columns=['price_eur_mwh'])
                    prices_df['country_code'] = country_code
                    prices_df['data_source'] = 'ENTSO-E'
                    prices_df['data_type'] = 'day_ahead_prices'
                    prices_df['fetch_timestamp'] = datetime.now()
                    
                    filename = f"ENTSOE_Precos_{country_code}_Semana_{start.date()}_a_{end.date()}.csv"
                    filepath = os.path.join(output_dir, filename)
                    prices_df.to_csv(filepath, index=True)
                    all_files.append(filepath)
                    
                    print(f"✅ Preços salvos: {filename} ({len(prices_df)} registros)")
                    print(f"   📈 Preço médio: {prices_df['price_eur_mwh'].mean():.2f} EUR/MWh")
                    print(f"   📊 Preço mínimo: {prices_df['price_eur_mwh'].min():.2f} EUR/MWh")
                    print(f"   📈 Preço máximo: {prices_df['price_eur_mwh'].max():.2f} EUR/MWh")
                else:
                    print(f"⚠️ Nenhum dado de preços encontrado para {country_code}")
                    
            except Exception as e:
                print(f"❌ Erro ao buscar preços para {country_code}: {e}")
            
            try:
                print(f"⚡ Buscando dados de geração...")
                generation = client.query_generation(country_code, start=start, end=end)
                
                if generation is not None and not generation.empty:
                    generation_clean = generation.dropna(axis=1, how='all')
                    generation_clean['country_code'] = country_code
                    generation_clean['data_source'] = 'ENTSO-E'
                    generation_clean['data_type'] = 'generation'
                    generation_clean['fetch_timestamp'] = datetime.now()
                    
                    filename = f"ENTSOE_Geracao_{country_code}_Semana_{start.date()}_a_{end.date()}.csv"
                    filepath = os.path.join(output_dir, filename)
                    generation_clean.to_csv(filepath, index=True)
                    all_files.append(filepath)
                    
                    print(f"✅ Geração salva: {filename} ({len(generation_clean.columns)-4} tipos)")
                    
                    gen_types = [col for col in generation_clean.columns if col not in ['country_code', 'data_source', 'data_type', 'fetch_timestamp']]
                    print(f"   🔋 Tipos: {', '.join(gen_types[:5])}{'...' if len(gen_types) > 5 else ''}")
                else:
                    print(f"⚠️ Nenhum dado de geração encontrado para {country_code}")
                    
            except Exception as e:
                print(f"❌ Erro ao buscar geração para {country_code}: {e}")
        
        print("\n" + "="*60)
        print("📋 RESUMO")
        print("="*60)
        print(f"📅 Período: {start.date()} a {end.date()}")
        print(f"🌍 Países: {', '.join(countries.values())}")
        print(f"📁 Arquivos criados: {len(all_files)}")
        print(f"📂 Pasta: {output_dir}/")
        print("\n📄 Arquivos:")
        for file in all_files:
            print(f"   - {os.path.basename(file)}")
        print("="*60)
        
        print("\n🎉 Busca de dados concluída com sucesso!")
        print("💡 Dica: Os arquivos CSV podem ser abertos no Excel ou outros programas")
        
    except Exception as e:
        logger.error(f"❌ Erro na execução: {e}")
        raise

if __name__ == "__main__":
    main()

