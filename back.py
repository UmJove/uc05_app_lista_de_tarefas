import json
from datetime import datetime
from tkinter import messagebox
import customtkinter as ctk
import	tkinter

def salvar(atividade, data, hora):
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
O que podemos fazer é olhar para frente, aprender com o que vivemos e decidir com sabedoria onde investir nosso tempo daqui para frente, pois o presente é o único momento onde podemos agir e transformar nosso destino."""
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
            "hora": hora
        })

        # Salva de volta
        with open("tarefas.json", "w") as f:
            json.dump(tarefas, f, indent=4)

        messagebox.showinfo("Sucesso", "Tarefa criada com sucesso!")

    except ValueError:
        messagebox.showerror(
            "Erro",
            "Data ou hora inválida, use o formato dd/mm/aaaa para a data e hh:mm para a hora."
        )







def deletar_tarefa(atividade, data, hora):
    try:
        with open("tarefas.json", "r") as f:
            tarefas = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showerror("Nenhuma tarefa encontrada para deletar.")
        return

    # Filtra as tarefas para remover a que bate com os parâmetros
    tarefas_filtradas = [
        t for t in tarefas
        if not (t["atividade"] == atividade and t["data"] == data and t["hora"] == hora)
    ]

    if len(tarefas_filtradas) == len(tarefas):
        messagebox.showinfo("Aviso", "Tarefa não encontrada.")
        return

    # Salva a lista atualizada
    with open("tarefas.json", "w") as f:
        json.dump(tarefas_filtradas, f, indent=4)

    messagebox.showinfo("Sucesso", "Tarefa deletada com sucesso!")



