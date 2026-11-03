class Solution:
    def fullJustify(self, words: list[str], maxWidth: int) -> list[str]:
        lines = []

        current_line_size = 0
        current_line = []
        for word in words:
            word_size = len(word)
            spaces = len(current_line) - 1
            if current_line_size + word_size + spaces + 1 > maxWidth:
                lines.append([current_line_size, current_line])
                current_line = [word]
                current_line_size = word_size
            else:
                current_line.append(word)
                current_line_size += word_size

        if current_line not in lines:
            lines.append([current_line_size, current_line])

        total_lines = len(lines)
        for idx in range(total_lines):
            line_size, line = lines[idx]
            words_in_line = len(line)
            if idx == total_lines - 1 or words_in_line == 1:
                curr_line = " ".join(line)
                curr_size = len(curr_line)
                lines[idx] = curr_line + (" " * (maxWidth - curr_size))
                continue

            total_spaces_left = maxWidth - line_size
            div, mod = divmod(total_spaces_left, words_in_line-1)

            curr_line = line[0]
            for word in line[1:]:
                curr_line += (" " * (div + (1 if mod > 0 else 0))) + word
                mod -= 1

            lines[idx] = curr_line

        return lines

    def fullJustify(self, words: list[str], maxWidth: int) -> list[str]:

            res, line, width = [], [], 0

            for w in words:
                if width + len(w) + len(line) > maxWidth:
                    for i in range(maxWidth - width):
                        line[i % (len(line) - 1 or 1)] += ' '

                    res, line, width = res + [''.join(line)], [], 0
                line += [w]
                width += len(w)

            return res + [' '.join(line).ljust(maxWidth)]
