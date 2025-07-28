from datetime import datetime
import os
from transform.processar_dados import coletar_imoveis_processados, salvar_csvs, salvar_parquets, criar_pastas

if __name__ == "__main__":
    # 1. Executa o crawler
    date_YMD = datetime.now().strftime("%Y_%m_%d")
    date_HMS = datetime.now().strftime("%H_%M_%S")
    base_path = criar_pastas(date_YMD, date_HMS)
    print(f"Iniciando o pipeline de scraping para EvidenceImoveis - {date_YMD} {date_HMS}")

    raw_path_evidence = f"{base_path}/raw/{date_HMS}/EvidenceImoveis.json"
    os.system(f"scrapy crawl EvidenceImoveis -o {raw_path_evidence}")

    # 2. Processa e transforma
    df_imovel, df_endereco, df_caracteristicas = coletar_imoveis_processados(raw_path_evidence)

    # 3. Salva os CSVs finais (prontos para análise ou carga no banco)
    salvar_csvs(df_imovel, df_endereco, df_caracteristicas, date_YMD, date_HMS)
    salvar_parquets(df_imovel, df_endereco, df_caracteristicas, date_YMD, date_HMS)
    print("Pipeline finalizado!")