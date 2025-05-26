import tkinter as tk
from tkinter import messagebox, ttk
from Gestor_estudiantes import SistemaEscolar, Estudiante, Profesor, Curso

# === Inicialización del sistema ===
sistema = SistemaEscolar()
sistema.cargar_todo_desde_json("sistema.json")

# === Ventana principal ===
root = tk.Tk()
root.title("Sistema Escolar")
root.geometry("500x600")
root.configure(bg="#f8f0f0")
notebook = ttk.Notebook(root)
notebook.pack_forget()

# === Estilo personalizado ===
style = ttk.Style()
style.theme_use("default")

style.configure("TNotebook", background="#1587df", borderwidth=0)
style.configure("TNotebook.Tab", background="#a9cce3", font=("Arial", 11, "bold"), padding=[10, 5])
style.map("TNotebook.Tab", background=[("selected", "#5dade2")], foreground=[("selected", "white")])

style.configure("TButton", background="#3498db", foreground="white", font=("Arial", 10, "bold"), padding=6)
style.map("TButton", background=[("active", "#2e86c1")])

# === Menú principal ===
frame_menu = tk.Frame(root, bg="#0f4174")
frame_menu.pack(expand=True, fill='both')

tk.Label(frame_menu, text="Menú Principal", font=("Arial", 18, "bold"), bg="#f8f6f0", fg="#2c3e50").pack(pady=30)

def ir_a_pestana(pestana_index):
    frame_menu.pack_forget()
    notebook.select(pestana_index)
    notebook.pack(expand=True, fill='both')

tk.Button(frame_menu, text="Estudiantes", width=30, command=lambda: ir_a_pestana(0)).pack(pady=10)
tk.Button(frame_menu, text="Profesores", width=30, command=lambda: ir_a_pestana(1)).pack(pady=10)
tk.Button(frame_menu, text="Cursos", width=30, command=lambda: ir_a_pestana(2)).pack(pady=10)

def volver_al_menu():
    notebook.pack_forget()
    frame_menu.pack(expand=True, fill='both')

# ==== Pestaña Estudiantes ====

frame_estudiantes = tk.Frame(notebook, bg="#0f4174")
notebook.add(frame_estudiantes, text='Estudiantes')
tk.Label(frame_estudiantes, text="Estudiantes", font=("Arial", 18, "bold"), bg="#f8f6f0", fg="#2c3e50").pack(pady=30)

# Función para registrar estudiante
def registrar_estudiante():
    Id = entry_id.get()
    nombre = entry_nombre.get()
    edad = entry_edad.get()
    correo = entry_correo.get()
    curso = entry_curso.get()

    if not Id or not nombre or not edad.isdigit() or not correo or not curso:
        messagebox.showerror("Error", "Todos los campos deben estar llenos y edad debe ser numérica.")
        return

    if Id in sistema.estudiantes_dict:
        messagebox.showwarning("Advertencia", "Ya existe un estudiante con este ID.")
        return

    estudiante = Estudiante(Id, nombre, int(edad), correo, curso)
    sistema.registrar_estudiante(estudiante)
    sistema.guardar_todo_en_json("sistema.json")
    messagebox.showinfo("Éxito", f"Estudiante {nombre} registrado correctamente.")
    entry_id.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_edad.delete(0, tk.END)
    entry_correo.delete(0, tk.END)
    entry_curso.delete(0, tk.END)

# Función para buscar estudiante por ID
def buscar_estudiante():
    Id = entry_buscar.get()
    estudiante = sistema.buscar_estudiante_por_id(Id)
    if estudiante:
        messagebox.showinfo("Estudiante encontrado", estudiante.mostrar_info())
    else:
        messagebox.showwarning("No encontrado", "No se encontró ningún estudiante con ese ID.")

tk.Label(frame_estudiantes, text="Registrar Estudiante").pack(pady=5)

tk.Label(frame_estudiantes, text="ID").pack()
entry_id = tk.Entry(frame_estudiantes)
entry_id.pack()

tk.Label(frame_estudiantes, text="Nombre").pack()
entry_nombre = tk.Entry(frame_estudiantes)
entry_nombre.pack()

tk.Label(frame_estudiantes, text="Edad").pack()
entry_edad = tk.Entry(frame_estudiantes)
entry_edad.pack()

