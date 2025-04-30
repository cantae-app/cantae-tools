import io

import io
import re

class CapturingOutput(io.StringIO):
    MAX_LINES = 1000  # Limite de linhas visíveis no text_field

    def __init__(self, text_field):
        super().__init__()
        self.text_field = text_field
        self.buffer = ""

    def write(self, s):
        self.buffer += s
        if '\n' in s or '\r' in s:
            self.flush()

    def flush(self):
        # Extrai o valor percentual
        percent_match = re.search(r"(\d+)%", self.buffer)
        if percent_match:
            percent = int(percent_match.group(1))
            total_blocks = self.calculate_blocks(percent)
            progress_bar = '🟩' * total_blocks + '⬜' * (10 - total_blocks)
            
            # Substitui só a barra visual de progresso, mantém o restante da linha
            self.buffer = re.sub(r"\d+%\|[^\|]+\|", f"{percent}%|{progress_bar}|", self.buffer)

        if '\r' in self.buffer:
            self.update_line(self.buffer)
        else:
            self.text_field.value += self.buffer

        self.truncate_text()
        self.text_field.update()
        self.buffer = ""

    def calculate_blocks(self, percent):
        # Converte percentagem (0-100) para blocos (0-10)
        return min(max(int(percent / 10), 0), 10)

    def update_line(self, new_line):
        lines = self.text_field.value.split('\n')
        if lines:
            lines[-1] = new_line.strip()
        self.text_field.value = '\n'.join(lines)

    def truncate_text(self):
        lines = self.text_field.value.split('\n')
        if len(lines) > self.MAX_LINES:
            self.text_field.value = '\n'.join(lines[-self.MAX_LINES:])
