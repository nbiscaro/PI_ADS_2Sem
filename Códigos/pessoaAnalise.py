'''
Juntar os dados que serão utilizados
para o projeto, passando para um arquivo
CSV
Feito por: @Denis Lima
'''

import pandas as pd

df_endereço = pd.read_csv(r"C:\Users\denis\Desktop\fatec_endereco_pessoa_fisica.csv", sep = "|", usecols=[1,2,3])
df_cpf = pd.read_csv(r"C:\Users\denis\Desktop\fatec_pessoa_fisica.csv", sep = "|", usecols=[1,2,3,4])
df_modelo = pd.DataFrame(columns = ['doc_cli', 'idc_sexo', 'ano_data_nascimento', 'nom_cidade', 'des_estado'])

for index in range(len(df_endereço.index)):
    cidade = df_endereço.iloc[index, 1].strip()
    for index2 in range(len(df_cpf.index)):
        ano = df_cpf.iloc[index2, 3].strip()
        if (df_endereço.iloc[index, 0] == df_cpf.iloc[index2, 0] and ano != 'NULL' and cidade != 'CIDADE NAO ENCONTRADA'):
            df_modelo.loc[0] = [df_cpf.iloc[index2,1], df_cpf.iloc[index2, 2].strip(), df_cpf.iloc[index2, 3].strip(), df_endereço.iloc[index, 1].strip(), df_endereço.iloc[index, 2].strip()]
            df_modelo.index = df_modelo.index + 1
df_modelo = df_modelo.sort_index()

df_modelo.to_csv('pessoa.csv', index=False, header=True, sep="|")
