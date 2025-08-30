import json
from datetime import datetime
from tkinter import messagebox
import customtkinter as ctk




def salvar(user, frame_lista, atividade, data, hora, parent=None):
    agora = datetime.now()
    try:
        data_obj = datetime.strptime(data, "%d/%m/%Y")
        hora_obj = datetime.strptime(hora, "%H:%M").time()
        data_completa = datetime.combine(data_obj.date(), hora_obj)

        if data_completa < agora:
            messagebox.showerror(
                "Erro",
                """O tempo que já passou é um rio que não volta para sua nascente. 
Tentar marcar um compromisso no passado é como querer reescrever páginas já escritas no livro da vida — impossível e desnecessário. 
O que podemos fazer é olhar para frente, aprender com o que vivemos e decidir com sabedoria onde investir nosso tempo daqui para frente, pois o presente é o único momento onde podemos agir e transformar nosso destino.""",
                parent=parent
            )
            return

        try:
            with open("tarefas.json", "r") as f:
                tarefas = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            tarefas = []

        tarefas.append({
            "atividade": atividade,
            "data": data,
            "hora": hora,
            "concluida": False,
            "usuario": user  # Corrigido de "user" para "usuario"
        })

        with open("tarefas.json", "w") as f:
            json.dump(tarefas, f, indent=4)

        messagebox.showinfo("Sucesso", "Tarefa criada com sucesso!", parent=parent)
        atualizar_lista(user, frame_lista)

    except ValueError:
        messagebox.showerror(
            "Erro",
            "Data ou hora inválida, use o formato dd/mm/aaaa para a data e hh:mm para a hora.",
            parent=parent
        )


def deletar_tarefa(atividade, data, hora, usuario_logado, parent=None):
    try:
        with open("tarefas.json", "r") as f:
            tarefas = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showerror("Erro", "Nenhuma tarefa encontrada para deletar.", parent=parent)
        return

    tarefas_filtradas = [
        t for t in tarefas
        if not (t["atividade"] == atividade and t["data"] == data and t["hora"] == hora and t["usuario"] == usuario_logado)
    ]

    if len(tarefas_filtradas) == len(tarefas):
        messagebox.showinfo("Aviso", "Tarefa não encontrada ou não pertence ao usuário logado.", parent=parent)
        return

    with open("tarefas.json", "w") as f:
        json.dump(tarefas_filtradas, f, indent=4)

    messagebox.showinfo("Sucesso", "Tarefa deletada com sucesso!", parent=parent)
    


def atualizar_lista(user, frame_lista):
        for widget in frame_lista.winfo_children():
            widget.destroy()
            
            
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

  
        try:
            with open("tarefas.json", "r") as f:
                tarefas = json.load(f)

            tarefas = [t for t in tarefas if t["usuario"] == user]

        except (FileNotFoundError, json.JSONDecodeError):
            tarefas = []
        
        def atualizar_status_concluida(index,var):
            with open("tarefas.json", "r") as f:
                tarefas = json.load(f)
            tarefas[index-2]["concluida"] = var.get()
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