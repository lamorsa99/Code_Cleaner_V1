import tkinter as tk
from tkinter import messagebox
import re

class CodeCleanerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Cleaner V1")
        self.root.geometry("800x600")
        self.create_widgets()
    
    def create_widgets(self):
        # Título
        title_label = tk.Label(self.root, text="Code Cleaner V1", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Frame para el texto de entrada
        input_frame = tk.Frame(self.root)
        input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Label para texto de entrada
        input_label = tk.Label(input_frame, text="Ingresa tu código aquí:", font=("Arial", 12))
        input_label.pack(anchor=tk.W)
        
        # Subframe para números de línea y área de texto
        code_frame = tk.Frame(input_frame)
        code_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar vertical compartido
        v_scroll = tk.Scrollbar(code_frame, orient=tk.VERTICAL)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Widget para números de línea
        self.line_numbers = tk.Text(
            code_frame, width=4, padx=4, takefocus=0, border=0,
            background="#f0f0f0", state=tk.DISABLED, font=("Courier", 10),
            yscrollcommand=v_scroll.set
        )
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        # Área de texto de entrada
        self.input_text = tk.Text(
            code_frame, height=10, font=("Courier", 10),
            yscrollcommand=v_scroll.set
        )
        self.input_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=5)
        
        v_scroll.config(command=self._on_scroll)
        
        # Vincular eventos para actualizar los números de línea
        self.input_text.bind("<KeyRelease>", self.update_line_numbers)
        self.input_text.bind("<MouseWheel>", self.update_line_numbers)
        self.input_text.bind("<Button-1>", self.update_line_numbers)
        self.input_text.bind("<Return>", self.update_line_numbers)
        self.input_text.bind("<Configure>", self.update_line_numbers)
        self.update_line_numbers()
        
        # Botón Clean Code
        clean_button = tk.Button(
            self.root, text="Clean Code", command=self.clean_code,
            bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
            padx=20, pady=5
        )
        clean_button.pack(pady=10)
        
        # Frame para el texto de salida
        output_frame = tk.Frame(self.root)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Label para texto de salida
        output_label = tk.Label(output_frame, text="Código limpio:", font=("Arial", 12))
        output_label.pack(anchor=tk.W)
        
        # Área de texto de salida
        self.output_text = tk.Text(
            output_frame, height=10, font=("Courier", 10), state=tk.DISABLED
        )
        self.output_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Botón para copiar resultado
        copy_button = tk.Button(
            self.root, text="Copiar Resultado", command=self.copy_result,
            bg="#2196F3", fg="white", font=("Arial", 10),
            padx=15, pady=3
        )
        copy_button.pack(pady=5)
    
    def update_line_numbers(self, event=None):
        self.line_numbers.config(state=tk.NORMAL)
        self.line_numbers.delete("1.0", tk.END)
        line_count = int(self.input_text.index('end-1c').split('.')[0])
        line_numbers_string = "\n".join(str(i) for i in range(1, line_count + 1))
        self.line_numbers.insert("1.0", line_numbers_string)
        self.line_numbers.config(state=tk.DISABLED)
        # Sincroniza el scroll de los números de línea con el área de texto
        self.line_numbers.yview_moveto(self.input_text.yview()[0])
    
    def _on_scroll(self, *args):
        self.input_text.yview(*args)
        self.line_numbers.yview(*args)
    
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
            line = line.strip()
            if line:
                cleaned_lines.append(line)
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