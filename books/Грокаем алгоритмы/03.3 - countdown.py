def countdown(i: int):
    print(i)
    if i <= 1:
        return
    else:
        countdown(i-1)

i = 5
countdown(i)
