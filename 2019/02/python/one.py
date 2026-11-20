def run_part_one(data):
    HALT = 99
    ADD = 1
    MULTIPLY = 2

    cursor = 0

    while cursor < len(data) and data[cursor] != HALT:
        a_idx = data[cursor + 1]
        b_idx = data[cursor + 2]
        o_idx = data[cursor + 3]

        if data[cursor] == ADD:
            data[o_idx] = data[a_idx] + data[b_idx]
        elif data[cursor] == MULTIPLY:
            data[o_idx] = data[a_idx] * data[b_idx]

        cursor += 4

    print('P1:', data[0])