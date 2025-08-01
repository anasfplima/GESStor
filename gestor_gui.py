'''GESStor de Referências - Trabalho final
    Ana Sofia Lima (10200763)
    Carolina Coutinho (10230053)
    Mestrado em Bioestatística e Bioinformática aplicadas à saúde - Programação e Bases de Dados'''


#%%

import unidecode, string # Módulo para normalizar as strings de input
from tkinter import ttk # Módulo para criar um GUI
from tkinter import filedialog # Função extra que permite abrir uma janela de diálogo para upload de ficheiros
import tkinter as tk
import json 
import sqlite3

#%%
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#%%

# Abrir o ficheiro txt onde as referências estão guardadas

with open('references.txt', 'r', encoding='utf-8') as file:
    references = json.load(file)

#%%

# Função para guardar as referências para o documento de texto 

def save_on_exit():
    with open('references.txt', 'w', encoding='utf-8') as file:
        json.dump(references, file, ensure_ascii=False)
        window.destroy()
        
#%% 

# Função para mostrar todas as referências inseridas com uma formatação visualmente apelativa 

def biblioteca():
    popup = tk.Toplevel()
    popup.title('Biblioteca')

    text_widget = tk.Text(popup)
    text_widget.pack()

    text_widget.insert(tk.END, f"A sua biblioteca contém {len(references)} referências.\n\n")
    for i, reference in enumerate(references, start=1): # Cria um par Índice-Referência para enumeração
        text_widget.insert(tk.END, f"{i}.\n")
        for key, value in reference.items():
            if key == 'Autores':
                authors = ', '.join([f"{author['Nome próprio']} {author['Apelido']}" for author in value])
                text_widget.insert(tk.END, f"{key}: {authors}\n")
            else:
                text_widget.insert(tk.END, f"{key}: {', '.join(value)}\n")
        text_widget.insert(tk.END, "\n")

#%%

# Função para eliminar uma referência

def del_ref():
    popup = tk.Toplevel()
    popup.title('Eliminar referência')
    
    text_widget = tk.Text(popup)
    text_widget.pack()
    
    for i, reference in enumerate(references, start=1): # Aqui o índice associado a cada referência é usado para ajudar o utilizador a escolher qual quer eliminar
        text_widget.insert(tk.END, f"{i}.\n")
        for key, value in reference.items():
            if key == 'Autores':
                authors = ', '.join([f"{author['Nome próprio']} {author['Apelido']}" for author in value])
                text_widget.insert(tk.END, f"{key}: {authors}\n")
            else:
                text_widget.insert(tk.END, f"{key}: {', '.join(value)}\n")
        text_widget.insert(tk.END, "\n")
    
    # Criar uma lista onde irão aparecer as opções 
    listbox = tk.Listbox(popup)
    listbox.pack()

    # Adicionar as opções
    for i, reference in enumerate(references, start=1):
        listbox.insert(tk.END, f"Referência {i}")

    # Função para eliminar a referência selecionada na listbox
    def delete_selected():
        selected_index = listbox.curselection()
        if selected_index:
            index = selected_index[0]
            references.pop(index)
            listbox.delete(index)
            popup.destroy()
    
    delete_button = tk.Button(popup, text="Eliminar referência selecionada", command=delete_selected)
    delete_button.pack()
   
#%%

# Função para adicionar uma referência manualmente

