

class Snake():
    def __init__(self, head_pos, body):
        self.head_pos = head_pos
        self.body = body
        self.direction = 'RIGHT'
        self.eaten = False

    def move_snake(self, direction):


        if direction == 'UP':
            self.head_pos[1] -= 10
        if direction == 'DOWN':
            self.head_pos[1] += 10
        if direction == 'LEFT':
            self.head_pos[0] -= 10
        if direction == 'RIGHT':
            self.head_pos[0] += 10

        self.direction = direction

    def check_grow(self, food_pos):

        self.body.insert(0, list(self.head_pos))
        if self.head_pos[0] == food_pos[0] and self.head_pos[1] == food_pos[1]:
            self.eaten = True
        else:
            self.body.pop()

    def return_lines(self):

        lines = []
        prev_pos = self.body[0]
        prev2 = (0,0)
        lines.append(prev_pos)
        for pos in self.body[1:]:
            if pos[0] == prev_pos[0] or pos[1] == prev_pos[1]:
                prev2 = pos
                continue

            lines.append(prev2)
            prev_pos = pos

        lines.append(self.body[-1])

        return lines