tk.Label(frame_estudiantes, text="Correo").pack()
entry_correo = tk.Entry(frame_estudiantes)
entry_correo.pack()

tk.Label(frame_estudiantes, text="Curso").pack()
entry_curso = tk.Entry(frame_estudiantes)
entry_curso.pack()

tk.Button(frame_estudiantes, text="Registrar", command=registrar_estudiante).pack(pady=10)

tk.Label(frame_estudiantes, text="Buscar Estudiante por ID").pack(pady=5)
entry_buscar = tk.Entry(frame_estudiantes)
entry_buscar.pack()
tk.Button(frame_estudiantes, text="Buscar", command=buscar_estudiante).pack(pady=5)

tk.Button(frame_estudiantes, text="← Volver al Menú", command=lambda: volver_al_menu()).pack(pady=5)
def volver_al_menu():
    notebook.pack_forget()
    frame_menu.pack(expand=True, fill='both')

# ==== Pestaña Profesores ====
frame_profesores = tk.Frame(notebook, bg="#0f4174")
notebook.add(frame_profesores, text='Profesores')
tk.Label(frame_profesores, text="Profesores", font=("Arial", 18, "bold"), bg="#f8f6f0", fg="#2c3e50").pack(pady=30)

# ==== Pestaña Cursos ====
frame_cursos = tk.Frame(notebook, bg="#0f4174")
notebook.add(frame_cursos, text='Cursos')
tk.Label(frame_cursos, text="Cursos", font=("Arial", 18, "bold"), bg="#f8f6f0", fg="#2c3e50").pack(pady=30)


def registrar_profesor():
    Id = entry_prof_id.get()
    nombre = entry_prof_nombre.get()
    especialidad = entry_prof_esp.get()

    if not Id or not nombre or not especialidad:
        messagebox.showerror("Error", "Todos los campos deben estar llenos.")
        return

    if Id in sistema.profesores_dict:
        messagebox.showwarning("Advertencia", "Ya existe un profesor con este ID.")
        return

    profesor = Profesor(Id, nombre, especialidad)
    sistema.registrar_profesor(profesor)
    sistema.guardar_todo_en_json("sistema.json")
    messagebox.showinfo("Éxito", f"Profesor {nombre} registrado correctamente.")
    entry_prof_id.delete(0, tk.END)
    entry_prof_nombre.delete(0, tk.END)
    entry_prof_esp.delete(0, tk.END)

tk.Label(frame_profesores, text="Registrar Profesor", font=("Arial", 12, "bold")).pack(pady=10)

tk.Label(frame_profesores, text="ID").pack()
entry_prof_id = tk.Entry(frame_profesores)
entry_prof_id.pack()

tk.Label(frame_profesores, text="Nombre").pack()
entry_prof_nombre = tk.Entry(frame_profesores)
entry_prof_nombre.pack()

tk.Label(frame_profesores, text="Especialidad").pack()
entry_prof_esp = tk.Entry(frame_profesores)
entry_prof_esp.pack()

tk.Button(frame_profesores, text="Registrar Profesor", command=registrar_profesor).pack(pady=10)

tk.Label(frame_cursos, text="Registrar Curso", font=("Arial", 12, "bold")).pack(pady=10)

# ID del curso
tk.Label(frame_cursos, text="ID del curso").pack()
entry_curso_id = tk.Entry(frame_cursos)
entry_curso_id.pack()

# Nombre del curso
tk.Label(frame_cursos, text="Nombre del curso").pack()
entry_curso_nombre = tk.Entry(frame_cursos)
entry_curso_nombre.pack()

# Profesor (menú desplegable)
tk.Label(frame_cursos, text="Seleccionar profesor").pack()
profesor_var = tk.StringVar()
combo_profesores = ttk.Combobox(frame_cursos, textvariable=profesor_var, state="readonly")
combo_profesores.pack()

# Estudiantes (lista con múltiples selección)
tk.Label(frame_cursos, text="Seleccionar estudiantes").pack()
lista_estudiantes = tk.Listbox(frame_cursos, selectmode="multiple", height=6)
lista_estudiantes.pack(fill="both", expand=True)