def manual_ref():
    popup = tk.Toplevel()
    popup.title('Inserção manual')

    author_list = []
    kw_list = []
    
    def author_entry():
        author_frame = tk.Frame(popup)
        author_frame.pack()

        first_name = tk.Entry(author_frame)
        first_name.insert(0, 'Primeiro nome')
        first_name.grid(row=0, column=0, padx=5)
        last_name = tk.Entry(author_frame)
        last_name.insert(0,'Apelido')
        last_name.grid(row=0, column=1, padx=5)

        author_list.append((first_name, last_name))
        

    def kw_entry():
        kw_frame = tk.Frame(popup)
        kw_frame.pack()

        keyword = tk.Entry(kw_frame)
        keyword.insert(0, 'Palavra-chave')
        keyword.pack()
        kw_list.append((keyword))
        
        
    
    title_entry = tk.Entry(popup)
    title_entry.insert(0, 'Título da publicação')
    title_entry.pack()
    
    n = tk.StringVar()
    type_entry = ttk.Combobox(popup, textvariable=n)
    type_entry['values'] = ('ABST', # ABSTRACT
                            'BLOG', # BLOG POST
                            'BOOK', # BOOK
                            'CASE', # CASE REPORT
                            'CHAP', # BOOK CHAPTER
                            'DBASE', # DATABASE
                            'EBOOK', # ELECTRONIC BOOK
                            'ECHAP', # ELECTRONIC BOOK CHAPTER
                            'EJOUR', # ELECTRONIC ARTICLE
                            'JOUR', # JOURNAL
                            'NEWS', # NEWSPAPER
                            'RPRT', # REPORT
                            'THES', # THESIS/DISSERTATION
                            'UNPB', # UNPUBLISHED
                            'WEB') # WEB PAGE
    type_entry.pack()
    
    year_entry = tk.Entry(popup)
    year_entry.insert(0, 'Ano')
    year_entry.pack()
    
    local_entry = tk.Entry(popup)
    local_entry.insert(0, 'Local de publicação')
    local_entry.pack()
    
    pagenum_entry = tk.Entry(popup)
    pagenum_entry.insert(0, 'Número de páginas')
    pagenum_entry.pack()
    
    doi_entry = tk.Entry(popup)
    doi_entry.insert(0, 'DOI')
    doi_entry.pack()
    
    kw_entry()
    add_kw_button = tk.Button(popup, text="Adicionar outra palavra-chave", command=kw_entry)
    add_kw_button.pack()
    
    def save_reference():
        authors_info = [{'Nome próprio': fn.get(), 'Apelido': ln.get()} for fn, ln in author_list]
        keywords = [keyword.get() for keyword in kw_list]
        
        info = {
            'Título': [title_entry.get()],
            'Tipo de publicação': [type_entry.get()],
            'Autores':authors_info,
            'Ano':[year_entry.get()],
            'Local de publicação': [local_entry.get()],
            'Número de páginas': [pagenum_entry.get()],
            'DOI': [doi_entry.get()],
            'Palavras-chave': keywords   
        }
        
        if info not in references:
            references.append(info)
            popup.destroy()
        else:
            popup.destroy()
    
    author_entry_label = tk.Label(popup, text='Autor:')
    author_entry_label.pack()    
    author_entry()
    add_author_button = tk.Button(popup, text="Adicionar outro autor", command=author_entry)
    add_author_button.pack()
    
    save_button = tk.Button(popup, text="Guardar referência", command=save_reference)
    save_button.pack()

#%%

# Função para adicionar uma referência automaticamente a partir de um ficheiro RIS

def read_ref():
    file = filedialog.askopenfilename(title="Selecione um ficheiro RIS")

    if file:
        info = {'Título': [],
                'Tipo de publicação': [],
                'Autores': [],
                'Ano': [],
                'Local de publicação': [],
                'Número de páginas': [],
                'DOI': [],
                'Palavras-chave': []}

        lines = open(file).read().split('\n')

        start_page = 0 # Variáveis inicializadas para os casos onde não existe informação sobre o nmr de páginas, para não dar erro (fica 0 páginas)
        end_page = 0

        for line in lines:
            if line.startswith('TI') or line.startswith('T1'):
                info['Título'].append(line[6:])
            elif line.startswith('TY'):
                info['Tipo de publicação'].append(line[6:])
            elif line.startswith('AU') or line.startswith('A1'):
                author_name = line[6:].strip()
                last_name, first_name = author_name.split(', ')
                author_info = {'Apelido': last_name, 'Nome próprio': first_name}
                info['Autores'].append(author_info)
            elif line.startswith('PY'):
                info['Ano'].append(line[6:])
            elif line.startswith('CY') or line.startswith('PP') or line.startswith('T2'):
                info['Local de publicação'].append(line[6:])
            elif line.startswith('DO'):
                info['DOI'].append(line[6:])
            elif line.startswith('KW'):
                info['Palavras-chave'].append(line[6:])
            elif line.startswith('SP'):
                start_page = int(line[6:])
            elif line.startswith('EP'):
                end_page = int(line[6:])

    info['Número de páginas'].append(str(end_page - start_page))
    
    if info not in references: # Condição para não adicionar referências repetidas
        return references.append(info)

