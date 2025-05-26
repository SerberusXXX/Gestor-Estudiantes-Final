import json
import os
class Persona:
    def __init__(self, Id, nombre):
        self.Id = Id
        self.nombre = nombre
# Definición de la clase Estudiantes
class Estudiante(Persona):
    def __init__(self, Id, nombre, edad, correo, Curso=None):
        super().__init__(Id, nombre)
        self.edad = edad
        self.correo = correo
        self.Curso = Curso
    
    def to_dict(self):
        return {
            "Id": self.Id,
            "nombre": self.nombre,
            "edad": self.edad,
            "correo": self.correo,
            "Curso": self.Curso,
        }

    def from_dict(data):
        return Estudiante(
            data["Id"],
            data["nombre"],
            data["edad"], 
            data["correo"],
            data.get("Curso"),
        )
    
    def mostrar_info(self):
        return f"Estudiante: {self.nombre}, Edad{self.edad}, Correo{self.correo} Curso: {self.Curso}"

# Definición de la clases en profesores
class Profesor(Persona):
    def __init__(self, Id, nombre, especialidad):
        super().__init__(Id, nombre)
        self.especialidad = especialidad

    def to_dict(self):
        return {
            "Id": self.Id,
            "nombre": self.nombre,
            "especialidad": self.especialidad
        }
    
    @staticmethod
    def from_dict(data):
        return Profesor(
            data["Id"],
            data["nombre"],
            data["especialidad"]
        )
    def mostrar_info(self):
        return f"Profesor: {self.nombre}, Especialidad: {self.especialidad}"

# Definicion de los Cursos. 
class Curso:
    def __init__(self, Id, nombre, profesor=None):
        self.Id = Id
        self.nombre = nombre
        self.profesor = profesor #lista de objetos de profesores
        self.estudiantes = [] # lista de objetos Estudiante
   

    def to_dict(self):
        return {
            "Id": self.Id,
            "nombre": self.nombre,
            "profesor": self.profesor.Id if self.profesor else None,
            "estudiantes": [e.Id for e in self.estudiantes]
        }

    @staticmethod
    def from_dict(data, profesores_dict, estudiantes_dict):
        curso = Curso(data["Id"], data["nombre"])
        if data["profesor"]:
            curso.profesor = profesores_dict.get(data["profesor"])
        curso.estudiantes = [estudiantes_dict[eid] for eid in data["estudiantes"] if eid in estudiantes_dict]
        return curso
        
    def mostrar_info(self):
        profesor_nombre = self.profesor.nombre if self.profesor else "No asignado"
        if self.estudiantes:
            estudiantes_nombres = ", ".join([e.nombre for e in self.estudiantes])
        else:
            estudiantes_nombres = "Sin estudiantes asignados"
        return f"ID: {self.Id}, Curso: {self.nombre}, Profesor: {profesor_nombre}, Estudiantes: {estudiantes_nombres}"

