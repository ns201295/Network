def flatten(x):
    for i in x:
        if isinstance(i,list):
            for j in flatten(i):
                yield j
        else: yield i
        