#%%

# Função para alterar os parâmetros definidos no enunciado

def modify_ref():
    popup = tk.Toplevel()
    popup.title('Modificar uma referência')
    
    text_widget = tk.Text(popup)
    text_widget.pack()
    
    def update_display(): # Função para dar refresh à lista de referências após uma alteração
        text_widget.delete('1.0', 'end')
        for i, reference in enumerate(references, start=1):
            text_widget.insert(tk.END, f"{i}.\n")
            for key, value in reference.items():
                if key == 'Autores':
                    authors = ', '.join([f"{author['Nome próprio']} {author['Apelido']}" for author in value])
                    text_widget.insert(tk.END, f"{key}: {authors}\n")
                else:
                    text_widget.insert(tk.END, f"{key}: {', '.join(value)}\n")
            text_widget.insert(tk.END, "\n")
            
    update_display()
    
    def update_reference():
            popup = tk.Toplevel()
            popup.title('Atualizar referência')
            selected_index = int(reference_combobox.get())
            parameter = parameter_combobox.get()
            operation = operation_combobox.get()
    
            if parameter == "Autores":
                if operation == "Inserir":
                    new_first_name_label = tk.Label(popup, text="Novo nome próprio:")
                    new_first_name_label.pack()
                    new_first_name_entry = tk.Entry(popup)
                    new_first_name_entry.pack()
                    
                    new_last_name_label = tk.Label(popup, text="Novo apelido:")
                    new_last_name_label.pack()
                    new_last_name_entry = tk.Entry(popup)
                    new_last_name_entry.pack()
                    
                    def author_add():
                        author_info = {'Apelido': str(new_last_name_entry.get()), 'Nome próprio': str(new_first_name_entry.get())}
                        references[selected_index - 1]['Autores'].append(author_info)
                        update_display()
                        popup.destroy()
                        
                    save_author = tk.Button(
                        popup,
                        text='Adicionar autor',
                        command=author_add)
                    save_author.pack()
                    
                    
                elif operation == "Eliminar":
                    author_widget = tk.Text(popup)
                    for key, value in enumerate(references[selected_index-1]['Autores']):
                        author_widget.insert(tk.END, f"{key+1}: {value['Nome próprio']} {value['Apelido']}\n")
                    author_widget.pack()
                    author_label = tk.Label(popup, text='Selecione o autor a eliminar:')
                    author_label.pack()
                    author_combobox = ttk.Combobox(popup, values=[str(i+1) for i in range(len(references[selected_index-1]['Autores']))])
                    author_combobox.pack()
                    
                    def author_delete():
                        author_index = int(author_combobox.get()) - 1
                        del references[selected_index - 1]['Autores'][author_index]
                        update_display()
                        popup.destroy()
                        
                    save_author = tk.Button(
                        popup,
                        text='Eliminar autor',
                        command=author_delete)
                    save_author.pack()
                    
                elif operation == "Alterar":
                    author_widget = tk.Text(popup)
                    for key, value in enumerate(references[selected_index-1]['Autores']):
                        author_widget.insert(tk.END, f"{key+1}: {value['Nome próprio']} {value['Apelido']}\n")
                    author_widget.pack()
                    author_label = tk.Label(popup, text='Selecione o autor a alterar:')
                    author_label.pack()
                    author_combobox = ttk.Combobox(popup, values=[str(i+1) for i in range(len(references[selected_index-1]['Autores']))])
                    author_combobox.pack()
                    new_first_name_label = tk.Label(popup, text="Novo nome próprio:")
                    new_first_name_label.pack()
                    new_first_name_entry = tk.Entry(popup)
                    new_first_name_entry.pack()
                    
                    new_last_name_label = tk.Label(popup, text="Novo apelido:")
                    new_last_name_label.pack()
                    new_last_name_entry = tk.Entry(popup)
                    new_last_name_entry.pack()
                    
                    def author_modify():
                        author_index = int(author_combobox.get())-1
                        new_last_name = new_last_name_entry.get()
                        new_first_name = new_first_name_entry.get()
                        references[selected_index - 1]['Autores'][author_index]['Apelido'] = new_last_name
                        references[selected_index - 1]['Autores'][author_index]['Nome próprio'] = str(new_first_name)
                        update_display()
                        popup.destroy()
                        
                    save_author = tk.Button(
                        popup,
                        text='Alterar autor',
                        command=author_modify)
                    save_author.pack()
                    
            if parameter == "Palavras-chave":
                if operation == "Inserir":
                    new_kw_label = tk.Label(popup, text='Nova palavra-chave:')
                    new_kw_label.pack()
                    new_kw = tk.Entry(popup)
                    new_kw.pack()
                    
                    def kw_add():
                        references[selected_index - 1]['Palavras-chave'].append(new_kw.get())
                        update_display()
                        popup.destroy()
                        
                    save_kw = tk.Button(
                        popup,
                        text='Adicionar palavra-chave',
                        command=kw_add)
                    save_kw.pack()
                    
                elif operation == "Eliminar":
                    kw_widget = tk.Text(popup)
                    for key, value in enumerate(references[selected_index-1]['Palavras-chave']):
                        kw_widget.insert(tk.END, f"{key+1}: {value}\n")
                    kw_widget.pack()
                    kw_label = tk.Label(popup, text='Selecione a palavra-chave a eliminar:')
                    kw_label.pack()
                    kw_combobox = ttk.Combobox(popup, values=[str(i + 1) for i in range(len(references[selected_index-1]['Palavras-chave']))])
                    kw_combobox.pack()
    
                    def kw_delete():
                        keyword_index = int(kw_combobox.get()) - 1
                        del references[selected_index - 1]['Palavras-chave'][keyword_index]
                        update_display()
                        popup.destroy()
            
                    save_kw = tk.Button(
                        popup,
                        text='Eliminar palavra-chave',
                        command=kw_delete)
                    save_kw.pack()
                
                elif operation == "Alterar":
                    kw_widget = tk.Text(popup)
                    for key, value in enumerate(references[selected_index-1]['Palavras-chave']):
                        kw_widget.insert(tk.END, f"{key+1}: {value}\n")
                    kw_widget.pack()
                    kw_label = tk.Label(popup, text='Selecione a palavra-chave a alterar:')
                    kw_label.pack()
                    kw_combobox = ttk.Combobox(popup, values=[str(i + 1) for i in range(len(references[selected_index-1]['Palavras-chave']))])
                    kw_combobox.pack()
            
                    new_kw_label = tk.Label(popup, text='Nova palavra-chave:')
                    new_kw_label.pack()
                    new_kw_entry = tk.Entry(popup)
                    new_kw_entry.pack()
            
                    def kw_modify():
                        keyword_index = int(kw_combobox.get()) - 1
                        new_keyword = new_kw_entry.get()
                        references[selected_index - 1]['Palavras-chave'][keyword_index] = new_keyword
                        update_display()
                        popup.destroy()
            
                    save_kw = tk.Button(
                        popup,
                        text='Alterar palavra-chave',
                        command=kw_modify)
                    save_kw.pack()
        
    ref_label = tk.Label(popup, text='Selecione a referência a modificar:')
    ref_label.pack()
    reference_combobox = ttk.Combobox(popup, values=[str(i + 1) for i in range(len(references))])
    reference_combobox.pack()
    
    parameter_label = tk.Label(popup, text="Parâmetro:")
    parameter_label.pack()
    parameter_combobox = ttk.Combobox(popup, values=["Autores", "Palavras-chave"])
    parameter_combobox.pack()
    
    operation_label = tk.Label(popup, text="Operação:")
    operation_label.pack()
    operation_combobox = ttk.Combobox(popup, values=["Inserir", "Eliminar", "Alterar"])
    operation_combobox.pack()

    update_button = tk.Button(popup, text="Atualizar Referência", command=update_reference)
    update_button.pack()
    
