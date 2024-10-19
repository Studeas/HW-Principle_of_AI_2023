import sys, pygame, random, time, queue, itertools
import tkinter as tk
pygame.init()

# 地图长度/尺寸
random.seed(0)
length = random.choice((7,8,9,10,11))

# 窗口大小
size = width, height = 100*length, 100*length
screen = pygame.display.set_mode(size)
speed = [1, 2]
black = 0, 0, 0


class maze_game:
    # 构造函数
    def __init__(self, length, k = 1, m = 1) -> None:
         self.Length = length
         # 9*9地图。E--Empty, W--Wall, M--Monster, S--Shield, A--Start, B--End
         self.Map = [['E' for j in range(length)] for i in range(length)]
         # k个怪兽，m个盾牌
         self.Num_Mons = k
         self.Num_Shie = m
         # 存储特殊点
         self.Start_End_Pos = [(0, 0), (0, 0)]
         self.Shield_Pos = [(0, 0) for i in range(self.Num_Shie)]
    
    
    # 随机生成地图
    def Gene_RandomMap(self, Obstacles_Ratio=0.4, Seed=0): 
        #随机生成全部非Ground元素
        Num_Nonground = int(Obstacles_Ratio * self.Length * self.Length)
        random.seed(Seed)
        # 合法格点，以供采样
        Available_pos = [(x, y) for x in range(0, self.Length) for y in range(0, self.Length)]

        if Num_Nonground > len(Available_pos):
            print("生成的障碍物数量大于可用位置数量。")
            return
    
        # 随机采样出非ground的格点，先全部作为Wall
        All_Nonground = random.sample(Available_pos, Num_Nonground)
        for x, y in All_Nonground:
            self.Map[x][y] = 'W'
    
        # 从Wall中再随机采样，选出怪兽数 + 盾牌数 + 起点 + 终点
        random.seed(Seed + 1)
        # 选出怪兽
        Monster_pos = random.sample(All_Nonground, self.Num_Mons)
        for x, y in Monster_pos:
            self.Map[x][y] = 'M'
        # 选出盾牌
        Shield_pos = random.sample(All_Nonground, self.Num_Shie)
        self.Shield_Pos = Shield_pos
        for x, y in Shield_pos:
            self.Map[x][y] = 'S'
        # 选出起点
        Start_pos = random.sample(All_Nonground, 1)
        self.Start_End_Pos[0] = Start_pos[0]
        for x, y in Start_pos:
            self.Map[x][y] = 'A' 
        # 选出终点
        End_pos = random.sample(All_Nonground, 1)
        self.Start_End_Pos[1] = End_pos[0]
        for x, y in End_pos:
            self.Map[x][y] = 'B'
    
    
    # 判定是否是合法移动1
    def Is_Valid_Move1(self, x, y, prev_x, prev_y): # 目前针对Problem1
        if x < 0 or y < 0 or x >= self.Length or y >= self.Length:
            return False
        if self.Map[x][y] == 'W' or self.Map[x][y] == 'M':
            return False
        return True
    
    
    # 判定是否是合法移动2
    def Is_Valid_Move2(self, x, y, prev_x, prev_y):
        if x < 0 or y < 0 or x >= self.Length or y >= self.Length:
            return False
        if self.Map[x][y] == 'W':
            return False
        return True
    
    
    # 获得下一步的行走范围1
    def Get_Possible_Moves1(self, x, y): # 目前针对Problem1  
        Possible_Moves = [
        (x + 1, y), (x, y + 1),
        (x - 1, y), (x, y - 1)
        ]
        return [(nx, ny) for nx, ny in Possible_Moves if self.Is_Valid_Move1(nx, ny, x, y)]
    

    # 获得下一步的行走范围2
    def Get_Possible_Moves2(self, x, y): # 目前针对Problem1  
        Possible_Moves = [
        (x + 1, y), (x, y + 1),
        (x - 1, y), (x, y - 1)
        ]
        return [(nx, ny) for nx, ny in Possible_Moves if self.Is_Valid_Move2(nx, ny, x, y)]
    

    # 计算在地图上两点之间的最短路程，BFS法1
    def Shortest_Distance_2points1(self, x_s, y_s, x_e, y_e):
        # 采用BFS求解问题2中各点的最短路：A-S1-S2...-Sm-B, C_{n+2}^2
        Visited = set()
        BFS_queue = queue.Queue()
        BFS_queue.put(((x_s, y_s), []))
        Search_Times = 0
        while not BFS_queue.empty():
            # 队首出队列，Position存储位置，Route存储路径
            Position, Route = BFS_queue.get()
            Search_Times += 1
            # 判断是否到达终点
            if Position == (x_e, y_e):
                # Mark记录是“第几步”
                Mark = 0 - 1
                for i in Route:
                    #self.board[i[0]][i[1]] = Mark
                    Mark += 1
                #print("找到最短路径，移动次数为：", Mark - 1)
                #print("搜索次数为：", Search_Times - 1)
                return [Mark, Route]
            
            # 遍历一步可达的合法节点（下一步）
            for Next_Pos in self.Get_Possible_Moves1(Position[0], Position[1]):
                # 如果节点未访问过，则标记为访问并且从队尾入队列，更新Route
                if Next_Pos not in Visited:
                    Visited.add(Next_Pos)
                    BFS_queue.put((Next_Pos, Route + [Next_Pos]))

        # 如果查找失败，即终点不可达，则输出提示语
        print("There is no path between the two points.")
        return [1000, []] 
    

    # 计算在地图上两点之间的最短路程，BFS法2
    def Shortest_Distance_2points2(self, x_s, y_s, x_e, y_e):
        # 采用BFS求解问题2中各点的最短路：A-S1-S2...-Sm-B, C_{n+2}^2
        Visited = set()
        BFS_queue = queue.Queue()
        BFS_queue.put(((x_s, y_s), []))
        Search_Times = 0
        while not BFS_queue.empty():
            # 队首出队列，Position存储位置，Route存储路径
            Position, Route = BFS_queue.get()
            Search_Times += 1
            # 判断是否到达终点
            if Position == (x_e, y_e):
                # Mark记录是“第几步”
                Mark = 0 - 1
                for i in Route:
                    #self.board[i[0]][i[1]] = Mark
                    Mark += 1
                #print("找到最短路径，移动次数为：", Mark - 1)
                #print("搜索次数为：", Search_Times - 1)
                return [Mark, Route]
            
            # 遍历一步可达的合法节点（下一步）
            for Next_Pos in self.Get_Possible_Moves2(Position[0], Position[1]):
                # 如果节点未访问过，则标记为访问并且从队尾入队列，更新Route
                if Next_Pos not in Visited:
                    Visited.add(Next_Pos)
                    BFS_queue.put((Next_Pos, Route + [Next_Pos]))

        # 如果查找失败，即终点不可达，则输出提示语
        print("There is no path between the two points.")
        return [1000, []] 


    # 问题1求解器
    def Solve_1(self):
        """
        首先求出一张A-S1-S2...-Sm-B两两之间最短路程表
        之后给出A-Sj1-Sj2...-Sjm-B等A_m^2种排序，求解最短总路程，并输出最短路程途径的点
        """
        # 求出起点、终点、盾牌m+2个点两两之间的最短路径（最短路径和cost）
        Point_Set = [self.Start_End_Pos[0]] + self.Shield_Pos + [self.Start_End_Pos[1]]
        Short_Dis_Table = [[1000 for j in range(self.Num_Shie + 2)] for i in range(self.Num_Shie + 2)]
        Short_Path_Table = [[[] for j in range(self.Num_Shie + 2)] for i in range(self.Num_Shie + 2)] 
        for i in range(self.Num_Shie + 2):
            for j in range(self.Num_Shie + 2):
                xi = Point_Set[i][0]
                yi = Point_Set[i][1]
                xj = Point_Set[j][0]
                yj = Point_Set[j][1]
                Short_Dis_Table[i][j], Short_Path_Table[i][j] = self.Shortest_Distance_2points1(xi, yi, xj, yj)
        #print(Short_Dis_Table)    
        #print(Short_Path_Table)
        # 求取S1-S2-...-Sm的全排列
        permutation = []
        for i in range(self.Num_Shie):
            permutation.append(i + 1)
        all_permutation = list(itertools.permutations(permutation))
        #print(all_permutation)
        # 求和并且比较所有路径，找出最短路径
        Shortest_Path_Cost = 1000
        Shortest_Path_Order = [(0, 0)]
        Shortest_Path_Full_Result = []
        Cur_Path_Cost = 0
        for cur_path in all_permutation:
            Cur_Path_Cost += Short_Dis_Table[0][cur_path[0]]
            for i in range(0, self.Num_Shie - 1):
                Cur_Path_Cost += Short_Dis_Table[cur_path[i]][cur_path[i+1]]
                if Cur_Path_Cost > Shortest_Path_Cost:
                    break
            Cur_Path_Cost += Short_Dis_Table[cur_path[self.Num_Shie - 1]][self.Num_Shie + 1]
            if Cur_Path_Cost < Shortest_Path_Cost:
                Shortest_Path_Cost = Cur_Path_Cost
                Shortest_Path_Order[0] = cur_path 
        #print(Shortest_Path_Cost)
        #print(Shortest_Path_Order)
        Shortest_Path_Full_Result += Short_Path_Table[0][Shortest_Path_Order[0][0]]
        #print(Shortest_Path_Full_Result)
        for i in range(0, self.Num_Shie - 1):
            Shortest_Path_Full_Result += Short_Path_Table[Shortest_Path_Order[0][i]][Shortest_Path_Order[0][i + 1]]
        Shortest_Path_Full_Result += Short_Path_Table[Shortest_Path_Order[0][self.Num_Shie - 1]][self.Num_Shie + 1]  
        return [Shortest_Path_Cost, Shortest_Path_Full_Result]         
        #print(Shortest_Path_Full_Result)


    # 问题2求解器        
    def Solve_2(self, p, h, s): # 初始生命值 p、怪物伤害 h、盾牌防御 s 
        """ 
        首先找到从起点到终点的路程最短路径，之后check本路径上是否含有怪兽、盾牌
        如果含有怪兽和盾牌，并且怪兽数量大于盾牌，那么考虑其他策略：寻找一个cost最低的新盾牌，或者绕过去
        其余和问题1一样 
        """
        # 最终的总代价，包含路程和生命减损
        ul_cost = 0
        # 首先求出起终点“路程最短”的最短路，记录路径及其长度
        xs = self.Start_End_Pos[0][0]
        ys = self.Start_End_Pos[0][1]
        xe = self.Start_End_Pos[1][0]
        ye = self.Start_End_Pos[1][1]
        Short_Path_by_Length = self.Shortest_Distance_2points2(xs, ys, xe, ye) # 用距离测量2，允许经过怪兽
        #print("xs = ",xs,ys,xe,ye)
        #print("solve2",Short_Path_by_Length)
        # check最短路上是否含有盾牌和怪兽，并统计其数量
        num_shie_thispath = 0
        num_mons_thispath = 0
        Pos_attri = []
        check_stack = [] # 栈，用来检查M和S出现的次序和数目问题
        Problem_Monster = []
        Shield_and_Monster = [['A',self.Start_End_Pos[0]]]
        #Shield_Near_P_M = []
        for i in Short_Path_by_Length[1]:
            this_attri = self.Map[i[0]][i[1]]
            Pos_attri.append(this_attri)
            if this_attri == 'M':
                num_mons_thispath += 1
                Shield_and_Monster.append(['M', i])
                # check
                check_stack.append(this_attri)
                if check_stack[0] == 'S':
                    # 新进入的Monster先出栈
                    check_stack.pop()
                    # 紧邻的Shield再出栈
                    check_stack.pop()
                else:
                    Problem_Monster.append(i)
                    check_stack.pop()
            if this_attri == 'S':
                num_shie_thispath += 1
                Shield_and_Monster.append(['S', i])
                # check
                check_stack.append(this_attri)
        Shield_and_Monster.append(['B', self.Start_End_Pos[1]])
        # 如果路上没有怪兽，直接输出结果
        if num_mons_thispath == 0:
            return Short_Path_by_Length
        else:
            # 如果在路途上，每一个怪兽之前都有“足够的”盾牌，即大于等于当前访问过的怪兽数量
            # 那么无需再去寻找新的盾牌，需要考虑的策略仅有是否“绕开”
            if len(Problem_Monster) == 0:
                # 从旁边绕开，最少也要多走2步，如果在盾牌防御下，怪兽造成的生命值损害小于2，则直接打怪即可
                if h - s < 2:
                    Short_Path_by_ulcost = Short_Path_by_Length
                    Short_Path_by_ulcost[0] += num_mons_thispath*(h-s)
                    return Short_Path_by_ulcost
                # 否则需要考虑绕路（盾牌数量是足够的）
                else:
                    Short_Path_by_ulcost = Short_Path_by_Length
                    key_len = len(Shield_and_Monster)
                    for i in range(key_len):
                        if Shield_and_Monster[i][0] == 'M':
                            for j in range(i, key_len):
                                if Shield_and_Monster[j][0] != 'M':
                                    txs = Shield_and_Monster[i-1][1][0]
                                    tys = Shield_and_Monster[i-1][1][1]
                                    txe = Shield_and_Monster[j][1][0]
                                    tye = Shield_and_Monster[j][1][1]
                                    temp = self.Shortest_Distance_2points1(txs,tys,txe,tye)
                                    oldpath = self.Shortest_Distance_2points2(txs,tys,txe,tye)
                                    if temp[0] - oldpath[0] < h - s:
                                        Short_Path_by_ulcost = self.Shortest_Distance_2points2(xs,ys,txs,tys) + temp + self.Shortest_Distance_2points2(txe,tye,xe,ye)
                                        del Shield_and_Monster[i:j]
                    new_num_mons = 0
                    for i in Shield_and_Monster:
                        if Shield_and_Monster[i][0] == 'M':
                            new_num_mons += 1
                    num_mons_thispath = new_num_mons
                    Short_Path_by_ulcost[0] += num_mons_thispath*(h-s)
                    return Short_Path_by_ulcost
            # 如果情况并非如上述，那么还需要考虑在当前怪兽之前的路径上寻找盾牌
            # 比较寻找盾牌、绕开、直接打怪三者的cost，选择一个合适的方案
            else:
                # 由于时间有限，这一部分完成度欠佳
                Short_Path_by_ulcost = Short_Path_by_Length
                key_len = len(Shield_and_Monster)
                for i in range(key_len):
                    if Shield_and_Monster[i][0] == 'M':
                        for j in range(i, key_len):
                            if Shield_and_Monster[j][0] != 'M':
                                txs = Shield_and_Monster[i-1][1][0]
                                tys = Shield_and_Monster[i-1][1][1]
                                txe = Shield_and_Monster[j][1][0]
                                tye = Shield_and_Monster[j][1][1]
                                temp = self.Shortest_Distance_2points1(txs,tys,txe,tye)
                                oldpath = self.Shortest_Distance_2points2(txs,tys,txe,tye)
                                if temp[0] - oldpath[0] < h - s:
                                    Short_Path_by_ulcost = self.Shortest_Distance_2points2(xs,ys,txs,tys) + temp + self.Shortest_Distance_2points2(txe,tye,xe,ye)
                                    del Shield_and_Monster[i:j]
                return Short_Path_by_ulcost    


