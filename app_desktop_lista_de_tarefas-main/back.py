import json
from datetime import datetime
from tkinter import messagebox
import customtkinter as ctk

user = ""

def salvar(atividade, data, hora, parent=None):
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
            "usuario": user  # Corrigido de "user" para "usuario"
        })

        with open("tarefas.json", "w") as f:
            json.dump(tarefas, f, indent=4)

        messagebox.showinfo("Sucesso", "Tarefa criada com sucesso!", parent=parent)

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

