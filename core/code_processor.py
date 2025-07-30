import re

class CodeProcessor:
    """Maneja la lógica de limpieza y procesamiento de código"""
    
    @staticmethod
    def clean_code(code):
        """Limpia el código removiendo comentarios y líneas vacías"""
        orig_lines = code.split('\n')
        cleaned_lines = []
        line_mapping = []

        for idx, line in enumerate(orig_lines):
            line_sin_comentario = re.sub(r'//.*$', '', line)
            line_sin_comentario = re.sub(r'/\*.*?\*/', '', line_sin_comentario)
            if line_sin_comentario.strip():
                cleaned_lines.append(line_sin_comentario.strip())
                line_mapping.append(idx)

        return '\n'.join(cleaned_lines), line_mapping

    @staticmethod
    def is_real_code(line):
        """Verifica si una línea contiene código real"""
        line = line.strip()
        if not line:
            return False
        if line.startswith("//"):
            return False
        if line.startswith("/*") and line.endswith("*/"):
            return False
        return True

    @staticmethod
    def count_errors_in_cleaned_code(orig_lines, clean_lines, highlighted_lines, highlighted_output_lines):
        """Cuenta los errores encontrados en el código limpio"""
        errores_editor = 0
        matched_output_lines = set()
        
        for i in highlighted_lines:
            if 0 <= i < len(orig_lines) and CodeProcessor.is_real_code(orig_lines[i]):
                content = orig_lines[i].strip()
                if content == "}":
                    if i-1 in highlighted_lines and i-1 >= 0:
                        prev_content = orig_lines[i-1].strip()
                        for idx in range(1, len(clean_lines)):
                            if clean_lines[idx].strip() == "}" and clean_lines[idx-1].strip() == prev_content:
                                if idx in highlighted_output_lines and idx not in matched_output_lines:
                                    errores_editor += 1
                                    matched_output_lines.add(idx)
                                    break
                else:
                    for idx, line in enumerate(clean_lines):
                        if line.strip() == content and idx in highlighted_output_lines and idx not in matched_output_lines:
                            errores_editor += 1
                            matched_output_lines.add(idx)
                            break

        return errores_editor