# Función para cargar datos actuales en los menús
def actualizar_listas():
    combo_profesores["values"] = [f"{p.Id} - {p.nombre}" for p in sistema.profesores_dict.values()]
    lista_estudiantes.delete(0, tk.END)
    for e in sistema.estudiantes_dict.values():
        lista_estudiantes.insert(tk.END, f"{e.Id} - {e.nombre}")

# Buscar profesor por ID
tk.Label(frame_profesores, text="Buscar Profesor por ID").pack(pady=5)
entry_buscar_prof = tk.Entry(frame_profesores)
entry_buscar_prof.pack()

def buscar_profesor():
    Id = entry_buscar_prof.get()
    profesor = sistema.buscar_profesor_por_id(Id)
    if profesor:
        messagebox.showinfo(
            "Profesor encontrado",
            f"ID: {profesor.Id}\nNombre: {profesor.nombre}\nEspecialidad: {profesor.especialidad}"
        )
    else:
        messagebox.showwarning("No encontrado", "No se encontró ningún profesor con ese ID.")

tk.Button(frame_profesores, text="Buscar", command=buscar_profesor).pack(pady=5)

tk.Button(frame_profesores, text="← Volver al Menú", command=lambda: volver_al_menu()).pack(pady=5)
def volver_al_menu():
    notebook.pack_forget()
    frame_menu.pack(expand=True, fill='both')

# Registrar curso
def registrar_curso():
    Id = entry_curso_id.get()
    nombre = entry_curso_nombre.get()

    if not Id or not nombre:
        messagebox.showerror("Error", "ID y nombre son obligatorios.")
        return

    if Id in sistema.cursos_dict:
        messagebox.showwarning("Advertencia", "Ya existe un curso con este ID.")
        return

    seleccion_prof = profesor_var.get()
    if not seleccion_prof:
        messagebox.showerror("Error", "Debe seleccionar un profesor.")
        return

    profesor_id = seleccion_prof.split(" - ")[0]
    profesor = sistema.profesores_dict.get(profesor_id)

    indices_est = lista_estudiantes.curselection()
    estudiantes = []
    for i in indices_est:
        est_id = lista_estudiantes.get(i).split(" - ")[0]
        est = sistema.estudiantes_dict.get(est_id)
        if est:
            estudiantes.append(est)

    curso = Curso(Id, nombre, profesor)
    curso.estudiantes = estudiantes

    sistema.registrar_curso(curso)
    sistema.guardar_todo_en_json("sistema.json")
    messagebox.showinfo("Éxito", f"Curso '{nombre}' registrado correctamente.")

    entry_curso_id.delete(0, tk.END)
    entry_curso_nombre.delete(0, tk.END)
    profesor_var.set("")
    lista_estudiantes.selection_clear(0, tk.END)

tk.Button(frame_cursos, text="Registrar Curso", command=registrar_curso).pack(pady=10)

# Actualiza listas cada vez que se cambia de pestaña
def al_cambiar_pestana(event):
    if notebook.index("current") == 2:  # Cursos
        actualizar_listas()

# Buscar curso por ID
tk.Label(frame_cursos, text="Buscar Curso por ID").pack(pady=5)
entry_buscar_curso = tk.Entry(frame_cursos)
entry_buscar_curso.pack()
tk.Button(frame_cursos, text="Buscar", command=lambda: buscar_curso()).pack(pady=5)

def buscar_curso():
    Id = entry_buscar_curso.get()
    curso = sistema.buscar_curso_por_id(Id)
    if curso:
        estudiantes = ', '.join(e.nombre for e in curso.estudiantes)
        messagebox.showinfo("Curso encontrado", f"ID: {curso.Id}\nNombre: {curso.nombre}\nProfesor: {curso.profesor.nombre}\nEstudiantes: {estudiantes}")
    else:
        messagebox.showwarning("No encontrado", "No se encontró ningún curso con ese ID.")

tk.Button(frame_cursos, text="← Volver al Menú", command=lambda: volver_al_menu()).pack(pady=5)
def volver_al_menu():
    notebook.pack_forget()
    frame_menu.pack(expand=True, fill='both')

notebook.bind("<<NotebookTabChanged>>", al_cambiar_pestana)

root.mainloop()