#%%
# Função para calcular e mostrar os dados estatísticos através da criação de listas
def statistics_page():
    popup = tk.Toplevel()
    popup.title('Estatísticas da biblioteca')
    
    author_list = []
    for i in range(len(references)):
        for j in references[i]['Autores']:
            if f"{j['Nome próprio']} {j['Apelido']}" not in author_list:
                author_list.append(f"{j['Nome próprio']} {j['Apelido']}")
    
    kw_list = []
    for i in references:
        for j in i["Palavras-chave"]:
            if j not in kw_list:
                kw_list.append(j)
    
    page_list=[]
    for i in references:
        page_list.append(int(i["Número de páginas"][0]))
    total=sum(page_list)
    
    pagemean_list=[]
    for i in references:
        pagemean_list.append(int(i["Número de páginas"][0]))
    if len(pagemean_list) != 0:
        mean=int(sum(pagemean_list)/len(pagemean_list))
    else:
        mean = 0
    
    text_widget = tk.Text(popup)
    text_widget.insert(tk.END, f"A sua biblioteca contém {len(references)} referências.\nO número total de autores na base de dados é de {len(author_list)}.\nO número total de palavras-chave na base de dados é de {len(kw_list)}.\nO número de páginas na base de dados é {total}.\nO número médio de páginas na base de dados é {mean}.")
    text_widget.pack()
    
    def list_authors(): # Função para mostrar a lista de autores
        text_widget.delete('1.0', 'end')
        text_widget.insert(tk.END, f"O número total de autores na base de dados é de {len(author_list)}.\n\n")
        text_widget.insert(tk.END, '\n'.join(author_list))
    
    def list_kw(): # Função para mostrar a lista de palavras-chave
        text_widget.delete('1.0', 'end') 
        text_widget.insert(tk.END, f"O número total de palavras-chave na base de dados é de {len(kw_list)}.\n\n")
        text_widget.insert(tk.END, '\n'.join(kw_list))
        
    def list_ty(): # Função para mostrar a lista de referências conforme o tipo da publicação: definir o tipo
        text_widget.delete('1.0', 'end')
        popup = tk.Toplevel()
        popup.title('Escolha')
        parameter_label = tk.Label(popup, text='Escolha o tipo de publicação que pretende filtrar:')
        parameter_label.pack()
        n = tk.StringVar()
        type_entry = ttk.Combobox(popup, textvariable=n)
        type_entry['values'] = ('ABST', # ABSTRACT
                                'BLOG', # BLOG POST
                                'BOOK', # BOOK
                                'CASE', # CASE REPORT
                                'CHAP', # BOOK CHAPTER
                                'DBASE', # DATABASE
                                'EBOOK', # ELECTRONIC BOOK
                                'ECHAP', # ELECTRONIC BOOK CHAPTER
                                'EJOUR', # ELECTRONIC ARTICLE
                                'JOUR', # JOURNAL
                                'NEWS', # NEWSPAPER
                                'RPRT', # REPORT
                                'THES', # THESIS/DISSERTATION
                                'UNPB', # UNPUBLISHED
                                'WEB') # WEB PAGE
        type_entry.pack()
        
        def choice_ty(): # Função para mostrar a lista de referências conforme o tipo da publicação: encontrar publicações do tipo
            parameter = type_entry.get()
            type_list = []
            for i in range(len(references)):
                if parameter == references[i]["Tipo de publicação"][0]:
                    type_list.append(references[i])
            if len(type_list) == 0:
                text_widget.insert(tk.END, 'Não existem publicações desse tipo.')
            else:
                for i, reference in enumerate(type_list, start=1):
                    text_widget.insert(tk.END, f"{i}.\n")
                    for key, value in reference.items():
                        if key == 'Autores':
                            authors = ', '.join([f"{author['Nome próprio']} {author['Apelido']}" for author in value])
                            text_widget.insert(tk.END, f"{key}: {authors}\n")
                        else:
                            text_widget.insert(tk.END, f"{key}: {', '.join(value)}\n")
                    text_widget.insert(tk.END, "\n")
            popup.destroy()
                    
        ok_button = tk.Button(popup, text='Ok', command=choice_ty)
        ok_button.pack()
    
    def list_year(): # Função para mostrar a lista de referências conforme o tipo da ano: definir o ano
        text_widget.delete('1.0', 'end')
        popup = tk.Toplevel()
        popup.title('Inserir')
        parameter_label = tk.Label(popup, text='Insira o ano das publicações que quer encontrar:')
        parameter_label.pack()
        year_entry = tk.Entry(popup)
        year_entry.pack()
        
        def choice_y(): # Função para mostrar a lista de referências conforme o tipo da publicação: encontrar publicações do ano
            year = year_entry.get()
            year_list = []
            for reference in references:
                if year == reference["Ano"][0]:
                    year_list.append(reference)
            if len(year_list) == 0:
                text_widget.insert(tk.END, 'Não existem publicações desse ano.')
            else:
                for i, reference in enumerate(year_list, start=1):
                    text_widget.insert(tk.END, f"{i}.\n")
                    for key, value in reference.items():
                        if key == 'Autores':
                            authors = ', '.join([f"{author['Nome próprio']} {author['Apelido']}" for author in value])
                            text_widget.insert(tk.END, f"{key}: {authors}\n")
                        else:
                            text_widget.insert(tk.END, f"{key}: {', '.join(value)}\n")
                    text_widget.insert(tk.END, "\n")
            popup.destroy()
                    
        ok_button = tk.Button(popup, text='Ok', command=choice_y)
        ok_button.pack()
        
    def list_pub_with_kw(): # Função para mostrar a lista de referências conforme uma ou mais palavras-chave: criação de listas e formatação da janela
        popup = tk.Toplevel()
        popup.title('Palavras-chave')
        kw_list = []
        publication_list = []
        parameter_label = tk.Label(popup, text='Insira a(s) palavra(s)-chave desejada(s):')
        parameter_label.pack()
        
        def kw_entry():  # Função para mostrar a lista de referências conforme uma ou mais palavras-chave: entrada da(s) palavra(s)-chave
            kw_frame = tk.Frame(popup)
            kw_frame.pack()
            keyword_entry = tk.Entry(kw_frame)
            keyword_entry.pack()
            kw_list.append(keyword_entry)
        
        kw_entry()
        add_kw_button = tk.Button(popup, text="Adicionar outra palavra-chave", command=kw_entry)
        add_kw_button.pack()
        
        def kw_list_make(): # Função para mostrar a lista de referências conforme uma ou mais palavras-chave: encontrar as referências que contenham a(s) palavra(s)-chave
            publication_list.clear()
            keywords = [keyword.get() for keyword in kw_list]
            input_keywords = [unidecode.unidecode(kw.casefold()).translate(str.maketrans('', '', string.punctuation)).replace(' ', '') for kw in keywords]
            for reference in references:
                keywords = reference.get("Palavras-chave", [])
                keywords = [unidecode.unidecode(kw.casefold()).translate(str.maketrans('', '', string.punctuation)).replace(' ', '') for kw in keywords]
                if all(kw in keywords for kw in input_keywords):
                    publication_list.append(reference)
            
            text_widget.delete('1.0', tk.END)
                            
            if len(publication_list) == 0:
                text_widget.insert(tk.END, 'Não existem publicações com essas palavras-chave.')
            else:
                for i, reference in enumerate(publication_list, start=1):
                    text_widget.insert(tk.END, f"{i}.\n")
                    for key, value in reference.items():
                        if key == 'Autores':
                            authors = ', '.join([f"{author['Nome próprio']} {author['Apelido']}" for author in value])
                            text_widget.insert(tk.END, f"{key}: {authors}\n")
                        else:
                            text_widget.insert(tk.END, f"{key}: {', '.join(value)}\n")
                    text_widget.insert(tk.END, "\n")
                
        ok_button = tk.Button(popup, text='Ok', command=kw_list_make)
        ok_button.pack()
        
        
    def list_pub_with_author(): # Função para mostrar a lista de referências de um determinado autor: entrada do autor
        popup = tk.Toplevel()
        popup.title = 'Autor'
        publication_list = []
        parameter_label = tk.Label(popup, text='Insira o nome completo ou o apelido do autor:')
        parameter_label.pack()
        author_name_entry = tk.Entry(popup)
        author_name_entry.pack()

        
        def authorpub_list_make(): # Função para mostrar a lista de referências de um determinado autor: encontrar referências do autor
            publication_list.clear()
            author_name = author_name_entry.get()
            author_name = (unidecode.unidecode((author_name.casefold()).translate(str.maketrans('', '', string.punctuation)))).replace(' ', '')                       
            for i in range(len(references)):
                for j in references[i]["Autores"]:
                    apelido = (j["Apelido"])
                    nome = f"{j['Nome próprio']} {j['Apelido']}"
                    if author_name == (unidecode.unidecode((apelido.casefold()).translate(str.maketrans('', '', string.punctuation))).replace(' ', '')) or author_name == (unidecode.unidecode((nome.casefold()).translate(str.maketrans('', '', string.punctuation))).replace(' ', '')):
                        publication_list.append(references[i])
            
            text_widget.delete('1.0', tk.END)
            
            if len(publication_list) == 0:
                text_widget.insert(tk.END, 'Não existem publicações desse autor.')
            else:
                for i, reference in enumerate(publication_list, start=1):
                    text_widget.insert(tk.END, f"{i}.\n")
                    for key, value in reference.items():
                        if key == 'Autores':
                            authors = ', '.join([f"{author['Nome próprio']} {author['Apelido']}" for author in value])
                            text_widget.insert(tk.END, f"{key}: {authors}\n")
                        else:
                            text_widget.insert(tk.END, f"{key}: {', '.join(value)}\n")
                    text_widget.insert(tk.END, "\n")
            
        ok_button = tk.Button(popup, text='Ok', command=authorpub_list_make)
        ok_button.pack()
        
