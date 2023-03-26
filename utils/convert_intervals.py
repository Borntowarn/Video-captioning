def convert_intervals(file_intervals):
    lines = []
    with open(file_intervals) as file:
        for line in file:
            values = line.split()
            val0 = float(values[0])
            val1 = float(values[1])
            line = [val0, val1]
            lines.append(line)
    return lines