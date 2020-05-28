#!/usr/bin/env python
# -*- coding: utf-8 -*-

# main.py
# Github:@WeDias

#  MIT License
#
#  Copyright (c) 2020 Wesley Ribeiro Dias
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import csv
import tkinter
import sqlite3
from hashlib import sha256
from tkinter import messagebox
from tkinter import ttk


def criptografar(string: str) -> str:
    """
    criptografar(): Serve para gerar uma hash sha256 a partir de uma string qualquer
    :param string: str, string usada para gerar a hash
    :return: str, hash sha256
    """
    return sha256(string.encode()).hexdigest()


def dashboard(nome: str) -> None:
    """
    dashboard(): Serve para criar a tela principal do programa apos o login ser realizado com sucesso
    :return: None
    """

    def indicadores():
        pass

    def salvar():
        pass

    def erros_cnpj():
        treeview.heading('#0', text='ID')
        treeview.heading('1', text='CNPJ')
        treeview.heading('2', text='RAZÃO SOCIAL')
        treeview.heading('3', text='MOTIVO')
        for item in treeview.get_children():
            treeview.delete(item)
        with open('Erros/erros.csv', encoding='utf-8') as csv_arquivo:
            dados = csv.DictReader(csv_arquivo)
            for linha in dados:
                treeview.insert('', 'end',
                                text=linha['ID'], values=(linha['CNPJ'], linha['RAZÃO_SOCIAL'], linha['MOTIVO']))

    # ------------------------------------------------------------------------------------------------------------------
    # Definicoes da janela_principal/dashboard

    janela_principal = tkinter.Tk()
    janela_principal.geometry('1115x540+500+250')
    janela_principal.title('Dashboard')
    janela_principal.iconbitmap('img/ico_spc.ico')
    janela_principal.resizable(False, False)

    # ------------------------------------------------------------------------------------------------------------------
    # Labels janela_principal

    img = tkinter.PhotoImage(file='img/logo_spc.png')
    lb_img = tkinter.Label(janela_principal, image=img)
    lb_img.place(x=100, y=35)

    frame_botoes = tkinter.LabelFrame(janela_principal, text='UTILIDADES', height=10)
    frame_botoes.place(x=699, y=100)

    frame_resumo = tkinter.LabelFrame(janela_principal, text='RESUMO', height=10)
    frame_resumo.place(x=30, y=150)

    frame_erros = tkinter.LabelFrame(janela_principal, text='RELATÓRIO DE ERROS')
    frame_erros.place(x=365, y=150)

    # ------------------------------------------------------------------------------------------------------------------
    # treeview principal

    treeview = ttk.Treeview(frame_erros, height=15, selectmode='none')
    treeview['columns'] = ('1', '2', '3')
    treeview.column('#0', width=100, minwidth=100, stretch=False)
    treeview.column('1', width=200, minwidth=100, stretch=False)
    treeview.column('2', width=200, minwidth=100, stretch=False)
    treeview.column('3', width=200, minwidth=100, stretch=False)

    barra_rolagem_h = ttk.Scrollbar(frame_erros, orient="horizontal", command=treeview.xview)
    barra_rolagem_h.pack(side="bottom", fill="x")

    barra_rolagem = ttk.Scrollbar(frame_erros, orient="vertical", command=treeview.yview)
    barra_rolagem.pack(side="right", fill="y")

    treeview.configure(yscrollcommand=barra_rolagem.set, xscrollcommand=barra_rolagem_h.set)
    treeview.pack(side="right", fill="y")

    # ------------------------------------------------------------------------------------------------------------------
    # treeview resumo

    treeview_resumo = ttk.Treeview(frame_resumo, height=15, selectmode='none')
    treeview_resumo.column('#0', width=300, minwidth=300, stretch=False)
    treeview_resumo.insert('', 'end', 'INDICADORES', text='INDICADORES')
    treeview_resumo.insert('INDICADORES', 'end', text='<indicador1>')
    treeview_resumo.insert('INDICADORES', 'end', text='<indicador2>')
    treeview_resumo.insert('INDICADORES', 'end', text='<indicador3>')
    treeview_resumo.insert('INDICADORES', 'end', text='<indicador4>')
    treeview_resumo.insert('', 'end', 'ERROS', text='ERROS')
    treeview_resumo.insert('ERROS', 'end', 'FONTES', text='FONTES')

    with open('Erros/somas.csv', encoding='utf-8') as arq:
        dados_somas = csv.DictReader(arq)
        for linha_soma in dados_somas:
            total_erros = int(linha_soma['CNPJ_INVALIDO']) + int(linha_soma['NULOS']) + int(linha_soma['DUPLICADOS'])
            treeview_resumo.insert('FONTES', 'end', 'Erros encontrados', text=f'Erros encontrados: {total_erros}')
            treeview_resumo.insert('Erros encontrados', 'end', text=f'-CNPJ inválido(s): {linha_soma["CNPJ_INVALIDO"]}')
            treeview_resumo.insert('Erros encontrados', 'end', text=f'-CNPJ nulo(s): {linha_soma["NULOS"]}')
            treeview_resumo.insert('Erros encontrados', 'end', text=f'-CNPJ duplicado(s): 0')
            treeview_resumo.insert('Erros encontrados', 'end', text=f'-Nome(s) duplicado(s): {linha_soma["DUPLICADOS"]}')

    barra_rolagem_resumo_h = ttk.Scrollbar(frame_resumo, orient="horizontal", command=treeview_resumo.xview)
    barra_rolagem_resumo_h.pack(side='bottom', fill='x')

    barra_rolagem_resumo = ttk.Scrollbar(frame_resumo, orient="vertical", command=treeview_resumo.yview)
    barra_rolagem_resumo.pack(side="right", fill="y")

    treeview_resumo.configure(yscrollcommand=barra_rolagem_resumo.set, xscrollcommand=barra_rolagem_resumo_h)
    treeview_resumo.pack(side="right", fill="y")

    # ------------------------------------------------------------------------------------------------------------------
    # Botoes janela_principal

    bt_indicadores = tkinter.Button(frame_botoes, text='INDICADORES', width=17, relief='groove', cursor='hand2')
    bt_indicadores.grid(row=0, column=0)

    bt_cnpj = tkinter.Button(frame_botoes, text='ERROS DE CNPJ', width=17, relief='groove', cursor='hand2',
                             command=erros_cnpj)
    bt_cnpj.grid(row=0, column=1)

    bt_salvar = tkinter.Button(frame_botoes, text='SALVAR', width=17, relief='groove', cursor='hand2')
    bt_salvar.grid(row=0, column=2)

    # ------------------------------------------------------------------------------------------------------------------
    # Fim janela_principal

    janela_principal.focus_force()
    janela_principal.mainloop()