# Associar funções aos botões
        
    lista_autores_button = tk.Button(
        popup,
        text='Lista de autores',
        command=list_authors)
    lista_autores_button.pack()
    
    lista_kw_button = tk.Button(
        popup,
        text='Lista de palavras-chave',
        command=list_kw)
    lista_kw_button.pack()
    
    lista_ty_button = tk.Button(
        popup,
        text='Lista de artigos por tipo',
        command=list_ty)
    lista_ty_button.pack()
    
    lista_anos_button = tk.Button(
        popup,
        text='Lista de artigos por ano',
        command=list_year)
    lista_anos_button.pack()
    
    lista_kwlist_button = tk.Button(
        popup,
        text='Lista de artigos por palavra(s)-chave',
        command=list_pub_with_kw)
    lista_kwlist_button.pack()
    
    lista_authorlist_button = tk.Button(
        popup,
        text='Lista de artigos por autor',
        command=list_pub_with_author)
    lista_authorlist_button.pack()
    
#%%

# Criação do menu principal

window = tk.Tk() # Se abrir uma janela extra vazia, trocar Toplevel() por Tk(); o programa comporta-se de forma diferente no PC da Carolina por alguma razão
window.title('Gestor de referências')
window.iconbitmap("ico.ico")

logo = tk.PhotoImage(file="logofullresize.png")
logo_label = tk.Label(window,image=logo).pack(pady=20)

