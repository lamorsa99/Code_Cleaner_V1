import tkinter as tk
from tkinter import scrolledtext, messagebox
import re

class CodeCleanerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Cleaner V1")
        self.root.geometry("800x600")
        
        # Crear la interfaz
        self.create_widgets()
    
    def create_widgets(self):
        # Título
        title_label = tk.Label(self.root, text="Code Cleaner V1", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Frame para el texto de entrada
        input_frame = tk.Frame(self.root)
        input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Label para texto de entrada
        input_label = tk.Label(input_frame, text="Ingresa tu código aquí:", 
                              font=("Arial", 12))
        input_label.pack(anchor=tk.W)
        
        # Área de texto de entrada
        self.input_text = scrolledtext.ScrolledText(input_frame, 
                                                   height=10, 
                                                   font=("Courier", 10))
        self.input_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Botón Clean Code
        clean_button = tk.Button(self.root, text="Clean Code", 
                                command=self.clean_code,
                                bg="#4CAF50", fg="white", 
                                font=("Arial", 12, "bold"),
                                padx=20, pady=5)
        clean_button.pack(pady=10)
        
        # Frame para el texto de salida
        output_frame = tk.Frame(self.root)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Label para texto de salida
        output_label = tk.Label(output_frame, text="Código limpio:", 
                               font=("Arial", 12))
        output_label.pack(anchor=tk.W)
        
        # Área de texto de salida
        self.output_text = scrolledtext.ScrolledText(output_frame, 
                                                    height=10, 
                                                    font=("Courier", 10),
                                                    state=tk.DISABLED)
        self.output_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Botón para copiar resultado
        copy_button = tk.Button(self.root, text="Copiar Resultado", 
                               command=self.copy_result,
                               bg="#2196F3", fg="white", 
                               font=("Arial", 10),
                               padx=15, pady=3)
        copy_button.pack(pady=5)
    
    def clean_code(self):
        # Obtener el texto de entrada
        input_code = self.input_text.get("1.0", tk.END)
        
        if not input_code.strip():
            messagebox.showwarning("Advertencia", "Por favor ingresa algún código para limpiar.")
            return
        
        # Limpiar el código
        cleaned_code = self.remove_comments_and_spaces(input_code)
        
        # Mostrar el resultado
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", cleaned_code)
        self.output_text.config(state=tk.DISABLED)
    
    def remove_comments_and_spaces(self, code):
        # 1. Eliminar comentarios de línea que empiezan con //
        code = re.sub(r'//.*$', '', code, flags=re.MULTILINE)
        
        # 2. Eliminar comentarios de bloque /* */
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        
        # 3. Eliminar líneas vacías y espacios extra
        lines = code.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Eliminar espacios al inicio y final de cada línea
            line = line.strip()
            # Solo agregar líneas que no estén vacías
            if line:
                cleaned_lines.append(line)
        
        # 4. Unir las líneas con un solo salto de línea
        return '\n'.join(cleaned_lines)
    
    def copy_result(self):
        # Copiar el resultado al clipboard
        result = self.output_text.get("1.0", tk.END).strip()
        if result:
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            messagebox.showinfo("Éxito", "Código copiado al portapapeles!")
        else:
            messagebox.showwarning("Advertencia", "No hay código limpio para copiar.")

def main():
    root = tk.Tk()
    app = CodeCleanerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()    