def main() -> None:
    """
    main(): Serve para fazer a tela de login para o usuario
    :return: None
    """

    def entrar() -> None:
        """
        entrar(): Serve para verificar se o usuario e a senha estao corretos e cadastrados no banco de dados
        :return: None
        """
        banco = sqlite3.connect('data/users.db')
        cursor = banco.cursor()
        dados = cursor.execute(f'SELECT * FROM login WHERE usuario = "{ent_entrar.get()}";').fetchone()
        banco.close()
        if dados and criptografar(ent_senha.get()) == dados[1]:
            messagebox.showinfo('Login', 'Login realizado com sucesso clique em OK para continuar')
            janela_login.destroy()
            dashboard(dados[0])
        else:
            messagebox.showerror('Erro', 'Falha ao realizar login, usuário/senha inválido')

    # ------------------------------------------------------------------------------------------------------------------
    # Definicoes da janela_login

    janela_login = tkinter.Tk()
    janela_login.title('Bem-vindo')
    janela_login.iconbitmap('img/ico_spc.ico')
    janela_login.geometry('400x115+700+400')
    janela_login.resizable(False, False)

    # ------------------------------------------------------------------------------------------------------------------
    # Labels janela_login

    tkinter.Label(janela_login).grid(row=0, column=0)

    img = tkinter.PhotoImage(file='img/logo_spc.png')
    lb_img = tkinter.Label(janela_login, image=img)
    lb_img.place(x=230, y=5)

    lb_entrar = tkinter.Label(janela_login, text='Usuário')
    lb_entrar.grid(row=1, column=0)

    lb_senha = tkinter.Label(janela_login, text='Senha')
    lb_senha.grid(row=2, column=0)

    lb_status = tkinter.Label(janela_login)
    lb_status.grid(row=3, column=2, pady=10)

    # ------------------------------------------------------------------------------------------------------------------
    # Botoes janela_login

    btn_entrar = tkinter.Button(janela_login, text='Entrar', width=20, command=entrar, relief='groove', cursor='hand2')
    btn_entrar.grid(row=3, column=1, pady=5)

    # ------------------------------------------------------------------------------------------------------------------
    # Entry janela_login

    ent_entrar = tkinter.Entry(janela_login, width=30)
    ent_entrar.grid(row=1, column=1)

    ent_senha = tkinter.Entry(janela_login, width=30, show='*')
    ent_senha.grid(row=2, column=1)

    # ------------------------------------------------------------------------------------------------------------------
    # Fim janela_login

    janela_login.focus_force()
    janela_login.mainloop()


if __name__ == '__main__':
    main()
