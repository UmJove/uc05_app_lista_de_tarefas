# Sistema: Aplicação de gerênciamento de tarefas pesssoais
import customtkinter as ctk
from tkinter import messagebox
from back import salvar
from back import deletar_tarefa
import json




# Adicionar tarefa
def criar_tarefa():
    nova_tarefa = ctk.CTkToplevel()
    nova_tarefa.title("Nova tarefa")
    nova_tarefa.geometry("450x200")
    nova_tarefa.focus()
    nova_tarefa.attributes('-topmost', True)

    # ajustando colunas
    nova_tarefa.columnconfigure(0, weight=1)
    nova_tarefa.columnconfigure(1, weight=1)
    nova_tarefa.columnconfigure(2, weight=0)
    nova_tarefa.columnconfigure(3, weight=1)

    # Título da página
    titulo_criar_tarefa = ctk.CTkLabel(nova_tarefa, text="Nova Tarefa", font=("Helvetica", 16))
    titulo_criar_tarefa.grid(row=0, column=0, columnspan=4, pady=(20,10))


    # Atividade
    atividade_label = ctk.CTkLabel(nova_tarefa, text="Atividade:")
    atividade_label.grid(row=1, column=0, padx=(20, 10), pady=(5,10), sticky="e")

    atividade_entry = ctk.CTkEntry(nova_tarefa, placeholder_text="Digite aqui nome da atividade a realizar", width=300)
    atividade_entry.grid(row=1, column=1, sticky="w", columnspan=3)

    # Data
    data_label = ctk.CTkLabel(nova_tarefa, text="Data:")
    data_label.grid(row=2, column=0, padx=10, pady=(5,10), sticky="e")

    data_entry = ctk.CTkEntry(nova_tarefa, placeholder_text="00/00/0000",  width=100)
    data_entry.grid(row=2, column=1, sticky="w")

    # Horário
    hora_label = ctk.CTkLabel(nova_tarefa, text="Horário:")
    hora_label.grid(row=2, column=2, padx=10, pady=(5,10), sticky="e")

    hora_entry = ctk.CTkEntry(nova_tarefa, placeholder_text="00:00",  width=100)
    hora_entry.grid(row=2, column=3, sticky="w")

    # Frame botoes
    frame_btn_nova_tarefa = ctk.CTkFrame(nova_tarefa, width=500, fg_color="transparent")
    frame_btn_nova_tarefa.grid(row=3, column=0, columnspan=4, pady=15)

    # btn_salvar  = 
    btn_salvar = ctk.CTkButton(frame_btn_nova_tarefa, text="Salvar", command=lambda: salvar(atividade=atividade_entry.get(), data=data_entry.get(), hora=hora_entry.get(), parent=nova_tarefa))
    btn_salvar.pack(side="left", padx=(0, 50))

    btn_cancelar = ctk.CTkButton(frame_btn_nova_tarefa, text="Cancelar", fg_color="darkred", hover_color="#a83232", command=nova_tarefa.destroy)
    btn_cancelar.pack(side="right", padx=(50, 0))

