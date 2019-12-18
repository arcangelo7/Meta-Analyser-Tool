from collections import deque
#converte ogni elemento in una stack
def stack_from_list(input_list):
    output_stack = deque()
    for item in input_list:
        output_stack.append(item)

    return output_stack

def my_enumerate(input_list):
#creare una funzione che a partire da una lista ritorna una lista con la posizione)
    output_list = []
    for i in range(len(input_list)):
        #per ogni posizione nel range (0,n-1) dato dalla lunghezza della lista stessa:
        output_list.append((i, input_list[i]))
        #aggiungere alla lista di output la posizione ogni volta presa in considerazione e l'oggetto nella relativa posizione specifica;
    return output_list

print(my_enumerate([1, 2, 3, 4])==list(enumerate([1, 2, 3, 4])))
#considero il risultato == enumerate(list)

def my_range(num):
    output_list = []
    n = 0
    while n < num:
        output_list.append(n)
        n = n+1
    return output_list
print(my_range(10) == list(range(10)))

def my_reversed(input_list):
    output_list = []
    idx=len(input_list)-1
    while(idx >= 0):
        output_list.append(input_list[idx])
        idx=idx-1
    return output_list
#we always need to pay attention to the index position

print(my_reversed([]) == [])
#it prints true

my_set = {"Bilbo"}
my_set.update({"Frodo", "Sam", "Pippin", "Merry"})
my_set.remove("Bilbo")
my_set.add("Saruman")
my_list = list(my_set)
my_list.sort()
print(my_list)

set_hobbit = {"Frodo", "Sam", "Pippin", "Merry"}
set_magician = {"Saruman", "Gandalf"}
lotr = dict()
lotr["hobbit"] = set_hobbit
lotr["magician"] = set_magician
lotr["other"] = {} #just for exercise reasons
#to create a dict, use a subrscript operation with a key string
#and assign as a value the requested set in this case
print(lotr)

def exponentiation(base_number, exponent):
    if exponent == 0:
        return 1
    elif exponent == 1:
        return base_number
    else:
        return base_number*exponentiation(base_number, exponent-1)

def test_exp(base_number, exponent, expected):
    return exponentiation(base_number, exponent)==expected
print(test_exp(3,4,3**4))
print(test_exp(17,1,17**1))
print(test_exp(2,0,2**0))
#l'operazione di 3^4 è identica a exp(3,4) = 3*exp(3,4-1)
#l'operazione di 3^3 è identica a exp(3,3) = a 3*exp(3,3-1)
#l'operazione di 3^2 è identica a exp(3,2) = a 3*exp(3,2-1)
#l'operazione di 3^1 è 3
#"risalgo" come ho fatto un tempo per fibonacci: sostituisco exp(3,2-1) col suo risultato che è 3
#quindi exp(3,2)=3*exp(3,1)=3*3=9
#poi exp(3,3)=3*exp(3,2)=3*9=27
#infine expo(3,4)=3*exp(3,3)=3*27=81