biblioteca_button = tk.Button(
    window,
    text='A minha biblioteca',
    command=biblioteca)

biblioteca_button.pack(
    ipadx=5,
    ipady=5,
    expand=True)

manualref_button = tk.Button(
    window,
    text='Inserir referência manualmente',
    command=manual_ref)

manualref_button.pack(
    ipadx=5,
    ipady=5,
    expand=True)

readref_button = tk.Button(
    window,
    text='Inserir referência a partir de um ficheiro RIS',
    command =read_ref)

readref_button.pack(
    ipadx=5,
    ipady=5,
    expand=True)

modref_button = tk.Button(
    window,
    text='Editar uma referência',
    command=modify_ref)

modref_button.pack(
    ipadx=5,
    ipady=5,
    expand=True)

delref_button = tk.Button(
    window,
    text='Eliminar uma referência',
    command=del_ref)

delref_button.pack(
    ipadx=5,
    ipady=5,
    expand=True)

stats_button = tk.Button(
    window,
    text='Estatísticas',
    command=statistics_page)

stats_button.pack(
    ipadx=5,
    ipady=5,
    expand=True)

window.protocol("WM_DELETE_WINDOW", save_on_exit) # Chama a função para guardar as referências no documento de texto quando o utilizador fecha a aplicação

window.mainloop()