def excluir_tarefas():
    excluir_tarefas_win = ctk.CTkToplevel()
    excluir_tarefas_win.title("Excluir tarefas")
    excluir_tarefas_win.geometry("500x530")
    excluir_tarefas_win.focus()
    excluir_tarefas_win.attributes('-topmost', True)

    ctk.CTkLabel(excluir_tarefas_win, text="Excluir tarefas", font=("Helvetica", 14)).pack(pady=(20,10))
    
    frame_lista_excluir = ctk.CTkScrollableFrame(excluir_tarefas_win, width=430, height=350)
    frame_lista_excluir.pack(pady=5)
    frame_lista_excluir.columnconfigure([0,2,3], weight=0)
    frame_lista_excluir.columnconfigure(1, weight=1)

    # Cabeçalhos
    ctk.CTkLabel(frame_lista_excluir, text="Selecione tarefa(s) que deseja excluir").grid(row=0, column=0, columnspan=4, pady=(20,10))

    ctk.CTkLabel(frame_lista_excluir, text="Atividade").grid(row=1, column=1, padx=15, sticky="w")
    ctk.CTkLabel(frame_lista_excluir, text="Data").grid(row=1, column=2, padx=15)
    ctk.CTkLabel(frame_lista_excluir, text="Hora").grid(row=1, column=3, padx=15)

    # Tenta carregar tarefas
    try:
        with open("tarefas.json", "r") as f:
            tarefas = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        tarefas = []

    # Guarda checkboxes com as tarefas
    checkboxes = []
    for i, tarefa in enumerate(tarefas, start=2):
        var = ctk.BooleanVar()
        checkbox = ctk.CTkCheckBox(frame_lista_excluir, variable=var, text="", width=15)
        checkbox.grid(row=i, column=0, padx=(15,5), sticky="e")

        ctk.CTkLabel(frame_lista_excluir, text=tarefa["atividade"]).grid(row=i, column=1, padx=(5,15), sticky="w")
        ctk.CTkLabel(frame_lista_excluir, text=tarefa["data"]).grid(row=i, column=2, padx=15)
        ctk.CTkLabel(frame_lista_excluir, text=tarefa["hora"]).grid(row=i, column=3, padx=15)

        checkboxes.append((var, tarefa))

    def confirmar_exclusao():
        selecionadas = [t for var, t in checkboxes if var.get()]
        if not selecionadas:
            messagebox.showinfo("Aviso", "Nenhuma tarefa selecionada para exclusão.", parent=excluir_tarefas_win)
            return
        
        # Chama a função do back para deletar cada tarefa marcada
        for tarefa in selecionadas:
            deletar_tarefa(tarefa["atividade"], tarefa["data"], tarefa["hora"], parent=excluir_tarefas_win)

        excluir_tarefas_win.destroy()

    btn_excluir = ctk.CTkButton(excluir_tarefas_win, text="Excluir selecionadas", command=confirmar_exclusao)
    btn_excluir.pack(pady=20)

def main():
    def lista_atualizada():
        titulo_lista = ctk.CTkLabel(frame_lista, text="Tarefas", font=("Helvetica", 14))
        titulo_lista.grid(row=0, column=0, columnspan=4, pady=5)

        label_status_topo = ctk.CTkLabel(frame_lista, text="Status")
        label_status_topo.grid(row=1, column=0, padx=(15))

        label_atividade_topo = ctk.CTkLabel(frame_lista, text="Atividade")
        label_atividade_topo.grid(row=1, column=1, padx=(5,15), sticky="w")

        label_dia_topo = ctk.CTkLabel(frame_lista, text="Dia")
        label_dia_topo.grid(row=1, column=2, padx=(15))

        label_hora_topo = ctk.CTkLabel(frame_lista, text="Horário")
        label_hora_topo.grid(row=1, column=3, padx=(15))

        # Lê tarefas do JSON
        try:
            with open("tarefas.json", "r") as f:
                tarefas = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            tarefas = []
        
        def atualizar_status_concluida(index,var):
            with open("tarefas.json", "r") as f:
                tarefas = json.load(f)
            tarefas[index]["concluida"] = var.get()
            with open("tarefas.json", "w") as f:
                json.dump(tarefas, f, indent=4)

        for i, tarefa in enumerate(tarefas, start=2):
            check_var = ctk.BooleanVar(value=tarefa.get("concluida", False)) 
            checkbox = ctk.CTkCheckBox(frame_lista, text="", width=20, variable=check_var, command=lambda idx=i, v=check_var: atualizar_status_concluida(idx, v), checkbox_width=20, checkbox_height=20, corner_radius=10, fg_color="darkgreen", hover_color="green")
            checkbox.grid(row=i, column=0, padx=(15))

            label_atividade = ctk.CTkLabel(frame_lista, text=tarefa["atividade"])
            label_atividade.grid(row=i, column=1, padx=(5,15), sticky="w")

            label_dia = ctk.CTkLabel(frame_lista, text=tarefa["data"])
            label_dia.grid(row=i, column=2, padx=(15))

            label_hora = ctk.CTkLabel(frame_lista, text=tarefa["hora"])
            label_hora.grid(row=i, column=3, padx=(15))
            
    main = ctk.CTk()
    main.title("My Tasks")
    main.geometry("500x600")



    titulo_main = ctk.CTkLabel(main, text="My Tasks", font=("Helvetica", 16))
    titulo_main.pack(pady=(20, 10))

    #Frame botões
    frame_botoes = ctk.CTkFrame(main, width=500, fg_color="transparent")
    frame_botoes.pack(pady=10)

    btn_criar_tarefa = ctk.CTkButton(frame_botoes, text="Criar nova tarefa", command=criar_tarefa)
    btn_criar_tarefa.pack(side="left", padx=(0, 80))

    btn_editar_lista = ctk.CTkButton(frame_botoes, text="Excluir tarefas", command=excluir_tarefas)
    btn_editar_lista.pack(side="right", padx=(80, 0))


    # Frame de lista de atividades
    frame_lista = ctk.CTkScrollableFrame(main, width=430, height=400)
    frame_lista.pack(pady=5)

    frame_lista.columnconfigure([0,2,3], weight=0)
    frame_lista.columnconfigure(1, weight=1)


    btn_atualizar = ctk.CTkButton(main, text="Atualizar lista", command=lista_atualizada)
    btn_atualizar.pack(pady=(20))

    titulo_lista = ctk.CTkLabel(frame_lista, text="Tarefas", font=("Helvetica", 14))
    titulo_lista.grid(row=0, column=0, columnspan=4, pady=5)

    label_status_topo = ctk.CTkLabel(frame_lista, text="Status")
    label_status_topo.grid(row=1, column=0, padx=(15))

    label_atividade_topo = ctk.CTkLabel(frame_lista, text="Atividade")
    label_atividade_topo.grid(row=1, column=1, padx=(5,15), sticky="w")

    label_dia_topo = ctk.CTkLabel(frame_lista, text="Dia")
    label_dia_topo.grid(row=1, column=2, padx=(15))

    label_hora_topo = ctk.CTkLabel(frame_lista, text="Horário")
    label_hora_topo.grid(row=1, column=3, padx=(15))
    

    main.mainloop()



