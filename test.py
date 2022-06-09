from vehicle import Vehicle
import random

initial_coords = [[41.198193, -8.627468, 4], [41.198187, -8.627429, 5], [41.198183, -8.627389, 6], [41.198290, -8.627454, 1], [41.198287, -8.627414, 2], [41.198282, -8.627371, 3]]


row_ls = [1,1,2,2,3,3] #1 -> right, 2 -> middle, 3 -> left
exit_ls = [1,2,3,random.randint(1, 3),random.randint(1, 3),random.randint(1, 3)]
random.shuffle(row_ls)
random.shuffle(initial_coords)
random.shuffle(exit_ls)
vehicle1 = Vehicle(1, exit_ls.pop(),initial_coords.pop())
ls=[]
for i in initial_coords:
    ls.append((i[0], i[1]))

print(ls)

vehicle1.get_position(ls)