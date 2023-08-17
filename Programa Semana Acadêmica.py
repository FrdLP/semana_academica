import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image, ImageDraw, ImageFont
import os
import sqlite3
import pandas as pd
import shutil
import datetime
import textwrap


def criar_evento():
    evento_window = tk.Toplevel(root)
    evento_window.title("Criar Evento")
    evento_window.geometry("1920x1080")

    nome_evento_label = tk.Label(evento_window, text="Nome do Evento:")
    nome_evento_label.pack()
    nome_evento_entry = tk.Entry(evento_window, width=50)
    nome_evento_entry.pack()

    def selecionar_imagem_botao():
        filename = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
        imagem_botao_entry.delete(0, tk.END)
        imagem_botao_entry.insert(tk.END, filename)

    imagem_botao_label = tk.Label(evento_window, text="Imagem para Botão:")
    imagem_botao_label.pack()
    imagem_botao_entry = tk.Entry(evento_window)
    imagem_botao_entry.pack()
    imagem_botao_button = tk.Button(evento_window, text="Selecionar Imagem", command=selecionar_imagem_botao)
    imagem_botao_button.pack()

    def selecionar_imagem_fundo():
        filename = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
        imagem_fundo_entry.delete(0, tk.END)
        imagem_fundo_entry.insert(tk.END, filename)

    imagem_fundo_label = tk.Label(evento_window, text="Imagem de Fundo:")
    imagem_fundo_label.pack()
    imagem_fundo_entry = tk.Entry(evento_window)
    imagem_fundo_entry.pack()
    imagem_fundo_button = tk.Button(evento_window, text="Selecionar Imagem", command=selecionar_imagem_fundo)
    imagem_fundo_button.pack()

    def selecionar_imagem_certificado():
        filename = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
        imagem_certificado_entry.delete(0, tk.END)
        imagem_certificado_entry.insert(tk.END, filename)

    imagem_certificado_label = tk.Label(evento_window, text="Imagem de Template do Certificado:")
    imagem_certificado_label.pack()
    imagem_certificado_entry = tk.Entry(evento_window)
    imagem_certificado_entry.pack()
    imagem_certificado_button = tk.Button(evento_window, text="Selecionar Imagem", command=selecionar_imagem_certificado)
    imagem_certificado_button.pack()

    def inserir_texto_certificado(pasta_evento):
        texto_certificado = texto_certificado_entry.get("1.0", tk.END).strip()
        arquivo_certificado = os.path.join(pasta_evento, "texto_certificado.txt")
        with open(arquivo_certificado, "w") as f:
            f.write(texto_certificado)

    texto_certificado_label = tk.Label(evento_window, text="Texto para Certificado:")
    texto_certificado_label.pack()
    texto_certificado_entry = tk.Text(evento_window, width=80, height=20)
    texto_certificado_entry.pack()

    def salvar_dias_evento(pasta_evento):
        dias = []
        for i in range(10):
            dia = dias_entries[i].get().strip()
            if dia:
                dias.append(dia)

        arquivo_dias_evento = os.path.join(pasta_evento, "dias_evento.txt")
        with open(arquivo_dias_evento, "w") as f:
            for i, dia in enumerate(dias):
                f.write(f"{i+1} - {dia}\n")

    def salvar_evento():
        nome_evento = nome_evento_entry.get()
        pasta_evento = nome_evento.replace(" ", "_")
        os.makedirs(pasta_evento, exist_ok=True)

        imagem_botao = imagem_botao_entry.get()
        imagem_fundo = imagem_fundo_entry.get()
        imagem_certificado = imagem_certificado_entry.get()

        destino_imagem_botao = os.path.join(pasta_evento, "imagem_botao.png")
        destino_imagem_fundo = os.path.join(pasta_evento, "imagem_fundo.png")
        destino_imagem_certificado = os.path.join(pasta_evento, "imagem_certificado.png")

        os.rename(imagem_botao, destino_imagem_botao)
        os.rename(imagem_fundo, destino_imagem_fundo)
        os.rename(imagem_certificado, destino_imagem_certificado)

        # Criação do banco de dados
        conn = sqlite3.connect(os.path.join(pasta_evento, f"{nome_evento}.db"))
        conn.close()

        inserir_texto_certificado(pasta_evento)
        salvar_dias_evento(pasta_evento)

        evento_window.destroy()
        atualizar_pagina_inicial()

    dias_entries = []
    for i in range(10):
        dia_label = tk.Label(evento_window, text=f"Dia {i+1} do Evento (dd/mm/aaaa):")
        dia_label.pack()
        dia_entry = tk.Entry(evento_window)
        dia_entry.pack()
        dias_entries.append(dia_entry)

    salvar_button = tk.Button(evento_window, text="Salvar", command=salvar_evento)
    salvar_button.pack(pady=10)

