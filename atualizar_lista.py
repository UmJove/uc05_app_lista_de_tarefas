import customtkinter as ctk
import json
import funcoes_back

def atualizar_lista(frame_lista):
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

            tarefas = [t for t in tarefas if t["usuario"] == funcoes_back.user]

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