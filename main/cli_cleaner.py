#!/usr/bin/env python3
"""
Code Cleaner V1 - Versión CLI
Limpia código eliminando comentarios y espacios extra
"""
import re
import sys
import os

class CodeCleanerCLI:
    def __init__(self):
        self.version = "1.0"
    
    def display_header(self):
        """Muestra el encabezado de la aplicación"""
        print("=" * 50)
        print("       CODE CLEANER V1 - CLI Version")
        print("=" * 50)
        print("Elimina comentarios (//, /* */) y espacios extra")
        print("-" * 50)
    
    def remove_comments_and_spaces(self, code):
        """Elimina comentarios y espacios del código"""
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
    
    def clean_from_input(self):
        """Modo interactivo: el usuario ingresa código línea por línea"""
        print("\n📝 MODO INTERACTIVO")
        print("Ingresa tu código (presiona Enter dos veces para terminar):")
        print("-" * 30)
        
        lines = []
        empty_lines = 0
        
        while True:
            try:
                line = input()
                if line == "":
                    empty_lines += 1
                    if empty_lines >= 2:  # Dos enters seguidos para terminar
                        break
                else:
                    empty_lines = 0
                    lines.append(line)
            except KeyboardInterrupt:
                print("\n\n❌ Operación cancelada.")
                return
        
        if not lines:
            print("❌ No se ingresó código para limpiar.")
            return
        
        input_code = '\n'.join(lines)
        cleaned_code = self.remove_comments_and_spaces(input_code)
        
        print("\n" + "=" * 50)
        print("✅ CÓDIGO LIMPIO:")
        print("=" * 50)
        print(cleaned_code)
        print("=" * 50)
        
        # Ofrecer guardar el resultado
        save = input("\n💾 ¿Guardar resultado en archivo? (s/n): ").lower()
        if save in ['s', 'si', 'y', 'yes']:
            self.save_to_file(cleaned_code)
    
    def clean_from_file(self, file_path):
        """Limpia código desde un archivo"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                input_code = file.read()
            
            print(f"\n📂 Procesando archivo: {file_path}")
            cleaned_code = self.remove_comments_and_spaces(input_code)
            
            print("\n" + "=" * 50)
            print("✅ CÓDIGO LIMPIO:")
            print("=" * 50)
            print(cleaned_code)
            print("=" * 50)
            
            # Guardar automáticamente con sufijo _clean
            base_name = os.path.splitext(file_path)[0]
            extension = os.path.splitext(file_path)[1]
            output_path = f"{base_name}_clean{extension}"
            
            with open(output_path, 'w', encoding='utf-8') as output_file:
                output_file.write(cleaned_code)
            
            print(f"💾 Resultado guardado en: {output_path}")
            
        except FileNotFoundError:
            print(f"❌ Error: No se encontró el archivo '{file_path}'")
        except Exception as e:
            print(f"❌ Error al procesar el archivo: {e}")
    
    def save_to_file(self, content):
        """Guarda el contenido en un archivo"""
        filename = input("Nombre del archivo (ej: codigo_limpio.txt): ").strip()
        if not filename:
            filename = "codigo_limpio.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"✅ Archivo guardado como: {filename}")
        except Exception as e:
            print(f"❌ Error al guardar: {e}")
    
    def show_help(self):
        """Muestra la ayuda del programa"""
        print("\n📚 AYUDA - CODE CLEANER V1")
        print("-" * 30)
        print("Uso:")
        print("  python cli_cleaner.py                    # Modo interactivo")
        print("  python cli_cleaner.py <archivo>          # Limpiar archivo")
        print("  python cli_cleaner.py -h/--help          # Mostrar ayuda")
        print("\nFunciones:")
        print("  • Elimina comentarios // y /* */")
        print("  • Remueve líneas vacías")
        print("  • Elimina espacios extra")
        print("\nEjemplo de código de entrada:")
        print("  // Este es un comentario")
        print("  function ejemplo() {")
        print("      /* comentario de bloque */")
        print("      console.log('Hola mundo');")
        print("  }")
        print("\nResultado:")
        print("  function ejemplo() {")
        print("      console.log('Hola mundo');")
        print("  }")
    
    def run(self):
        """Función principal"""
        self.display_header()
        
        # Verificar argumentos de línea de comandos
        if len(sys.argv) > 1:
            arg = sys.argv[1]
            if arg in ['-h', '--help']:
                self.show_help()
            else:
                # Tratar como archivo
                self.clean_from_file(arg)
        else:
            # Modo interactivo
            self.clean_from_input()

def main():
    cleaner = CodeCleanerCLI()
    cleaner.run()

if __name__ == "__main__":
    main()
