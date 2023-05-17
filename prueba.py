import random
uso = 30
estado = 0
def usoCPU():
    global uso
    global estado
    if estado == 0:
        delta = random.random()
        print(f'DELTA1 --> {delta}')
        if delta <= 0.5:
            uso -= 1
        else:
            uso +=1
        
        delta2 = random.random()
        print(f'DELTA2 --> {delta2}')
        if delta2 >= 0.8 and delta2<=0.85:
            estado = 2
        elif delta2 >0.85 and delta2<=0.9:
            estado = 1
        else: 
            estado = 0
    elif estado == 1 and uso <100:
        print(uso)
        uso +=1
    elif estado == 2 and uso > 0:
        print(uso)
        uso -= 1
    
    return uso

