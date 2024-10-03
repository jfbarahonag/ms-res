from contextlib import suppress
import base64
import os

class AttachmentsService:
    @staticmethod
    def b64_to_file(b64_string: str, file_name: str, output_dir: str = "./"):
        # Decodificar la cadena base64
        file_data = base64.b64decode(b64_string)

        # Crear el directorio si no existe
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Construir la ruta completa del archivo
        file_path = os.path.join(output_dir, file_name)

        # Guardar el archivo en el sistema de archivos
        with open(file_path, "wb") as file:
            file.write(file_data)
            file.close()

        return file_path
    
    @staticmethod
    def filepaths_to_multipart(file_paths: list[str]):
        files = []
        files_opened = []
        for file_path in file_paths:
            file_opened = open(file_path, "rb")
            files_opened.append(file_opened)
            files.append(
                ('files', (os.path.basename(file_path), file_opened))
            )
        
        return files, files_opened
    
    @staticmethod
    def close_open_files(file_objects: list):
        for file in file_objects:
            with suppress(Exception):  # Suprimir cualquier excepción que ocurra al intentar cerrar un archivo
                if not file.closed:
                    file.close()
                    print(f"Archivo {file.name} cerrado correctamente.")
    
    @staticmethod
    def delete_files(file_paths:list[str]):
        for file_path in file_paths:
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    print(f"Archivo eliminado: {file_path}")
                except Exception as delete_error:
                    print(f"Error al eliminar el archivo {file_path} por: {str(delete_error)}")
