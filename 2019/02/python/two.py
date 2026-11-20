def run_logic(data):
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

        NOUN = data[1]
        VERB = data[2]

        cursor += 4

    return data[0]

def find_solution(memory):
    target = 19690720

    for noun in range(0, 100):
        for verb in range(0, 100):
            data = memory[::]

            data[1] = noun
            data[2] = verb

            result = run_logic(data)

            if result == target:
                return 100 * noun + verb

def run_part_two(memory):
    solution = find_solution(memory)

    print('P2:', solution)
