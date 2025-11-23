with open("reproduce_output.txt", "r") as f:
    lines = f.readlines()
    print("".join(lines[-50:]))
