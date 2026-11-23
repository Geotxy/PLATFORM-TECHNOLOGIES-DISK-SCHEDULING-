def fcfs(requests, head):
    sequence = [head] + requests
    movement = sum(abs(sequence[i] - sequence[i - 1])
                    for i in range(1, len(sequence)))
    return sequence, movement


def sstf(requests, head):
    remaining = requests.copy()
    sequence = [head]
    movement = 0

    while remaining:
        nearest = min(remaining, key=lambda request: abs(request - head))
        movement += abs(nearest - head)
        head = nearest
        sequence.append(head)
        remaining.remove(nearest)

    return sequence, movement


def scan(requests, head, disk_size, direction="right"):
    sequence = [head]
    movement = 0

    if direction == "right":
        right = sorted(request for request in requests if request >= head)
        left = sorted((request for request in requests if request < head),
                      reverse=True)
        order = right
        if head < disk_size - 1 and disk_size - 1 not in order:
            order = order + [disk_size - 1]
        order = order + left
    else:
        left = sorted((request for request in requests if request <= head),
                      reverse=True)
        right = sorted(request for request in requests if request > head)
        order = left
        if head > 0 and 0 not in order:
            order = order + [0]
        order = order + sorted(request for request in requests
                               if request > head)

    for cylinder in order:
        if cylinder != sequence[-1]:
            movement += abs(cylinder - sequence[-1])
            sequence.append(cylinder)

    return sequence, movement


def read_requests():
    while True:
        try:
            text = input("Enter requests (example: 98, 183, 37): ")
            requests = [int(value.strip()) for value in text.split(",")]
            if requests:
                return requests
        except ValueError:
            pass
        print("Please enter whole numbers separated by commas.")


def read_number(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a whole number.")


def main():
    head = read_number("Enter initial head position: ")
    requests = read_requests()
    disk_size = read_number("Enter disk size: ")

    print("\n1. FCFS")
    print("2. SSTF")
    print("3. SCAN")
    choice = input("Choose an algorithm: ").strip()

    if choice == "1":
        sequence, movement = fcfs(requests, head)
        name = "FCFS"
    elif choice == "2":
        sequence, movement = sstf(requests, head)
        name = "SSTF"
    else:
        direction = input("Direction (left/right): ").strip().lower()
        if direction not in ("left", "right"):
            direction = "right"
        sequence, movement = scan(requests, head, disk_size, direction)
        name = "SCAN"

    print(f"\n{name}")
    print("Sequence:", " -> ".join(map(str, sequence)))
    print("Total cylinder:", movement)


if __name__ == "__main__":
    main()