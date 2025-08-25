#!/usr/bin/env python3
"""
Script para processar dados OMIE e converter para UTC
Converte arquivos .TXT do OMIE para CSV com timezone UTC
"""

import pandas as pd
import os
import re
from datetime import datetime, timedelta
import pytz

def parse_omie_file(file_path):
    """
    Parse um arquivo OMIE .TXT e extrai os preços
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        date_match = re.search(r'(\d{2}/\d{2}/\d{4})', content)
        if not date_match:
            print(f"❌ Não foi possível extrair a data do arquivo: {file_path}")
            return None
        
        file_date = datetime.strptime(date_match.group(1), '%d/%m/%Y')
    
        lines = content.split('\n')
        prices_es = None
        prices_pt = None
        
        for i, line in enumerate(lines):
            if 'Precio marginal en el sistema espa' in line:
                prices_text = line.split(';')[1:]
                prices_es = []
                for price_str in prices_text:
                    if price_str.strip():
                        try:
                            price_clean = price_str.strip().replace(',', '.')
                            price = float(price_clean)
                            prices_es.append(price)
                        except ValueError:
                            continue
                break
        
        for i, line in enumerate(lines):
            if 'Precio marginal en el sistema portugu' in line:
                prices_text = line.split(';')[1:]
                prices_pt = []
                for price_str in prices_text:
                    if price_str.strip():
                        try:
                            price_clean = price_str.strip().replace(',', '.')
                            price = float(price_clean)
                            prices_pt.append(price)
                        except ValueError:
                            continue
                break
        
        if not prices_es or not prices_pt:
            print(f"❌ Não foi possível extrair preços do arquivo: {file_path}")
            return None
        
        data = []
        for hour in range(24):
            if hour < len(prices_es) and hour < len(prices_pt):
                # Converter para UTC -- Horario da ENTSOE   
                local_time = datetime(file_date.year, file_date.month, file_date.day, hour, 0, 0)
                cest_tz = pytz.timezone('Europe/Madrid')
                utc_tz = pytz.UTC
            
                local_time = cest_tz.localize(local_time, is_dst=True)
                utc_time = local_time.astimezone(utc_tz)
                
                data.append({
                    'datetime_utc': utc_time,
                    'price_es_omie': prices_es[hour],
                    'price_pt_omie': prices_pt[hour],
                    'date': file_date.date(),
                    'hour_local': hour,
                    'data_source': 'OMIE'
                })
        
        return pd.DataFrame(data)
        
    except Exception as e:
        print(f"❌ Erro ao processar arquivo {file_path}: {e}")
        return None

def process_all_omie_files():
    """
    Processa todos os arquivos OMIE na pasta dadosomie
    """
    print("🔄 PROCESSANDO DADOS OMIE")
    print("="*50)
    
    omie_dir = 'dadosomie'
    if not os.path.exists(omie_dir):
        print(f"❌ Pasta {omie_dir} não encontrada!")
        return None
    
    txt_files = [f for f in os.listdir(omie_dir) if f.endswith('.TXT')]
    txt_files.sort()  # Ordenar por data
    
    print(f"📁 Encontrados {len(txt_files)} arquivos OMIE")
    
    all_data = []
    
    for file_name in txt_files:
        file_path = os.path.join(omie_dir, file_name)
        print(f"📄 Processando: {file_name}")
        
        df = parse_omie_file(file_path)
        if df is not None:
            all_data.append(df)
            print(f"   ✅ {len(df)} registros extraídos")
        else:
            print(f"   ❌ Falha ao processar")
    
    if not all_data:
        print("❌ Nenhum dado foi processado com sucesso!")
        return None
    
    combined_df = pd.concat(all_data, ignore_index=True)
    combined_df = combined_df.sort_values('datetime_utc').reset_index(drop=True)
    
    print(f"\n✅ Total de registros processados: {len(combined_df)}")
    print(f"📅 Período: {combined_df['datetime_utc'].min()} a {combined_df['datetime_utc'].max()}")
    
    return combined_df

def save_omie_data(df):
    """
    Salva os dados OMIE processados
    """
    if df is None:
        return
    
    output_dir = 'omie_data'
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, 'OMIE_Precos_Processados_10_08_a_16_08_2025.csv')
    df.to_csv(output_file, index=False)
    
    print(f"\n💾 Dados salvos em: {output_file}")
    
    # Estatísticas
    print("\n📊 ESTATÍSTICAS OMIE:")
    print("-" * 30)
    print(f"🇪🇸 Espanha:")
    print(f"   Média: {df['price_es_omie'].mean():.2f} EUR/MWh")
    print(f"   Mínimo: {df['price_es_omie'].min():.2f} EUR/MWh")
    print(f"   Máximo: {df['price_es_omie'].max():.2f} EUR/MWh")
    
    print(f"\n🇵🇹 Portugal:")
    print(f"   Média: {df['price_pt_omie'].mean():.2f} EUR/MWh")
    print(f"   Mínimo: {df['price_pt_omie'].min():.2f} EUR/MWh")
    print(f"   Máximo: {df['price_pt_omie'].max():.2f} EUR/MWh")
    
    return output_file

def main():
    """
    Função principal
    """
    print("🌍 PROCESSAMENTO DE DADOS OMIE")
    print("="*50)
    print("📅 Período: 10/08/2025 a 16/08/2025")
    print("🕐 Conversão: CEST → UTC")
    print("="*50)
    
    omie_df = process_all_omie_files()
    
    if omie_df is not None:
        output_file = save_omie_data(omie_df)
        
        print(f"\n🎉 Processamento concluído!")
        print(f"📁 Arquivo gerado: {output_file}")
        print(f"📊 Pronto para comparação com dados ENTSO-E!")
        
        return omie_df
    else:
        print("❌ Falha no processamento!")
        return None

if __name__ == "__main__":
    main()
