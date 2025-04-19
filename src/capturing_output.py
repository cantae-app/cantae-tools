import io

class CapturingOutput(io.StringIO):
    def __init__(self, text_field):
        super().__init__()
        self.text_field = text_field
        self.current_progress = 0

    def write(self, s):
        if '#' in s:
            num_hashes = s.count('#')
            total_blocks = self.calculate_blocks(num_hashes)
   
            progress_bar = '🟩' * total_blocks + '⬜' * (10 - total_blocks)
            s = s.replace('#' * num_hashes, progress_bar)

            if '\r' in s:
                self.update_line(s)
            else:
                self.text_field.value += s

        else:
            self.text_field.value += s
        
        self.text_field.update()

    def calculate_blocks(self, num_hashes):
        total_blocks = int(num_hashes / 156 * 10)
        return min(total_blocks, 10)

    def update_line(self, progress_bar):
        lines = self.text_field.value.split('\n')
        if lines:
            lines[-1] = progress_bar.strip()
        self.text_field.value = '\n'.join(lines)