def atualizar_pagina_inicial():
    # Limpa a página inicial
    for widget in pagina_inicial.winfo_children():
        if widget != criar_evento_button:
            widget.destroy()
    
    eventos = []
    for item in os.listdir():
        if os.path.isdir(item):
            eventos.append(item)
    
    # Configurações para o posicionamento dos botões
    num_botoes_por_linha = 7
    
    # Cria um novo frame para os botões dos eventos
    frame_botoes = tk.Frame(pagina_inicial)
    frame_botoes.pack()
    
    # Adiciona os botões para cada evento
    for i, evento in enumerate(eventos):
        botao_evento = tk.Button(frame_botoes, command=lambda evento=evento: abrir_evento(evento))
        
        # Carrega a imagem do botão
        imagem_botao_path = os.path.join(evento, "imagem_botao.png")
        if os.path.exists(imagem_botao_path):
            imagem_botao = Image.open(imagem_botao_path)
            imagem_botao = imagem_botao.resize((200, 200), Image.LANCZOS)
            imagem_botao = ImageTk.PhotoImage(imagem_botao)
            botao_evento.config(image=imagem_botao)
            botao_evento.image = imagem_botao
        
        # Calcula a posição do botão na grade
        row = i // num_botoes_por_linha
        column = i % num_botoes_por_linha
        
        # Empacota o botão na posição correta
        botao_evento.grid(row=row, column=column, padx=10, pady=10)