# --------------------------------------------------------------

# 勇者、怪兽、盾牌、墙壁、地板、起点、终点的图片
Soldier = pygame.image.load("img\soldier.png")
Monster = pygame.image.load("img\monster.png")
Shield = pygame.image.load("img\shield.png")
Wall = pygame.image.load("img\wall.png")
Ground = pygame.image.load("img\ground.png")
Start = pygame.image.load("img\startend.png")
End = pygame.image.load("img\startend.png")
Road = pygame.image.load("img\Road.png")

def Draw_Background(Map):
    for i in range(0,length):
        for j in range(0,length):
            if Map[i][j] == 'E':
                screen.blit(Ground,(i*100,j*100))
            if Map[i][j] == 'W':
                screen.blit(Wall,(i*100,j*100))
            if Map[i][j] == 'M':
                screen.blit(Monster,(i*100,j*100))
            if Map[i][j] == 'S':
                screen.blit(Shield,(i*100,j*100))
            if Map[i][j] == 'A':
                screen.blit(Soldier,(i*100,j*100))
            if Map[i][j] == 'B':
                screen.blit(End,(i*100,j*100))

def on_submit():
    user_input1 = entry1.get()
    user_input2 = entry2.get()
    user_input3 = entry3.get()
    #print("用户输入:", user_input)
    return game.Solve_2(user_input1,user_input2,user_input3)

