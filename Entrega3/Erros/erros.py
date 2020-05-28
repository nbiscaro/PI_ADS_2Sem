import tkinter as tk
from tkinter import filedialog
import pandas as pd

def Caminho():
    """

    :return: Retorna o caminho do arquivo
    """
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path

def AnalisarFontes():
    """

    :return: Cria csv dos dados
    """
    df_fontes = pd.read_excel(Caminho())
    df_fontes = df_fontes.rename(columns={"NOM_RAZ_SCL": "RAZÃO_SOCIAL", "ID_STG_FNT_ITT": "ID"})
    if df_fontes['NUM_CNPJ'].dtypes != 'object':
        df_fontes['NUM_CNPJ'] = df_fontes.NUM_CNPJ.astype('str')
    if df_fontes['NUM_CMP_CNPJ'].dtypes != 'object':
        df_fontes['NUM_CMP_CNPJ'] = df_fontes.NUM_CMP_CNPJ.astype('str')
    df_fontes['CNPJ'] = df_fontes['NUM_CNPJ'] + df_fontes['NUM_CMP_CNPJ']
    df_fontes = df_fontes[['ID', 'CNPJ', 'RAZÃO_SOCIAL', 'NUM_CNPJ', 'NUM_CMP_CNPJ', 'NOM_COM']]

    '''Validando CNPJ por quantidade (14) e nulos'''
    cnpjInvalido = df_fontes.loc[(df_fontes['CNPJ'].str.len()) != 14, ['ID', 'CNPJ', 'RAZÃO_SOCIAL']]
    cnpjInvalido['MOTIVO'] = 'CNPJ INVÁLIDO'
    cnpjNulo = df_fontes[df_fontes.NUM_CNPJ.isnull()]
    cnpjCmpNulo = df_fontes[df_fontes.NUM_CMP_CNPJ.isnull()]
    cnpjNulo = pd.concat([cnpjNulo, cnpjCmpNulo])
    cnpjNulo = cnpjNulo.drop(['NUM_CNPJ', 'NUM_CMP_CNPJ', 'NOM_COM'], axis=1)
    cnpjNulo['MOTIVO'] = 'CNPJ/COMP NULO'

    '''Nome e razão social nulos'''
    nomeNulo = df_fontes[df_fontes.NOM_COM.isnull()]
    nomeRazSlcNulo = df_fontes[df_fontes.RAZÃO_SOCIAL.isnull()]
    nomeNulo = pd.concat([nomeNulo, nomeRazSlcNulo])
    nomeNulo = nomeNulo.drop(['NUM_CNPJ', 'NUM_CMP_CNPJ', 'NOM_COM'], axis=1)
    nomeNulo['MOTIVO'] = 'NOME NULO'

    '''Verificar duplicidade nos cnpj's e razão social'''
    cnpjDupl = df_fontes.loc[(df_fontes['CNPJ'].duplicated()), ['ID', 'CNPJ', 'RAZÃO_SOCIAL']]
    cnpjDupl['MOTIVO'] = 'CNPJ DUPLICADO'
    nomeDupl = df_fontes.loc[(df_fontes['RAZÃO_SOCIAL'].duplicated()), ['ID', 'CNPJ', 'RAZÃO_SOCIAL']]
    nomeDupl['MOTIVO'] = 'NOME DUPLICADO'

    '''Armazenar todas as linhas de dados corretas'''
    corretos = df_fontes.drop_duplicates('RAZÃO_SOCIAL')
    corretos = corretos.drop(['NUM_CNPJ', 'NUM_CMP_CNPJ', 'NOM_COM'], axis=1)
    corretos = corretos.loc[df_fontes['CNPJ'].str.len() == 14]
    for index in range(len(corretos.index)):
        for index2 in range(len(cnpjDupl.index)):
            if (corretos.iloc[index, 1] == cnpjDupl.iloc[index2, 1]):
                corretos = corretos.drop(index)

    '''Armazenar todos os erros em um único DataFrame'''
    erros = pd.concat([cnpjInvalido, cnpjNulo, nomeNulo, cnpjDupl, nomeDupl])

    '''Contabilizar as quantidades'''
    total = len(df_fontes.index)
    totalCorretos = len(corretos.index)
    totalInvalido = len(cnpjInvalido.index)
    totalNulo = len(cnpjNulo.index) + len(nomeNulo.index)
    totalDupl = len(cnpjDupl.index) + len(nomeDupl.index)
    s1 = pd.Series([total, totalCorretos, totalInvalido, totalNulo, totalDupl])
    somas = pd.DataFrame([list(s1)], columns=['TOTAL', 'CORRETOS', 'CNPJ_INVALIDO', 'NULOS', 'DUPLICADOS'])

    '''Passar para csv'''
    erros.to_csv('erros.csv', index=False, header=True)
    corretos.to_csv('corretos.csv', index=False, header=True)
    somas.to_csv('somas.csv', index=False, header=True)
