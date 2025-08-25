#!/usr/bin/env python3
"""
Script para comparar dados ENTSO-E vs OMIE
Compara os arquivos já processados e salvos
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

def load_entsoe_data():
    """Carrega dados ENTSO-E processados"""
    print("📊 Carregando dados ENTSO-E...")
    
    pt_prices = pd.read_csv('entsoe_data/ENTSOE_Precos_PT_Semana_2025-08-10_a_2025-08-16.csv', index_col=0)
    pt_prices.index = pd.to_datetime(pt_prices.index)
    
    es_prices = pd.read_csv('entsoe_data/ENTSOE_Precos_ES_Semana_2025-08-10_a_2025-08-16.csv', index_col=0)
    es_prices.index = pd.to_datetime(es_prices.index)
    
    print(f"✅ ENTSO-E carregado: {len(pt_prices)} registros PT, {len(es_prices)} registros ES")
    
    return pt_prices, es_prices

def load_omie_data():
    """Carrega dados OMIE processados"""
    print("📊 Carregando dados OMIE...")
    
    omie_data = pd.read_csv('omie_data/OMIE_Precos_Processados_10_08_a_16_08_2025.csv')
    omie_data['datetime_utc'] = pd.to_datetime(omie_data['datetime_utc'])
    omie_data.set_index('datetime_utc', inplace=True)
    
    print(f"✅ OMIE carregado: {len(omie_data)} registros")
    
    return omie_data

def compare_prices(entsoe_pt, entsoe_es, omie_data):
    """Compara preços entre ENTSO-E e OMIE"""
    print("\n🔍 COMPARANDO PREÇOS ENTSO-E vs OMIE")
    print("="*60)
    
    common_index = entsoe_pt.index.intersection(omie_data.index)
    
    if len(common_index) == 0:
        print("❌ Nenhum período comum encontrado!")
        return None
    
    print(f"📅 Período comum: {len(common_index)} registros")
    print(f"📅 De: {common_index.min()}")
    print(f"📅 Até: {common_index.max()}")
    
    entsoe_pt_aligned = entsoe_pt.loc[common_index]
    entsoe_es_aligned = entsoe_es.loc[common_index]
    omie_aligned = omie_data.loc[common_index]
    
    print("\n🇵🇹 COMPARAÇÃO PORTUGAL:")
    print("-" * 40)
    
    pt_diff = entsoe_pt_aligned['price_eur_mwh'] - omie_aligned['price_pt_omie']
    pt_corr = entsoe_pt_aligned['price_eur_mwh'].corr(omie_aligned['price_pt_omie'])
    
    print(f"📊 Diferença média: {pt_diff.mean():.2f} EUR/MWh")
    print(f"📊 Diferença máxima: {pt_diff.max():.2f} EUR/MWh")
    print(f"📊 Diferença mínima: {pt_diff.min():.2f} EUR/MWh")
    print(f"📊 Desvio padrão: {pt_diff.std():.2f} EUR/MWh")
    print(f"📈 Correlação: {pt_corr:.4f}")
    
    print("\n🇪🇸 COMPARAÇÃO ESPANHA:")
    print("-" * 40)
    
    es_diff = entsoe_es_aligned['price_eur_mwh'] - omie_aligned['price_es_omie']
    es_corr = entsoe_es_aligned['price_eur_mwh'].corr(omie_aligned['price_es_omie'])
    
    print(f"📊 Diferença média: {es_diff.mean():.2f} EUR/MWh")
    print(f"📊 Diferença máxima: {es_diff.max():.2f} EUR/MWh")
    print(f"📊 Diferença mínima: {es_diff.min():.2f} EUR/MWh")
    print(f"📊 Desvio padrão: {es_diff.std():.2f} EUR/MWh")
    print(f"📈 Correlação: {es_corr:.4f}")
    
    return {
        'pt_diff': pt_diff,
        'es_diff': es_diff,
        'pt_corr': pt_corr,
        'es_corr': es_corr,
        'common_index': common_index
    }

def create_comparison_report(entsoe_pt, entsoe_es, omie_data, comparison_results):
    """Cria relatório de comparação"""
    print("\n📋 CRIANDO RELATÓRIO DE COMPARAÇÃO...")
    
    report_dir = 'comparison_reports'
    os.makedirs(report_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"{report_dir}/comparison_report_{timestamp}.csv"
    
    common_index = comparison_results['common_index']
    entsoe_pt_aligned = entsoe_pt.loc[common_index]
    entsoe_es_aligned = entsoe_es.loc[common_index]
    omie_aligned = omie_data.loc[common_index]
    
    comparison_df = pd.DataFrame({
        'datetime_utc': common_index,
        'entsoe_pt_price': entsoe_pt_aligned['price_eur_mwh'],
        'omie_pt_price': omie_aligned['price_pt_omie'],
        'pt_difference': comparison_results['pt_diff'],
        'entsoe_es_price': entsoe_es_aligned['price_eur_mwh'],
        'omie_es_price': omie_aligned['price_es_omie'],
        'es_difference': comparison_results['es_diff']
    })
    
    comparison_df.to_csv(report_file, index=False)
    
    print(f"💾 Relatório salvo: {report_file}")
    
    return comparison_df

def print_summary_statistics(comparison_results):
    """Imprime estatísticas resumidas"""
    print("\n📊 RESUMO ESTATÍSTICO")
    print("="*60)
    
    pt_diff = comparison_results['pt_diff']
    es_diff = comparison_results['es_diff']
    
    print("🇵🇹 PORTUGAL:")
    print(f"   Correlação: {comparison_results['pt_corr']:.4f}")
    print(f"   Diferença média: {pt_diff.mean():.2f} EUR/MWh")
    print(f"   RMSE: {np.sqrt((pt_diff**2).mean()):.2f} EUR/MWh")
    
    print("\n🇪🇸 ESPANHA:")
    print(f"   Correlação: {comparison_results['es_corr']:.4f}")
    print(f"   Diferença média: {es_diff.mean():.2f} EUR/MWh")
    print(f"   RMSE: {np.sqrt((es_diff**2).mean()):.2f} EUR/MWh")
    
    print("\n🎯 INTERPRETAÇÃO:")
    if comparison_results['pt_corr'] > 0.95 and comparison_results['es_corr'] > 0.95:
        print("✅ Correlação muito alta - dados muito similares")
    elif comparison_results['pt_corr'] > 0.8 and comparison_results['es_corr'] > 0.8:
        print("✅ Correlação alta - dados similares")
    else:
        print("⚠️  Correlação moderada - diferenças significativas")
    
    print("="*60)

def main():
    """Função principal"""
    print("🌍 COMPARAÇÃO ENTSO-E vs OMIE")
    print("="*60)
    print("📅 Período: 10/08/2025 a 16/08/2025")
    print("🕐 Timezone: UTC")
    print("="*60)
    
    try:
        entsoe_pt, entsoe_es = load_entsoe_data()
        omie_data = load_omie_data()
        
        comparison_results = compare_prices(entsoe_pt, entsoe_es, omie_data)
        
        if comparison_results:
            comparison_df = create_comparison_report(entsoe_pt, entsoe_es, omie_data, comparison_results)
            
            print_summary_statistics(comparison_results)
            
            print("\n🎉 Comparação concluída com sucesso!")
            print("📁 Arquivos gerados:")
            print("   - Relatório: comparison_reports/comparison_report_[timestamp].csv")
            print("   - Dados ENTSO-E: entsoe_data/")
            print("   - Dados OMIE: omie_data/")
            
        else:
            print("❌ Falha na comparação!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()