# Definicion del sistema escolar
class SistemaEscolar:
    def __init__(self):
        self.estudiantes_dict = {}
        self.profesores_dict = {}
        self.cursos_dict = {}

    def registrar_estudiante(self, estudiante):
        self.estudiantes_dict[estudiante.Id] = estudiante

    def registrar_profesor(self, profesor):
        self.profesores_dict[profesor.Id] = profesor

    def registrar_curso(self, curso):
        self.cursos_dict[curso.Id] = curso

    def buscar_estudiante_por_id(self, est_id):
        return self.estudiantes_dict.get(est_id)

    def buscar_estudiante_por_id(self, est_id):
        return self.estudiantes_dict.get(est_id)

    def buscar_profesor_por_id(self, prof_id):
        return self.profesores_dict.get(prof_id)

    def buscar_curso_por_id(self, cur_id):
        return self.cursos_dict.get(cur_id)

    def guardar_todo_en_json(self, archivo):
        datos_existentes = {
            "estudiantes": [],
            "profesores": [],
            "cursos": []
        }

        if os.path.exists(archivo):
            with open(archivo, "r") as f:
                try:
                    datos_existentes = json.load(f)
                except json.JSONDecodeError:
                    print("Archivo JSON corrupto o vacío. Se sobrescribirá.")

        # Convertir listas existentes a diccionarios por ID
        est_dict = {e["Id"]: e for e in datos_existentes.get("estudiantes", []) if "Id" in e}
        prof_dict = {p["Id"]: p for p in datos_existentes.get("profesores", []) if "Id" in p}
        curs_dict = {c["Id"]: c for c in datos_existentes.get("cursos", []) if "Id" in c}

        # Agregar nuevos objetos
        for est in self.estudiantes_dict.values():
            est_data = est.to_dict()
            if "Id" in est_data and "nombre" in est_data:
                est_dict[est.Id] = est_data
            else:
                print(f"Estudiante inválido: {est_data}")

        for prof in self.profesores_dict.values():
            prof_data = prof.to_dict()
            if "Id" in prof_data and "nombre" in prof_data:
                prof_dict[prof.Id] = prof_data
            else:
                print(f"Profesor inválido: {prof_data}")

        for curs in self.cursos_dict.values():
            curs_data = curs.to_dict()
            if "Id" in curs_data and "nombre" in curs_data:
                curs_dict[curs.Id] = curs_data
            else:
                print(f"Curso inválido: {curs_data}")

        # Datos finales a guardar
        datos_finales = {
            "estudiantes": list(est_dict.values()),
            "profesores": list(prof_dict.values()),
            "cursos": list(curs_dict.values())
        }

        # Guardar el archivo
        try:
            with open(archivo, "w") as f:
                json.dump(datos_finales, f, indent=4)
            print("Datos guardados exitosamente.")

            # Verificación rápida: reabrimos el archivo
            with open(archivo, "r") as f:
                json.load(f)
            print("Verificación posterior: JSON válido.")

        except Exception as e:
            print(f"Error al guardar/verificar el archivo: {e}")


    def cargar_todo_desde_json(self, archivo):
        if not os.path.exists(archivo):
            print(f"Archivo '{archivo}' no encontrado.")
            return

        try:
            with open(archivo, "r") as f:
                datos = json.load(f)
        except json.JSONDecodeError:
            print("Error: El archivo JSON está corrupto o mal formado.")
            return
        except Exception as e:
            print(f"Error inesperado al abrir el archivo: {e}")
            return

        # Validar estructura general
        if not all(clave in datos for clave in ["estudiantes", "profesores", "cursos"]):
            print("Estructura del archivo inválida. Faltan claves principales.")
            return

        # Limpiar los diccionarios actuales
        self.estudiantes_dict.clear()
        self.profesores_dict.clear()
        self.cursos_dict.clear()

        # Cargar estudiantes
        for d in datos["estudiantes"]:
            if isinstance(d, dict) and "Id" in d and "nombre" in d:
                estudiante = Estudiante.from_dict(d)
                self.estudiantes_dict[estudiante.Id] = estudiante
            else:
                print(f"Estudiante con formato inválido ignorado: {d}")

        # Cargar profesores
        for d in datos["profesores"]:
            if isinstance(d, dict) and "Id" in d and "nombre" in d:
                profesor = Profesor.from_dict(d)
                self.profesores_dict[profesor.Id] = profesor
            else:
                print(f"Profesor con formato inválido ignorado: {d}")

        # Cargar cursos (dependen de los anteriores)
        for c in datos["cursos"]:
            if isinstance(c, dict) and "Id" in c and "nombre" in c:
                curso = Curso.from_dict(c, self.profesores_dict, self.estudiantes_dict)
                self.cursos_dict[curso.Id] = curso
            else:
                print(f"Curso con formato inválido ignorado: {c}")

        print("Datos cargados correctamente y verificados.")

def pedir_entero(prompt, min_val=None, max_val=None):
        while True:
            entrada = input(prompt)
            if not entrada.isdigit():
                print("Error: Por favor, ingrese un número entero válido.")
                continue
            valor = int(entrada)
            if min_val is not None and valor < min_val:
                print(f"Error: El número debe ser mayor o igual a {min_val}.")
                continue
            if max_val is not None and valor > max_val:
                print(f"Error: El número debe ser menor o igual a {max_val}.")
                continue
            return valor

def pedir_cadena_no_vacia(prompt):
        while True:
            texto = input(prompt).strip()
            if texto == "":
                print("Error: Este campo no puede estar vacío.")
                continue
            return texto

def validar_correo(correo):
        if "@" in correo and "." in correo.split("@")[-1]:
            return True
        return False

def pedir_correo(prompt):
        while True:
            correo = input(prompt).strip()
            if validar_correo(correo):
                return correo
            print("Error: Por favor ingrese un correo válido.")  