# 创建主窗口
root = tk.Tk()
root.title("输入框")

# 创建标签
label = tk.Label(root, text="请依次输入:")
label.pack(pady=10)

# 创建输入框1
label1 = tk.Label(root, text="初始生命值p:")
label1.pack(pady=5)
entry1 = tk.Entry(root)
entry1.pack(pady=5)

# 创建输入框2
label2 = tk.Label(root, text="怪物伤害h:")
label2.pack(pady=5)
entry2 = tk.Entry(root)
entry2.pack(pady=5)

# 创建输入框3
label3 = tk.Label(root, text="盾牌防御s:")
label3.pack(pady=5)
entry3 = tk.Entry(root)
entry3.pack(pady=5)

# 创建按钮
submit_button = tk.Button(root, text="提交", command=on_submit)
submit_button.pack(pady=10)

#def Draw

# --------------------------------------------------------------

# 创建魔塔游戏对象
game = maze_game(length, 2, 2)
# 随机生成地图
game.Gene_RandomMap(0.4, 3)

result1 = game.Solve_1()

result2 = game.Solve_2(20,2,1)

# 创建勇士的rect对象，并将其位置初始化为起点位置
Sodier_rect = Soldier.get_rect()
Sodier_rect.topleft = (game.Start_End_Pos[0][0]*100,game.Start_End_Pos[0][1]*100)
#print(game.Start_End_Pos[0][0]*100,game.Start_End_Pos[0][1]*100)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    # 绘制地图背景
    Draw_Background(game.Map)
    screen.blit(Soldier, Sodier_rect)
        
    # 绘制问题1的查找结果
    path = result1[1]
        #print(path)
    for next in path:
        # 绘制勇士rect
        #screen.blit(Road, (next[0]*100, next[1]*100))
        screen.blit(Soldier, Sodier_rect)
    
    pygame.display.flip()
    
    # 运行主循环
    root.mainloop()
    Draw_Background(game.Map)
    pygame.display.flip()
    
    # 绘制问题2的查找结果
    path = result2[1]
        #print(path)
    for next in path:
        # 绘制勇士rect
        screen.blit(Road, (next[0]*100, next[1]*100))
        screen.blit(Soldier, Sodier_rect)

    screen.blit(Soldier, Sodier_rect)
    while True:
        pygame.display.flip()
    