def confirmar_login():
    login_win.destroy()
    main()

def confirmar_cadastro(novo_user, nova_senha):
    pass
    
def cadastro():
    cadastro_win = ctk.CTkToplevel()
    cadastro_win.title("Cadastro")
    cadastro_win.geometry("400x250")
    cadastro_win.focus()
    cadastro_win.attributes("-topmost", True)

    titulo_login = ctk.CTkLabel(cadastro_win, text="Cadastro de usuário")
    titulo_login.grid(row=0,column=0,columnspan=2, pady=10)

    # Rótulos e entradas
    novo_user_label = ctk.CTkLabel(cadastro_win, text="Usuário")
    novo_user_label.grid(row=1,column=0, padx=15, pady=10)

    novo_user_entry = ctk.CTkEntry(cadastro_win, placeholder_text="Digite um nome de usuário")
    novo_user_entry.grid(row=1,column=1, padx=15, pady=10)

    nova_senha_label = ctk.CTkLabel(cadastro_win, text="Senha")
    nova_senha_label.grid(row=2,column=0, padx=15, pady=10)

    nova_senha_entry = ctk.CTkEntry(cadastro_win, placeholder_text="Crie uma senha", show="*")
    nova_senha_entry.grid(row=2,column=1, padx=15, pady=10)

    cadastro_win.columnconfigure(0, weight=1)
    cadastro_win.columnconfigure(1, weight=1)

    # Botões
    btn_confirma = ctk.CTkButton(cadastro_win, text="Confirmar", command=confirmar_cadastro(novo_user_entry.get(), nova_senha_entry.get()))
    btn_confirma.grid(row=4, column=0, pady=10)

    btn_cadastro = ctk.CTkButton(cadastro_win, text="Cancelar", command=cadastro_win.destroy)
    btn_cadastro.grid(row=4, column=1, pady=5)


login_win = ctk.CTk()
login_win.title("Login")
login_win.geometry("400x250")

# Configurações de aparência
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

titulo_login = ctk.CTkLabel(login_win, text="Login")
titulo_login.grid(row=0,column=0,columnspan=2, pady=10)

# Rótulos e entradas
user_label = ctk.CTkLabel(login_win, text="Usuário")
user_label.grid(row=1,column=0, padx=15, pady=10)

user_entry = ctk.CTkEntry(login_win)
user_entry.grid(row=1,column=1, padx=15, pady=10)

senha_label = ctk.CTkLabel(login_win, text="Senha")
senha_label.grid(row=2,column=0, padx=15, pady=10)

senha_entry = ctk.CTkEntry(login_win, show="*")
senha_entry.grid(row=2,column=1, padx=15, pady=10)

login_win.columnconfigure(0, weight=1)
login_win.columnconfigure(1, weight=1)

# Botões
btn_confirma = ctk.CTkButton(login_win, text="Confirma", command=confirmar_login)
btn_confirma.grid(row=3, column=0, pady=10)

btn_cadastro = ctk.CTkButton(login_win, text="Cadastrar usuário", command=cadastro)
btn_cadastro.grid(row=3, column=1, pady=5)

# Iniciar a aplicação
login_win.mainloop()
