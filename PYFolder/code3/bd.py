import tkinter as tk
from tkinter import messagebox
import mysql.connector

def inserir_dados():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="conglomerado",
            port=3308
        )
        cursor = conn.cursor()

        # Inserir na tabela Pessoas
        sql_pessoa = """
        INSERT INTO Pessoas (Nome, Aniversario, CPF, Sexo, CEP)
        VALUES (%s, %s, %s, %s, %s)
        """
        dados_pessoa = (
            nome_entry.get(),
            nascimento_entry.get(),
            cpf_entry.get(),
            sexo_entry.get(),
            cep_entry.get()
        )
        cursor.execute(sql_pessoa, dados_pessoa)
        id_pessoa = cursor.lastrowid

        # Inserir na tabela Celular
        sql_celular = """
        INSERT INTO Celular (numcelular, modelo, NS)
        VALUES (%s, %s, %s)
        """
        dados_celular = (
            celular_entry.get(),
            modelo_entry.get(),
            ns_entry.get()
        )
        cursor.execute(sql_celular, dados_celular)
        id_celular = cursor.lastrowid

        # Inserir na tabela dadosconect
        sql_dados = """
        INSERT INTO dadosconect (idPessoas, idCelular, email, contagoogle, senhag, contamicrosoft, senham, senhaw)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        dados_dados = (
            id_pessoa, id_celular,
            email_entry.get(),
            google_var.get(),
            senha_entry.get(),
            microsoft_var.get(),
            senham_entry.get(),
            senhaw_entry.get()
        )
        cursor.execute(sql_dados, dados_dados)

        conn.commit()
        messagebox.showinfo("Sucesso", "Dados inseridos com sucesso!")
        conn.close()

    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Interface Tkinter
root = tk.Tk()
root.title("Cadastro no banco conglomerado")

# --- Pessoa ---
tk.Label(root, text="Nome").grid(row=0, column=0)
nome_entry = tk.Entry(root)
nome_entry.grid(row=0, column=1)

tk.Label(root, text="Nascimento (YYYY-MM-DD)").grid(row=1, column=0)
nascimento_entry = tk.Entry(root)
nascimento_entry.grid(row=1, column=1)

tk.Label(root, text="CPF").grid(row=2, column=0)
cpf_entry = tk.Entry(root)
cpf_entry.grid(row=2, column=1)

tk.Label(root, text="Sexo (M/F)").grid(row=3, column=0)
sexo_entry = tk.Entry(root)
sexo_entry.grid(row=3, column=1)

tk.Label(root, text="CEP").grid(row=4, column=0)
cep_entry = tk.Entry(root)
cep_entry.grid(row=4, column=1)

# --- Celular ---
tk.Label(root, text="Número Celular").grid(row=5, column=0)
celular_entry = tk.Entry(root)
celular_entry.grid(row=5, column=1)

tk.Label(root, text="Modelo").grid(row=6, column=0)
modelo_entry = tk.Entry(root)
modelo_entry.grid(row=6, column=1)

tk.Label(root, text="NS").grid(row=7, column=0)
ns_entry = tk.Entry(root)
ns_entry.grid(row=7, column=1)

# --- Dados Conect ---
tk.Label(root, text="Email").grid(row=8, column=0)
email_entry = tk.Entry(root)
email_entry.grid(row=8, column=1)

tk.Label(root, text="Conta Google (Y/N)").grid(row=9, column=0)
google_var = tk.Entry(root)
google_var.grid(row=9, column=1)

tk.Label(root, text="Senha Google").grid(row=10, column=0)
senha_entry = tk.Entry(root)
senha_entry.grid(row=10, column=1)

tk.Label(root, text="Conta Microsoft (Y/N)").grid(row=11, column=0)
microsoft_var = tk.Entry(root)
microsoft_var.grid(row=11, column=1)

tk.Label(root, text="Senha Microsoft").grid(row=12, column=0)
senham_entry = tk.Entry(root)
senham_entry.grid(row=12, column=1)

tk.Label(root, text="Senha Windows").grid(row=13, column=0)
senhaw_entry = tk.Entry(root)
senhaw_entry.grid(row=13, column=1)

# Botão de enviar
tk.Button(root, text="Inserir Dados", command=inserir_dados).grid(row=14, column=0, columnspan=2, pady=10)

root.mainloop()