def abrir_evento(evento):
    evento_window = tk.Toplevel(root)
    evento_window.title("Evento: " + evento)
    evento_window.geometry("1920x1080")
    
    # Carrega a imagem de fundo
    imagem_fundo_path = os.path.join(evento, "imagem_fundo.png")
    if os.path.exists(imagem_fundo_path):
        imagem_fundo = Image.open(imagem_fundo_path)
        imagem_fundo = imagem_fundo.resize((1920, 1080), Image.LANCZOS)
        imagem_fundo = ImageTk.PhotoImage(imagem_fundo)
        fundo_label = tk.Label(evento_window, image=imagem_fundo)
        fundo_label.place(x=0, y=0, relwidth=1, relheight=1)
        fundo_label.image = imagem_fundo
    
    # Botão "Configurações"
    configuracoes_button = tk.Button(evento_window, text="Configurações")
    configuracoes_button.place(x=10, y=10)


    def abrir_pagina_configuracoes():
        configuracoes_window = tk.Toplevel(evento_window)
        configuracoes_window.geometry("200x250")


        def cadastro_pessoas():
            cadastro_window = tk.Toplevel(evento_window)
            cadastro_window.geometry("500x500")
            
            nome_label = tk.Label(cadastro_window, text="Nome:")
            nome_label.pack()
            nome_entry = tk.Entry(cadastro_window,width=50)
            nome_entry.pack()
            
            ra_label = tk.Label(cadastro_window, text="RA:")
            ra_label.pack()
            ra_entry = tk.Entry(cadastro_window)
            ra_entry.pack()
            
            email_label = tk.Label(cadastro_window, text="Email:")
            email_label.pack()
            email_entry = tk.Entry(cadastro_window,width=50)
            email_entry.pack()
            
            def salvar_cadastro():
                nome = nome_entry.get()
                ra = ra_entry.get()
                email = email_entry.get()
                
                # Conexão com o banco de dados
                conn = sqlite3.connect(os.path.join(evento, f"{evento}.db"))
                c = conn.cursor()
                
                # Verifica se a tabela já existe, caso contrário, cria a tabela
                c.execute('''CREATE TABLE IF NOT EXISTS Dados
                            (Nome TEXT, RA INTEGER, Email TEXT)''')
                
                # Insere os dados na tabela
                c.execute("INSERT INTO Dados VALUES (?, ?, ?)", (nome, ra, email))
                
                # Finaliza e confirma as alterações no banco de dados
                conn.commit()
                conn.close()
                
                # Cria uma pasta com o nome da pessoa dentro da pasta do evento
                pasta_pessoa = os.path.join(evento, nome)
                os.makedirs(pasta_pessoa, exist_ok=True)
                
                # Cria o arquivo de texto com os dados do cadastro
                arquivo_cadastro = os.path.join(pasta_pessoa, "dados_cadastro.txt")
                with open(arquivo_cadastro, "w") as f:
                    f.write(f"Nome: {nome}\n")
                    f.write(f"RA: {ra}\n")
                    f.write(f"Email: {email}\n")
                    f.write(f"\n")
                    f.write(f"Palestras com presença:\n")

                cadastro_window.destroy()

            salvar_button = tk.Button(cadastro_window, text="Salvar", command=salvar_cadastro)
            salvar_button.pack()

        
        def cadastro_palestras():
            cadastro_palestras_window = tk.Toplevel(evento_window)
            cadastro_palestras_window.title("Cadastro de Palestras")
            cadastro_palestras_window.geometry("1920x1080")

            nome_palestra_label = tk.Label(cadastro_palestras_window, text="Nome da Palestra:")
            nome_palestra_label.pack()
            nome_palestra_entry = tk.Entry(cadastro_palestras_window,width=50)
            nome_palestra_entry.pack()

            descricao_label = tk.Label(cadastro_palestras_window, text="Descrição:")
            descricao_label.pack()
            descricao_entry = tk.Text(cadastro_palestras_window)
            descricao_entry.pack()

            imagem_label = tk.Label(cadastro_palestras_window, text="Imagem:")
            imagem_label.pack(pady=10)
            imagem_entry = tk.Entry(cadastro_palestras_window)
            imagem_entry.pack(pady=10)

            def selecionar_imagem():
                filename = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
                imagem_entry.delete(0, tk.END)
                imagem_entry.insert(tk.END, filename)

            def selecionar_imagem_botao():
                filename = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
                imagem_botao_entry.delete(0, tk.END)
                imagem_botao_entry.insert(tk.END, filename)

            imagem_button = tk.Button(cadastro_palestras_window, text="Selecionar Imagem", command=selecionar_imagem)
            imagem_button.pack()

            imagem_botao_label = tk.Label(cadastro_palestras_window, text="Imagem do Botão:")
            imagem_botao_label.pack()
            imagem_botao_entry = tk.Entry(cadastro_palestras_window)
            imagem_botao_entry.pack()

            imagem_botao_button = tk.Button(cadastro_palestras_window, text="Selecionar Imagem do Botão", command=selecionar_imagem_botao)
            imagem_botao_button.pack()

            dia_label = tk.Label(cadastro_palestras_window, text="Dia da Palestra (dd/mm/aaaa):")
            dia_label.pack()
            dia_entry = tk.Entry(cadastro_palestras_window)
            dia_entry.pack()

            horario_inicio_label = tk.Label(cadastro_palestras_window, text="Horário de Início (HH:MM):")
            horario_inicio_label.pack()
            horario_inicio_entry = tk.Entry(cadastro_palestras_window)
            horario_inicio_entry.pack()

            horario_termino_label = tk.Label(cadastro_palestras_window, text="Horário de Término (HH:MM):")
            horario_termino_label.pack()
            horario_termino_entry = tk.Entry(cadastro_palestras_window)
            horario_termino_entry.pack()

            def salvar_palestra():
                nome_palestra = nome_palestra_entry.get()
                descricao = descricao_entry.get("1.0", tk.END).strip()
                imagem = imagem_entry.get()
                imagem_botao = imagem_botao_entry.get()
                dia = dia_entry.get()
                horario_inicio = horario_inicio_entry.get()
                horario_termino = horario_termino_entry.get()

                # Conexão com o banco de dados
                conn = sqlite3.connect(os.path.join(evento, f"{evento}.db"))
                c = conn.cursor()

                # Verifica se a tabela já existe, caso contrário, cria a tabela
                c.execute('''CREATE TABLE IF NOT EXISTS Palestras
                            (Nome TEXT, Descricao TEXT, Imagem TEXT, ImagemBotao TEXT,
                            Dia TEXT, HorarioInicio TEXT, HorarioTermino TEXT)''')

                # Insere os dados na tabela
                c.execute("INSERT INTO Palestras VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (nome_palestra, descricao, imagem, imagem_botao, dia, horario_inicio, horario_termino))

                # Finaliza e confirma as alterações no banco de dados
                conn.commit()
                conn.close()

                # Salva a imagem e a imagem do botão na pasta do evento
                if imagem:
                    pasta_evento = evento.replace(" ", "_")
                    destino_imagem = os.path.join(pasta_evento, f"{nome_palestra}.png")
                    shutil.copy(imagem, destino_imagem)

                if imagem_botao:
                    pasta_evento = evento.replace(" ", "_")
                    destino_imagem_botao = os.path.join(pasta_evento, f"{nome_palestra}_botao.png")
                    shutil.copy(imagem_botao, destino_imagem_botao)

                cadastro_palestras_window.destroy()

            salvar_button = tk.Button(cadastro_palestras_window, text="Salvar", command=salvar_palestra)
            salvar_button.pack()

        
        def remocao_pessoas():
            remocao_window = tk.Toplevel(evento_window)
            remocao_window.title("Remoção de Pessoas")
            remocao_window.geometry("300x150")
            
            nome_label = tk.Label(remocao_window, text="Nome:")
            nome_label.pack()
            nome_entry = tk.Entry(remocao_window)
            nome_entry.pack()
            
            ra_label = tk.Label(remocao_window, text="RA:")
            ra_label.pack()
            ra_entry = tk.Entry(remocao_window)
            ra_entry.pack()
            
            def remover_dados():
                nome = nome_entry.get()
                ra = ra_entry.get()
                
                # Conexão com o banco de dados
                conn = sqlite3.connect(os.path.join(evento, f"{evento}.db"))
                c = conn.cursor()
                
                # Remoção dos dados correspondentes ao nome ou RA
                if nome:
                    c.execute("DELETE FROM Dados WHERE Nome=?", (nome,))
                elif ra:
                    c.execute("DELETE FROM Dados WHERE RA=?", (ra,))
                
                # Finaliza e confirma as alterações no banco de dados
                conn.commit()
                conn.close()
                
                remocao_window.destroy()
            
            remover_button = tk.Button(remocao_window, text="Remover", command=remover_dados)
            remover_button.pack()

        
        def remocao_palestras():
            remocao_palestras_window = tk.Toplevel(evento_window)
            remocao_palestras_window.title("Remoção de Palestras")
            remocao_palestras_window.geometry("300x150")
            
            nome_palestra_label = tk.Label(remocao_palestras_window, text="Nome da Palestra:")
            nome_palestra_label.pack()
            nome_palestra_entry = tk.Entry(remocao_palestras_window)
            nome_palestra_entry.pack()
            
            def remover_palestra():
                nome_palestra = nome_palestra_entry.get()
                
                # Conexão com o banco de dados
                conn = sqlite3.connect(os.path.join(evento, f"{evento}.db"))
                c = conn.cursor()
                
                # Remoção dos dados correspondentes à palestra
                c.execute("DELETE FROM Palestras WHERE Nome=?", (nome_palestra,))
                
                # Finaliza e confirma as alterações no banco de dados
                conn.commit()
                conn.close()
                
                # Apaga a imagem da palestra da pasta do evento
                pasta_evento = evento.replace(" ", "_")
                imagem_palestra = os.path.join(pasta_evento, f"{nome_palestra}.png")
                if os.path.exists(imagem_palestra):
                    os.remove(imagem_palestra)
                
                remocao_palestras_window.destroy()
            
            remover_button = tk.Button(remocao_palestras_window, text="Remover", command=remover_palestra)
            remover_button.pack()

        def mostrar_tabela():
            # Conexão com o banco de dados
            conn = sqlite3.connect(os.path.join(evento, f"{evento}.db"))
            
            # Obtém o nome das tabelas
            c = conn.cursor()
            c.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tabelas = c.fetchall()
            
            if not tabelas:
                messagebox.showinfo("Informação", "Não há tabelas no banco de dados.")
                conn.close()
                return
            
            # Cria a janela para mostrar as tabelas
            tabela_window = tk.Toplevel(evento_window)
            tabela_window.title("Tabelas")
            tabela_window.geometry("800x600")
            
            style = ttk.Style(tabela_window)
            style.theme_use("clam")  # Escolha o tema de acordo com sua preferência
            
            notebook = ttk.Notebook(tabela_window)
            notebook.pack(fill=tk.BOTH, expand=True)
            
            for tabela in tabelas:
                tabela_frame = tk.Frame(notebook)
                notebook.add(tabela_frame, text=tabela[0])
                
                # Lê a tabela utilizando Pandas
                query = f"SELECT * FROM {tabela[0]};"
                df = pd.read_sql_query(query, conn)
                
                # Cria o widget DataFrame do Pandas
                table = ttk.Treeview(tabela_frame, style="Custom.Treeview")
                table['columns'] = tuple(df.columns)
                table['show'] = 'headings'
                
                # Define o estilo da tabela
                style.configure("Custom.Treeview", font=("Arial", 12))
                style.configure("Custom.Treeview.Heading", font=("Arial", 12, "bold"))
                
                # Define as colunas e seus cabeçalhos
                for col in df.columns:
                    table.heading(col, text=col)
                
                # Adiciona os dados da tabela
                for row in df.itertuples(index=False):
                    table.insert('', tk.END, values=tuple(row))
                
                # Adiciona a tabela ao frame
                table.pack(fill=tk.BOTH, expand=True)
            
            # Mostra a tabela de presença
            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Presenca'")
            presenca_exists = c.fetchone()
            if presenca_exists:
                tabela_frame_presenca = tk.Frame(notebook)
                notebook.add(tabela_frame_presenca, text="Presenca")
                
                # Lê a tabela de presença utilizando Pandas
                query_presenca = "SELECT * FROM Presenca;"
                df_presenca = pd.read_sql_query(query_presenca, conn)
                
                # Cria o widget DataFrame do Pandas para a tabela de presença
                table_presenca = ttk.Treeview(tabela_frame_presenca, style="Custom.Treeview")
                table_presenca['columns'] = tuple(df_presenca.columns)
                table_presenca['show'] = 'headings'
                
                # Define o estilo da tabela de presença
                style.configure("Custom.Treeview", font=("Arial", 12))
                style.configure("Custom.Treeview.Heading", font=("Arial", 12, "bold"))
                
                # Define as colunas e seus cabeçalhos
                for col in df_presenca.columns:
                    table_presenca.heading(col, text=col)
                
                # Adiciona os dados da tabela de presença
                for row in df_presenca.itertuples(index=False):
                    table_presenca.insert('', tk.END, values=tuple(row))
                
                # Adiciona a tabela de presença ao frame
                table_presenca.pack(fill=tk.BOTH, expand=True)
            
            conn.close()

        cadastro_pessoas_button = tk.Button(configuracoes_window, text="Cadastro de Pessoas", command=cadastro_pessoas)
        cadastro_pessoas_button.pack(pady=10)
        
        cadastro_palestras_button = tk.Button(configuracoes_window, text="Cadastro de Palestras", command=cadastro_palestras)
        cadastro_palestras_button.pack(pady=10)
        
        remocao_pessoas_button = tk.Button(configuracoes_window, text="Remoção de Pessoas", command=remocao_pessoas)
        remocao_pessoas_button.pack(pady=10)
        
        remocao_palestras_button = tk.Button(configuracoes_window, text="Remoção de Palestras", command=remocao_palestras)
        remocao_palestras_button.pack(pady=10)

        mostrar_tabela_button = tk.Button(configuracoes_window, text="Mostrar Tabela", command=mostrar_tabela)
        mostrar_tabela_button.pack(pady=10)

    configuracoes_button.config(command=abrir_pagina_configuracoes)
    
    # Resto do conteúdo da janela do evento

    # ... (previous code)

    def botoes_palestras(evento_window, evento):
        
        #Conexão com o banco de dados
        conn = sqlite3.connect(os.path.join(evento, f"{evento}.db"))
        c = conn.cursor()

        # Get the event days from the database and sort them chronologically
        c.execute("SELECT DISTINCT Dia FROM Palestras ORDER BY Dia")
        dias_evento = [dia[0] for dia in c.fetchall()]

        # Create a notebook to hold the lecture buttons for each day
        notebook = ttk.Notebook(evento_window)
        notebook.place(x=50, y=300, width=400, height=780)  # Position the notebook in the center

         # Create a style for the notebook tabs
        style = ttk.Style()
        style.theme_create("custom_style", parent="alt", settings={
            "TNotebook.Tab": {
                "configure": {"padding": [5, 2], "background": "#f0f0f0"},
                "map": {"background": [("selected", "#ffffff")]}
            }
        })
        style.theme_use("custom_style")

        # Create a page for each event day
        for dia in dias_evento:
            tab_page = tk.Frame(notebook)
            notebook.add(tab_page, text=dia)

            # Get the lectures for this day
            c.execute("SELECT Nome, ImagemBotao FROM Palestras WHERE Dia=?", (dia,))
            palestras_dia = c.fetchall()

            # Create the buttons for each lecture on this day
            for palestra in palestras_dia:
                nome_palestra = palestra[0]
                imagem_botao_path = palestra[1]
                imagem_fundo_path = os.path.join(evento, f"{nome_palestra}.png")



                # Load the button image
                if os.path.exists(imagem_botao_path):
                    imagem_botao = Image.open(imagem_botao_path)
                    imagem_botao = imagem_botao.resize((400, 80), Image.LANCZOS)
                    imagem_botao = ImageTk.PhotoImage(imagem_botao)

                    # Create the button for the lecture
                    botao_palestra = tk.Button(tab_page, image=imagem_botao, command=lambda np=nome_palestra, ifp=imagem_fundo_path: pagina_palestra(evento,np, ifp))
                    botao_palestra.image = imagem_botao
                    botao_palestra.pack(side=tk.TOP)

        # Close the connection to the database
        conn.close()


    botoes_palestras(evento_window, evento)
    


    def pagina_palestra(evento, nome_palestra, imagem_fundo):
        palestra_window = tk.Toplevel(root)
        palestra_window.title(nome_palestra)
        palestra_window.geometry("1920x1080")

        # Conexão com o banco de dados
        conn = sqlite3.connect(os.path.join(evento, f"{evento}.db"))
        c = conn.cursor()

        # Verifica se a tabela Palestras existe
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Palestras'")
        table_exists = c.fetchone()
        if table_exists:
            # Obtém os dados da palestra específica
            c.execute("SELECT Descricao, Imagem, ImagemBotao FROM Palestras WHERE Nome=?", (nome_palestra,))
            palestra = c.fetchone()

            if palestra:
                descricao_palestra = palestra[0]

                # Load the background image of the lecture
                if os.path.exists(imagem_fundo):
                    imagem_fundo = Image.open(imagem_fundo)
                    imagem_fundo = imagem_fundo.resize((1920, 1080), Image.LANCZOS)
                    imagem_fundo = ImageTk.PhotoImage(imagem_fundo)
                    fundo_label = tk.Label(palestra_window, image=imagem_fundo)
                    fundo_label.place(x=0, y=0, relwidth=1, relheight=1)
                    fundo_label.image = imagem_fundo

        # Descrição da palestra
        descricao_palestra_text = tk.Text(palestra_window, width=60, height=10, font=("Arial", 14))
        descricao_palestra_text.place(x=660, y=200, width=600, height=400)
        descricao_palestra_text.insert(tk.END, descricao_palestra)

        # Input para fornecer o RA
        ra_label = tk.Label(palestra_window, text="RA:", font=("Arial", 20))
        ra_label.place(x=660, y=600)
        ra_entry = tk.Entry(palestra_window, font=("Arial", 20))
        ra_entry.place(x=710, y=600, width=550)

        # Label para exibir os dados da pessoa encontrada
        dados_label = tk.Label(palestra_window, text="", font=("Arial", 25))
        dados_label.place(x=660, y=635, width=600, height=250)

        def buscar_pessoa_por_ra(evento, ra, dados_label):
            # Conexão com o banco de dados
            conn = sqlite3.connect(os.path.join(evento, f"{evento}.db"))
            c = conn.cursor()

            # Obtém o RA digitado na caixa de texto
            ra_digitado = ra_entry.get()

            # Procura a pessoa pelo RA no banco de dados
            c.execute("SELECT Nome, RA FROM Dados WHERE RA=?", (ra_digitado,))
            pessoa = c.fetchone()

            conn.close()

            if pessoa:
                nome, ra = pessoa
                # Exibe os dados encontrados em um Label
                dados_label["text"] = f"Nome: {nome}\n\nRA: {ra}"
            else:
                dados_label["text"] = "Pessoa não cadastrada"

        # Bind the KeyRelease event of ra_entry to call the buscar_pessoa_por_ra function
        ra_entry.bind("<KeyRelease>", lambda event: buscar_pessoa_por_ra(evento, ra_entry.get(), dados_label))

        def marcar_presenca(evento, nome_palestra, ra_entry):
            # Conexão com o banco de dados
            conn = sqlite3.connect(os.path.join(evento, f"{evento}.db"))
            c = conn.cursor()

            # Obtém o RA digitado na caixa de texto
            ra_digitado = ra_entry.get()

            # Procura a pessoa pelo RA no banco de dados
            c.execute("SELECT Nome FROM Dados WHERE RA=?", (ra_digitado,))
            pessoa = c.fetchone()

            if pessoa:
                nome = pessoa[0]

                # Procura os dados da palestra no banco de dados
                c.execute("SELECT Dia, HorarioInicio, HorarioTermino FROM Palestras WHERE Nome=?", (nome_palestra,))
                palestra = c.fetchone()

                if palestra:
                    dia, horario_inicio, horario_termino = palestra

                    # Calcula a carga horária da palestra
                    formato_horario = "%H:%M"
                    horario_inicio_dt = datetime.datetime.strptime(horario_inicio, formato_horario)
                    horario_termino_dt = datetime.datetime.strptime(horario_termino, formato_horario)
                    carga_horaria = (horario_termino_dt - horario_inicio_dt).seconds // 3600

                    # Pega o texto do certificado
                    arquivo_certificado = os.path.join(evento, "texto_certificado.txt")
                    with open(arquivo_certificado, "r") as f:
                        texto_certificado = f.read()
                    
                    imagem_certificado = os.path.join(evento, "imagem_certificado.png")

                    pasta_destino = os.path.join(evento, nome)

                    #Troca o _ por espaço no nome do evento
                    evento = evento.replace("_", " ")
                    
                    # Substitui as variáveis do texto do certificado pelos valores correspondentes e salva como texto_final
                    texto_final = texto_certificado.replace("NOME", nome)
                    texto_final = texto_final.replace("EVENTO", evento)
                    texto_final = texto_final.replace("ATIVIDADE", nome_palestra)
                    texto_final = texto_final.replace("DATA", dia)
                    texto_final = texto_final.replace("CARGA", str(carga_horaria))
                    texto_final = texto_final.replace("DIA", dia[0:2])

                    conn.close()

                def criar_certificado(texto_final, imagem_fundo, pasta_destino):
                    # Abre a imagem de fundo
                    fundo_certificado = Image.open(imagem_fundo)

                    # Cria uma instância de ImageDraw para desenhar no certificado
                    draw = ImageDraw.Draw(fundo_certificado)

                    # Define as dimensões e posição da caixa de texto
                    caixa_largura = 1015
                    caixa_altura = 650
                    caixa_pos_x = 200
                    caixa_pos_y = 600

                    # Cria uma instância de ImageDraw para desenhar na imagem de fundo
                    draw = ImageDraw.Draw(fundo_certificado)

                    # Cria a caixa de texto usando um retângulo
                    caixa_texto = (caixa_pos_x, caixa_pos_y, caixa_pos_x + caixa_largura, caixa_pos_y + caixa_altura)
                    #Cria um retângulo oco com as dimensões da caixa de texto 
                    #draw.rectangle(caixa_texto, outline="black", width=5)

                    # Define a fonte e tamanho do texto dentro da caixa
                    fonte = ImageFont.truetype("arial.ttf", 55)

                    # Separa as linhas do texto_final
                    linhas = texto_final.splitlines()

                    # Separa as linhas com os nomes conforme solicitado
                    linha_declaramos = linhas[0]
                    linha_nome = linhas[1]
                    linha_corpo = linhas[2]
                    linha_local_e_data = linhas[3]

                     # Escreve a linha declaramos
                    fonte_declaramos = ImageFont.truetype("arial.ttf", 50)  # Defina a fonte e tamanho desejados para o "Declaramos"
                    linha_declaramos_width, linha_declaramos_height = draw.textsize(linha_declaramos, font=fonte_declaramos)
                    pos_y = caixa_pos_y + 10  # Espaçamento após a caixa
                    #Centraliza horizontalmente a linha "declaramos"
                    x_declaramos_centralizado = caixa_pos_x + (caixa_largura - linha_declaramos_width) / 2
                    # Quebra a linha se o texto for muito grande
                    if fonte_declaramos.getsize(linha_declaramos)[0] > caixa_largura:
                        linha_declaramos = textwrap.fill(linha_declaramos, width=45)
                        draw.text((x_declaramos_centralizado, pos_y), linha_declaramos, fill="black", font=fonte_declaramos, align="center")
                    else:
                        draw.text((x_declaramos_centralizado, pos_y), linha_declaramos, fill="black", font=fonte_declaramos, align="center")

                    # Escreve a linha nome
                    fonte_nome_size = 55
                    fonte_nome = ImageFont.truetype("arialbd.ttf", fonte_nome_size)  # Defina a fonte e tamanho desejados para o nome
                    linha_nome_width, linha_nome_height = draw.textsize(linha_nome, font=fonte_nome)
                    pos_y += fonte.getsize(linha_declaramos)[1] + fonte_nome_size/2  # Espaçamento após a primeira linha
                    #Centraliza horizontalmente o nome
                    x_nome_centralizado = caixa_pos_x + (caixa_largura - linha_nome_width) / 2
                    # Quebra a linha se o texto for muito grande
                    if fonte_nome.getsize(linha_nome)[0] > caixa_largura:
                        linha_nome = textwrap.fill(linha_nome, width=40)
                        draw.text((x_nome_centralizado, pos_y), linha_nome, fill="black", font=fonte_nome, align="center")
                    else:
                        draw.text((x_nome_centralizado, pos_y), linha_nome, fill="black", font=fonte_nome, align="center")
     
                    # Configurações para o corpo do texto
                    fonte_corpo = ImageFont.truetype("arial.ttf", 40)
                    pos_y = pos_y + fonte.getsize(linha_nome)[1] + 30
                    caixa_texto = (caixa_pos_x, pos_y, caixa_pos_x + caixa_largura, caixa_pos_y + caixa_altura)
                    #draw.rectangle(caixa_texto, outline="black", width=5)

                    # Divide o texto em linhas
                    lines = textwrap.wrap(linha_corpo, width=50)
                    line_height = fonte_corpo.getsize(' ')[1]

                    # Ajusta o espaçamento para a última linha
                    last_line_height = draw.textsize(lines[-1], font=fonte_corpo)[1]

                    # Loop pelas linhas
                    for idx, line in enumerate(lines):
                        words = line.split()
                        
                        if idx == len(lines) - 1:  # Última linha, alinhada à esquerda
                            x = caixa_pos_x
                        else:  # Linhas justificadas
                            space_width = (caixa_largura - sum(draw.textsize(word, font=fonte_corpo)[0] for word in words)) / (len(words) - 1)
                            x = caixa_pos_x
                        
                        for word in words:
                            word_width, _ = draw.textsize(word, font=fonte_corpo)
                            draw.text((x, pos_y), word, font=fonte_corpo, fill="black")
                            x += word_width + space_width
                            
                        pos_y += line_height
                        
                    # Escreve a linha local e data
                    fonte_local_data = ImageFont.truetype("arial.ttf", 35)  # Defina a fonte e tamanho desejados para o local e data
                    local_data_width, local_data_height = draw.textsize(linha_local_e_data, font=fonte_local_data)
                    pos_x_local_data = caixa_pos_x + caixa_largura - local_data_width  # Alinha à direita
                    pos_y = caixa_pos_y + caixa_altura - local_data_height - 10
                    draw.text((pos_x_local_data, pos_y), linha_local_e_data, fill="black", font=fonte_local_data)

                    # Salva o certificado na pasta_destino
                    certificado_path = os.path.join(pasta_destino, f"{nome_palestra}_{nome}.png")
                    fundo_certificado.save(certificado_path)

                    # Abre o arquivo de texto na página do participante
                    arquivo_cadastro = os.path.join(pasta_destino, "dados_cadastro.txt")
                    with open(arquivo_cadastro, "a") as f:
                        f.write(f"{nome_palestra}\n")

                    # Fecha a imagem
                    fundo_certificado.close()

                criar_certificado(texto_final, imagem_certificado, pasta_destino)

                # Limpar a caixa do ra_entry e dados_label
                ra_entry.delete(0, tk.END)
                dados_label["text"] = ""

            conn.close()

        #Botão para marcar presença
        marcar_presenca_button = tk.Button(palestra_window, text="Marcar Presença", font=("Arial", 40), command=lambda: marcar_presenca(evento, nome_palestra, ra_entry))
        marcar_presenca_button.place(x=660, y=885, width=601, height=100)

    evento_window.mainloop()

root = tk.Tk()
root.title("Página Inicial do Evento")
root.geometry("1920x1080")

pagina_inicial = tk.Frame(root)
pagina_inicial.pack()

criar_evento_button = tk.Button(pagina_inicial, text="Criar Evento", command=criar_evento)
criar_evento_button.pack(side=tk.BOTTOM, pady=10)

atualizar_pagina_inicial()

root.mainloop()
