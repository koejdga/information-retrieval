# У музеї упродовж дня відбувається реєстрація приходу та виходу кожного відвідувача.
# Таким чином, за день отримані n пар значень,
# де перше значення в парі показує час приходу відвідувача та друге значення - час його виходу.
# Знайти проміжок часу, упродовж якого в музеї одночасно перебувало максимальне число відвідувачів.

inputt = [(7, 8), (7.5, 13)]
input = [(7, 1), (8, -1), (8, 1), (10, 1), (11.45, -1), (13.18, -1)]

start_time = 0
vis = 0
max = 0
intervals = []

for pair in input:
    if pair[1] == -1:
        if max < vis:
            max = vis
            intervals.clear()
        if max <= vis:
            intervals.append((start_time, pair[0]))

        vis -= 1
        start_time = 0

    else:
        start_time = pair[0]
        vis += 1

print(max)
print(intervals)