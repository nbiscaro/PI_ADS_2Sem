#!/usr/bin/env python
# -*- coding: utf-8 -*-

# main.pyw
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

import tkinter
from tkinter.simpledialog import messagebox
from tkinter.filedialog import askopenfilenames
from emailgmail import email


def dashboard() -> None:
    """
    dashboard(): Serve para criar a tela principal do programa onde
    o usuario podera ter acesso as demais funcionalidades do sistema
    :return: None
    """

    with open('data') as rarq:
        emails = rarq.read().split()

    def novo() -> None:
        """
        novo(): Serve para criar uma tela para a criação e edicao
        de um novo email para ser enviado para os enderecos cadastrados
        no sistema
        :return: None
        """

        anexos = []

        def anexar() -> None:
            """
            anexar(): Serve para anexar arquivos no email que sera enviado
            :return: None
            """
            for arquivo in askopenfilenames():
                anexos.append(arquivo)
                list_anexos.insert(tkinter.END, arquivo[arquivo.rfind('/')+1:])
                lb_anexos['text'] = f'{len(anexos)} ANEXOS:'

        def desanexar() -> None:
            """
            desanexar(): Serve para desanexar um arquivo anteriormente anexado
            :return: None
            """
            try:
                for arquivo in list_anexos.selection_get().split():
                    for indice, arq in enumerate(list_anexos.get(0, tkinter.END)):
                        if arquivo == arq:
                            list_anexos.delete(indice)
                            del anexos[indice]
                            lb_anexos['text'] = f'{len(anexos)} ANEXOS:'
                            break
            except tkinter.TclError:
                pass

        def enviar() -> None:
            """
            enviar(): Serve para enviar o email para os enderecos cadastrados
            no sistema
            :return: None
            """
            email(emails, ent_assunto.get(), txt_mensagem.get(0.0, tkinter.END).rstrip(), anexos)


        # --------------------------------------------------------------------------------------------------------------
        # Definicoes janela_email

        janela_email = tkinter.Toplevel()
        janela_email.geometry('350x300+500+250')
        janela_email.title('Novo email')
        janela_email.iconbitmap('img/ico_spc.ico')
        janela_email.resizable(False, False)

        # --------------------------------------------------------------------------------------------------------------
        # Labels janela_email

        frame_assunto = tkinter.LabelFrame(janela_email)
        frame_assunto.place(x=0, y=0)

        lb_assunto = tkinter.Label(frame_assunto, text='ASSUNTO:', fg='#284d92')
        lb_assunto.grid(row=0, column=0)

        frame_anexos = tkinter.LabelFrame(janela_email)
        frame_anexos.place(x=0, y=24)

        lb_anexos = tkinter.Label(frame_anexos, text='0 ANEXOS:', fg='#284d92')
        lb_anexos.grid(row=0, column=0)

        frame_mensagem = tkinter.LabelFrame(janela_email)
        frame_mensagem.place(x=0, y=67)

        lb_mensagem = tkinter.Label(frame_mensagem, text='MENSAGEM:', fg='#284d92')
        lb_mensagem.grid(row=0, column=0)

        # --------------------------------------------------------------------------------------------------------------
        # Entry janela_email

        ent_assunto = tkinter.Entry(frame_assunto, font=2, width=32, selectbackground='#5ac091')
        ent_assunto.grid(row=0, column=1)

        txt_mensagem = tkinter.Text(frame_mensagem, width=43, height=10, selectbackground='#5ac091')
        txt_mensagem.grid(row=1, column=0)

        # --------------------------------------------------------------------------------------------------------------
        # Listbox janela_email

        list_anexos = tkinter.Listbox(frame_anexos, width=30, height=2, selectmode='extended',
                                      selectbackground='#5ac091')
        list_anexos.grid(row=0, column=1)

        # --------------------------------------------------------------------------------------------------------------
        # Botoes janela_email

        enviar_img = tkinter.PhotoImage(file='img/enviar.png')
        btn_enviar_email = tkinter.Button(janela_email, image=enviar_img, relief='groove', cursor='hand2',
                                          width=345, command=enviar)
        btn_enviar_email.place(x=0, y=251)

        btn_anexar = tkinter.Button(frame_anexos, text='+', relief='groove', cursor='hand2', fg='blue',
                                    width=6, height=2, command=anexar)
        btn_anexar.grid(row=0, column=2)

        btn_desanexar = tkinter.Button(frame_anexos, text='x', relief='groove', cursor='hand2', fg='red',
                                       width=6, height=2, command=desanexar)
        btn_desanexar.grid(row=0, column=3)

        # --------------------------------------------------------------------------------------------------------------
        # Fim janela_email

        janela_email.grab_set()
        janela_principal.focus_force()
        janela_email.mainloop()

    def adicionar_email() -> None:
        """
        adicionar_email(): Serve para adicionar novos enderecos de email
        :return: None
        """
        novo_email = entrada.get().strip()
        if novo_email != '':
            if novo_email not in lista.get(0, tkinter.END):
                lista.insert(tkinter.END, entrada.get())
                emails.append(novo_email)
                frame_cadastrados['text'] = f'{len(emails)} EMAILS CADASTRADOS:'
                with open('data', 'a') as aarq:
                    aarq.write(f'{novo_email}\n')
            else:
                messagebox.showinfo('Info', f'O email {novo_email} já está cadastrado')
            entrada.delete(0, tkinter.END)

    def remover_email() -> None:
        """
        remover_email(): Serve para remover enderevos de email já cadastrados
        :return: None
        """
        try:
            for selecionado in lista.selection_get().split():
                for i, email in enumerate(lista.get(0, tkinter.END)):
                    if email == selecionado:
                        lista.delete(i)
                        del emails[i]
                        frame_cadastrados['text'] = f'{len(emails)} EMAILS CADASTRADOS:'
                        with open('data', 'w') as warq:
                            warq.write('\n'.join(emails) + '\n')
                        break
        except tkinter.TclError:
            pass

    # ------------------------------------------------------------------------------------------------------------------
    # Definicoes janela_principal

    janela_principal = tkinter.Tk()
    janela_principal.geometry('600x367+500+250')
    janela_principal.title('Dashboard')
    janela_principal.iconbitmap('img/ico_spc.ico')
    janela_principal.resizable(False, False)

    # ------------------------------------------------------------------------------------------------------------------
    # Labels janela_principal

    img = tkinter.PhotoImage(file='img/logo_spc.png')
    lb_img = tkinter.Label(janela_principal, image=img)
    lb_img.place(x=15, y=15)

    frame_botoes_l = tkinter.LabelFrame(janela_principal, height=10, text='CADASTRAR / REMOVER', fg='#284d92')
    frame_botoes_l.place(x=205, y=60)

    frame_cadastrados = tkinter.LabelFrame(janela_principal, text=f'{len(emails)} EMAILS CADASTRADOS:', fg='#049552')
    frame_cadastrados.place(x=15, y=105)

    # ------------------------------------------------------------------------------------------------------------------
    # Listbox janela_principal

    lista = tkinter.Listbox(frame_cadastrados, width=94, height=14, selectmode='extended', selectbackground='#5ac091')
    for email_arq in emails:
        lista.insert(tkinter.END, email_arq)
    lista.grid()

    # ------------------------------------------------------------------------------------------------------------------
    # Entry janela_principal

    entrada = tkinter.Entry(frame_botoes_l, width=33, font=2, selectbackground='#5ac091')
    entrada.grid(row=0, column=0)

    # ------------------------------------------------------------------------------------------------------------------
    # Botoes janela_principal

    novo_img = tkinter.PhotoImage(file='img/novo.png')
    btn_novo_email = tkinter.Button(janela_principal, image=novo_img, relief='groove', cursor='hand2', command=novo)
    btn_novo_email.place(x=495, y=13)

    btn_adicionar = tkinter.Button(frame_botoes_l, text='+', width=4, relief='groove', cursor='hand2',
                                   command=adicionar_email, fg='blue')
    btn_adicionar.grid(row=0, column=1)

    btn_remover = tkinter.Button(frame_botoes_l, text='x', width=4, relief='groove', cursor='hand2',
                                 command=remover_email, fg='red')
    btn_remover.grid(row=0, column=2)

    # ------------------------------------------------------------------------------------------------------------------
    # Fim janela_principal

    janela_principal.focus_force()
    janela_principal.mainloop()


if __name__ == '__main__':
    dashboard()
