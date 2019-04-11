'''
  1.接受输入，判读是否有解
  2.有解则找0值
  3.分析移动，计算评估函数
  4.全局排序，选择下一步
  5.判断是否是目标状态，是则跳出循环，否则回到2
  6.输出path
测试值：
1.[[2,8,3],[1,6,4],[7,0,5]]
2.[[1,0,4],[7,3,5],[8,6,2]]
3.[[3,4,1],[0,8,6],[7,2,5]]
目标状态：[[1,2,3],[8,0,4],[7,6,5]]
'''
import copy

class Node():
    def __init__(self,data,parent=None,point=0):
        self.data = data
        self.parent = parent
        self.point = point

def e_solution(s):
    test = []
    for i in s:
        for j in i:
            test.append(j)
    p = 0
    for i in range(1,9):
        if test[i] == 0:
            continue
        now = test[i]
        for j in range(i):
            if test[j] == 0:
                continue
            elif test[j] < now:
                p += 1
    if p%2 == 1:
        return True
    else:
        return False

def find_num(in_list,num):
    #可直接用（0,1,2）进行判断，在更普遍的情况下根据输入的长度进行循环
    lth_ex = len(in_list)
    for i in range(lth_ex):
        lth_in = len(in_list[i])
        for j in range(lth_in):
            if in_list[i][j] == num:
                return i,j
            
def get_coo_movie(coo):
    #分四块进行判断，上下左右进行移动
    coo_movie = []
    if coo[0] <= 1:
        #上两排可向下移动
        coo_movie.append((coo[0]+1,coo[1]))
    if coo[0] >= 1:
        #下两排可向上移动
        coo_movie.append((coo[0]-1,coo[1]))
    if coo[1] <= 1:
        #左两排
        coo_movie.append((coo[0],coo[1]+1))
    if coo[1] >= 1:
        #右两排
        coo_movie.append((coo[0],coo[1]-1))
    return coo_movie

def move(node,coo_zreo,coo_move):
    after_move = []
    s = node.data
    if node.parent != None:
        par = node.parent.data
    else:
        par = []
    m = coo_zreo[0]
    n = coo_zreo[1]
    lth = len(coo_move)
    for i in range(lth):
        new = copy.deepcopy(s)
        new_m = coo_move[i][0]
        new_n = coo_move[i][1]
        new[m][n] = s[new_m][new_n]
        new[new_m][new_n] = 0
        new[3] += 1
        if new[0:3] == par[0:3]: #避免回到上一个节点
            continue
        else:
            new_node = Node(data=new,parent=node)
            after_move.append(new_node)
    return after_move

def assess(sn):
    s_aim = [[1,2,3],[8,0,4],[7,6,5]]
    tag_num = 0
    for i in (0,1,2):
        for j in (0,1,2):
            if sn[i][j] == 0:
                continue
            num_coo = find_num(s_aim,sn[i][j])
            m = num_coo[0]
            n = num_coo[1]
            tag_num += abs(i-m) + abs(j-n)

    if tag_num == 0 or tag_num == 1:
        #if get the aim, increase priority
        assess_point = tag_num
    else:
        assess_point = sn[3] + tag_num
    return assess_point

def get_next(open_list):
    point_list = []
    n_list = []
    step_list = []
    for each in open_list:
        point_list.append(each.point)
    min_point = min(point_list)
    for each in open_list:
        if each.point == min_point:
            n_list.append(each)
    for each in n_list:
        step_list.append(each.data[3])
    max_step = max(step_list)
    for each in n_list:
        if each.data[3] == max_step:
            return each

def main(s0):
    s0.append(0) #加一个标记，表示移动次数
    node0 = Node(s0)
    s_aim = [[1,2,3],[8,0,4],[7,6,5]]
    route = []
    open_list = []
    route.append(node0)
    open_list.append(node0)
    while s0[0:3] != s_aim:
        node0 = get_next(open_list)
        open_list.remove(node0)
        s0 = node0.data
        route.append(node0)
        #get coordinate of 0 and the nodes possible
        coo_zero = find_num(s0,0)
        coo_move_to = get_coo_movie(coo_zero)
        after_move = move(node0,coo_zero,coo_move_to)
        #get assess point of every possible node
        for each in after_move:
            assess_ponit = assess(each.data)
            each.point = assess_ponit
            open_list.append(each)
    
    last = route[-1]
    path=[]
    #from the last to get the path
    while last:
        path.insert(0,last.data)
        last = last.parent
    print('Got it. The path is')
    for each in path:
        print(each[3],':',each[0:3])


ini_v = input('Please input a initial value(input q or Q to stop):')
while ini_v not in ('q','Q'):
    s0 = eval(ini_v)
    if e_solution(s0):
        print('Looking for the path...')
        main(s0)
    else:
        print('There is no path...')
    ini_v = input('Please input a initial value(input q or Q to stop):')
print('Over. Thanks for using.')