#Interaccion del menu
def menu ():
    sistema = SistemaEscolar()
    # Cargar datos automáticamente si el archivo existe
    if os.path.exists("sistema.json"):
        try:
            sistema.cargar_todo_desde_json("sistema.json")
            print("Datos cargados desde sistema.json.")
        except Exception as e:
            print(f"Error al cargar los datos: {e}")

    while True:
        print("\n=== Menú del Sistema Escolar ===")
        print("1. Registrar estudiante")
        print("2. Registrar profesor")
        print("3. Registrar curso")
        print("4. Buscar estudiante por ID")
        print("5. Buscar profesor por ID")
        print("6. Buscar curso por ID")
        print("7. Guardar datos")
        print("8. mostrar toda la informacion")
        print("9. Cargar datos")
        print("10. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":  # Registrar estudiante
            Id = pedir_cadena_no_vacia("ID del estudiante: ")
            if Id in sistema.estudiantes_dict:
                print(f"Ya existe un estudiante con ID '{Id}'. Registro cancelado.")
                continue
            nombre = pedir_cadena_no_vacia("Nombre: ")
            edad = pedir_entero("Edad: ", 1, 120)
            correo = pedir_correo("Correo: ")
            curso = pedir_cadena_no_vacia("Curso: ")
            estudiante = Estudiante(Id, nombre, edad, correo, curso)
            sistema.registrar_estudiante(estudiante)
            print("Estudiante registrado.")

        elif opcion == "2":  # Registrar profesor
            Id = pedir_cadena_no_vacia("ID del profesor: ")
            if Id in sistema.profesores_dict:
                print(f"Ya existe un profesor con ID '{Id}'. Registro cancelado.")
                continue
            nombre = pedir_cadena_no_vacia("Nombre: ")
            especialidad = pedir_cadena_no_vacia("Especialidad: ")
            profesor = Profesor(Id, nombre, especialidad)
            sistema.registrar_profesor(profesor)
            print("Profesor registrado.")

        elif opcion == "3":  # Registrar curso
            Id = pedir_cadena_no_vacia("ID del curso: ")
            if Id in sistema.cursos_dict:
                print(f"Ya existe un curso con ID '{Id}'. Registro cancelado.")
                continue
            nombre = pedir_cadena_no_vacia("Nombre del curso: ")
            profesores = list(sistema.profesores_dict.values())
            if not profesores:
                print("No hay profesores registrados. Registre primero un profesor.")
                continue
            print("Profesores disponibles:")
            for i, p in enumerate(profesores):
                print(f"{i + 1}. {p.nombre} ({p.especialidad})")
            opcion_prof = pedir_entero("Seleccione un profesor por número: ", 1, len(profesores)) - 1
            profesor = profesores[opcion_prof]

            curso = Curso(Id, nombre, profesor)
            estudiantes = list(sistema.estudiantes_dict.values())
            if estudiantes:
                print("Estudiantes disponibles:")
                for i, e in enumerate(estudiantes):
                    print(f"{i + 1}. {e.nombre} ({e.Curso})")
                selecciones = input("Seleccione estudiantes (números separados por coma): ").split(",")
                for sel in selecciones:
                    sel = sel.strip()
                    if sel.isdigit():
                        idx = int(sel) - 1
                        if 0 <= idx < len(estudiantes):
                            curso.estudiantes.append(estudiantes[idx])
            else:
                print("No hay estudiantes registrados para asignar al curso.")

            sistema.registrar_curso(curso)
            print("Curso creado.")

        elif opcion == "4":
            if os.path.exists("sistema.json"):
                sistema.cargar_todo_desde_json("sistema.json")
            est_id = input("Ingrese el ID del estudiante: ").strip()
            estudiante = sistema.buscar_estudiante_por_id(est_id)
            if estudiante:
                print("Estudiante encontrado:")
                print(estudiante.mostrar_info())
            else:
                print(f"No se encontró ningún estudiante con ID '{est_id}'. Verifique el ID e intente nuevamente.")


        elif opcion == "5":
            if os.path.exists("sistema.json"):
                sistema.cargar_todo_desde_json("sistema.json")
            prof_id = input("Ingrese el ID del profesor: ").strip()
            profesor = sistema.buscar_profesor_por_id(prof_id)
            if profesor:
                print("Profesor encontrado:")
                print(profesor.mostrar_info())
            else:
                print(f"No se encontró ningún profesor con ID '{prof_id}'. Asegúrese de que está registrado.")

        elif opcion == "6":
            if os.path.exists("sistema.json"):
                sistema.cargar_todo_desde_json("sistema.json")
            curso_id = input("Ingrese el ID del curso: ")
            curso = sistema.buscar_curso_por_id(curso_id)
            if curso:
                print(curso.mostrar_info())
            else:
                print("Curso no encontrado.")


        elif opcion == "7":
            sistema.guardar_todo_en_json("sistema.json")
            print("Datos guardados en sistema.json.")

        elif opcion == "8":
            try:
                with open("sistema.json", "r") as archivo:
                    datos = json.load(archivo)
                print("\nContenido del archivo sistema.json:")
                print(json.dumps(datos, indent=4))
            except FileNotFoundError:
                print("El archivo sistema.json no existe. Guarda datos primero (opción 7).")
        
        elif opcion == "9":
            try:
                sistema.cargar_todo_desde_json("sistema.json")
                print("Datos cargados correctamente desde sistema.json.")
            except FileNotFoundError:
                print("El archivo sistema.json no existe. Guarda datos primero (opción 7).")

        elif opcion == "10":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción inválida. Intente de nuevo.")

# Ejecutar menú
if __name__ == "__main__":
    menu()