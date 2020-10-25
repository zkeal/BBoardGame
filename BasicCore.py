# coding=utf-8
import pygame
import Cplayer
from Alphabeta_search import ABsearch, get_TT
import numpy as np
import NNFrame as NF




class basic_core:
    def __init__(self):

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GOLDEN = (205, 127, 50)
        self.sliver = (192, 192, 192)
        self.Green = (0, 233, 0)

        self.BoardWidth = 780
        self.BoardHeight = 780
        self.GridWidth = int(self.BoardWidth/13)
        self.init_position = (self.GridWidth+int(self.GridWidth/2), self.GridWidth+int(self.GridWidth/2))
        self.cheese  = np.zeros((11, 11), dtype=np.int) # 1: sliver, 2:golden, 3: flagship
        self.undo_cheese = np.zeros((11, 11), dtype=np.int)

        self.screen = pygame.display.set_mode((960, 840), 0, 32)
        self.points = []
        # self.background_image_filename = 'background.jpg'
        self.selected_pos = (-1,-1)

        # self.background = pygame.image.load(self.background_image_filename).convert()
        self.screen.fill(self.WHITE)
        #self.back_gound = pygame.Surface((960, 840), flags=0, depth=0, masks=None)
        # self.screen.blit(self.background, (0, 0))
        self.BackGround = self.screen.copy()
        self.FPS = 30
        self.clock = pygame.time.Clock()
        self.inital_board()
        self.select_status = 0
        self.turn_opportunity = 2
        self.active_flag = 1
        self.COUNT = pygame.USEREVENT + 1
        self.counts = 600
        pygame.init()
        pygame.time.set_timer(self.COUNT, 1000)

    def draw_background(self, surf, HEIGHT, WIDTH ,GRID_WIDTH):
        # 加载背景图片
        # surf.blit(self.background_img, (0, 0))

        # 画网格线，棋盘为 19行 19列的
        # 1. 画出边框，这里 GRID_WIDTH = WIDTH // 20
        rect_lines = [
            ((GRID_WIDTH, GRID_WIDTH), (GRID_WIDTH, HEIGHT - GRID_WIDTH)),
            ((GRID_WIDTH, GRID_WIDTH), (WIDTH - GRID_WIDTH, GRID_WIDTH)),
            ((GRID_WIDTH, HEIGHT - GRID_WIDTH),
             (WIDTH - GRID_WIDTH, HEIGHT - GRID_WIDTH)),
            ((WIDTH - GRID_WIDTH, GRID_WIDTH),
             (WIDTH - GRID_WIDTH, HEIGHT - GRID_WIDTH)),
        ]

        font = pygame.font.Font(None, 30)
        vertical_line = ['11', '10', '9', '8', '7', '6', '5', '4', '3', '2', '1']
        horizontal_line = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']



        for line in rect_lines:
            pygame.draw.line(surf, self.BLACK, line[0], line[1], 2)

        # 画出中间的网格线
        for i in range(10):
            pygame.draw.line(surf, self.BLACK,
                             (GRID_WIDTH * (2 + i), GRID_WIDTH),
                             (GRID_WIDTH * (2 + i), HEIGHT - GRID_WIDTH))

            pygame.draw.line(surf, self.BLACK,
                             (GRID_WIDTH, GRID_WIDTH * (2 + i)),
                             (HEIGHT - GRID_WIDTH, GRID_WIDTH * (2 + i)))

            ver_textSurfaceObj = font.render(vertical_line[i], True, self.BLACK)
            ver_textRectObj = ver_textSurfaceObj.get_rect()
            ver_textRectObj.center = (int(self.GridWidth/2), GRID_WIDTH * (2 + i)-int(self.GridWidth/2))
            surf.blit(ver_textSurfaceObj,ver_textRectObj)

            hori_textSurfaceObj = font.render(horizontal_line[i], True, self.BLACK)
            hori_textRectObj = hori_textSurfaceObj.get_rect()
            hori_textRectObj.center = (GRID_WIDTH * (2 + i) - int(self.GridWidth / 2), int(self.GridWidth/2))
            surf.blit(hori_textSurfaceObj, hori_textRectObj)

        ver_textSurfaceObj = font.render(vertical_line[10], True, self.BLACK)
        ver_textRectObj = ver_textSurfaceObj.get_rect()
        ver_textRectObj.center = (int(self.GridWidth/2), GRID_WIDTH * (2 + 10)-int(self.GridWidth/2))
        surf.blit(ver_textSurfaceObj, ver_textRectObj)

        hori_textSurfaceObj = font.render(horizontal_line[10], True, self.BLACK)
        hori_textRectObj = hori_textSurfaceObj.get_rect()
        hori_textRectObj.center = (GRID_WIDTH * (2 + 10) - int(self.GridWidth / 2), int(self.GridWidth/2))
        surf.blit(hori_textSurfaceObj, hori_textRectObj)

    def inital_board(self):
        for i in range(3,8):
            self.cheese[1][i] = 1
            self.cheese[i][1] = 1
            self.cheese[i][9] = 1
            self.cheese[9][i] = 1

        for i in range(4,7):
            self.cheese[3][i] = 2
            self.cheese[7][i] = 2
            self.cheese[i][3] = 2
            self.cheese[i][7] = 2

        self.cheese[5][5] = 3


    def update_board(self, surf, CurrentResult, gamelog,runmode):

        if CurrentResult == -1: # game continue
            for i in range(len(self.cheese)):
                for j in range(len(self.cheese[0])):
                    if self.cheese[i][j] ==  3:
                        pygame.draw.circle(surf, self.GOLDEN, (self.init_position[0] + i * self.GridWidth, self.init_position[1] + j * self.GridWidth), int(self.GridWidth/2) - 5, 10)
                    if self.cheese[i][j] ==  2:
                        pygame.draw.circle(surf, self.GOLDEN, (
                        self.init_position[0] + i * self.GridWidth, self.init_position[1] + j * self.GridWidth),
                                           int(self.GridWidth / 2) - 5)
                    if self.cheese[i][j] == 1:
                        pygame.draw.circle(surf, self.sliver, (
                        self.init_position[0] + i * self.GridWidth, self.init_position[1] + j * self.GridWidth),
                                           int(self.GridWidth / 2) - 5)
                    if self.cheese[i][j] >9:
                        pygame.draw.circle(surf, self.Green, (
                        self.init_position[0] + i * self.GridWidth, self.init_position[1] + j * self.GridWidth),
                                       int(self.GridWidth / 2), 5)

            font = pygame.font.Font(None, 50)
            if self.active_flag == 0:
                textSurfaceObj = font.render("Sliver's Turn", True,self.sliver, self.BLACK)
                textRectObj = textSurfaceObj.get_rect()
                textRectObj.center = (840,100)
                surf.blit(textSurfaceObj, textRectObj)
            if self.active_flag != 0:
                textSurfaceObj = font.render("Golden's Turn", True,self.GOLDEN, self.BLACK)
                textRectObj = textSurfaceObj.get_rect()
                textRectObj.center = (840,100)
                surf.blit(textSurfaceObj, textRectObj)

        winfont = pygame.font.Font(None, 100)
        if CurrentResult == 0:
            textSurfaceObj = winfont.render("Sliver Win", True, self.sliver, self.BLACK)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (480, 400)
            surf.blit(textSurfaceObj, textRectObj)
            print("Sliver Win ")

        if CurrentResult == 1:
            textSurfaceObj = winfont.render("Gloden Win", True, self.GOLDEN, self.BLACK)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (480, 400)
            surf.blit(textSurfaceObj, textRectObj)
            print("Golden Win ")

        LogFont = pygame.font.Font(None, 30)
        if gamelog is not None and len(gamelog) > 0:
            if self.active_flag == 1:
                textSurfaceObj_t = LogFont.render("Sliver's action", True, self.sliver, self.BLACK)
                textRectObj_t = textSurfaceObj_t.get_rect()
                textRectObj_t.center = (840, 300)
                surf.blit(textSurfaceObj_t, textRectObj_t)
                textSurfaceObj = LogFont.render(gamelog[len(gamelog)-1], True, self.sliver, self.BLACK)
                textRectObj = textSurfaceObj.get_rect()
                textRectObj.center = (840, 350)
                surf.blit(textSurfaceObj, textRectObj)
            if self.active_flag == 0:
                textSurfaceObj_t = LogFont.render("Golden's action", True, self.GOLDEN, self.BLACK)
                textRectObj_t = textSurfaceObj_t.get_rect()
                textRectObj_t.center = (840, 300)
                surf.blit(textSurfaceObj_t, textRectObj_t)
                textSurfaceObj = LogFont.render(gamelog[len(gamelog)-1], True, self.GOLDEN, self.BLACK)
                textRectObj = textSurfaceObj.get_rect()
                textRectObj.center = (840, 350)
                surf.blit(textSurfaceObj, textRectObj)

        # if runmode == 1:
        #     textSurfaceObj_c = LogFont.render("AL's Timer", True, self.BLACK, self.WHITE)
        #     textRectObj_c = textSurfaceObj_c.get_rect()
        #     textRectObj_c.center = (840, 700)
        #     surf.blit(textSurfaceObj_c, textRectObj_c)
        #     textSurfaceObcs = LogFont.render(str(self.counts), True, self.GOLDEN, self.BLACK)
        #     textSurRectcs = textSurfaceObcs.get_rect()
        #     textSurRectcs.center = (840, 750)
        #     surf.blit(textSurfaceObcs, textSurRectcs)



    def Wining_judege(self):
        SliShip = np.argwhere(self.cheese == 1)
        if len(SliShip) == 0:
            return 1

        flagship_index = np.squeeze(np.argwhere(self.cheese == 3))
        if len(flagship_index) == 0:
            if self.cheese.max() == 13:
                return -1
            else:
                return 0
        if flagship_index[0] == 0 or flagship_index[1] == 0 or flagship_index[0] == 10 or flagship_index[1]==10:
            return 1
        return -1


    def restore_cheese(self):
        for i in range(len(self.cheese)):
            for j in range(len(self.cheese[0])):
                if self.cheese[i][j] > 9:
                    self.cheese[i][j] = self.cheese[i][j] - 10

    def moving(self, index_x, index_y):
        temp_chess = self.cheese
        if (self.active_flag == 0 and self.cheese[index_x][index_y] == 1) or (self.active_flag == 1 and self.cheese[index_x][index_y] >=2) :
            if self.select_status == 0: # perpare a chess to move
                if 0 <= index_x< 11 and 0 <= index_x < 11:
                    if temp_chess[index_x][index_y] != 0:
                        temp_chess[index_x][index_y] = temp_chess[index_x][index_y] + 10
                self.select_status = 1
                self.selected_pos = (index_x, index_y)

            return temp_chess
        if self.select_status == 1:
            # moving mode

            if index_x == self.selected_pos[0] and index_y == self.selected_pos[1]:
                self.select_status = 0
                return temp_chess
            if index_x == self.selected_pos[0] and index_y != self.selected_pos[1]:
                if index_y > self.selected_pos[1]:
                    for i in range(self.selected_pos[1]+1, index_y+1):
                        if temp_chess[index_x][i] != 0: # moving illegal
                            self.select_status = 1
                            return None
                if index_y < self.selected_pos[1]:
                    for i in range(index_y, self.selected_pos[1]):
                        if temp_chess[index_x][i] != 0:
                            self.select_status = 1
                            return None
            if index_y == self.selected_pos[1] and index_x != self.selected_pos[0]:
                if index_x > self.selected_pos[0]:
                    for i in range(self.selected_pos[0]+1, index_x+1):
                        if temp_chess[i][index_y] != 0:
                            self.select_status = 1
                            return None
                if index_x < self.selected_pos[0]:
                    for i in range(index_x, self.selected_pos[0]):
                        if temp_chess[i][index_y] != 0:
                            self.select_status = 1
                            return None
            if index_x != self.selected_pos[0] and index_y != self.selected_pos[1]:
                self.select_status = 0
                return None

            if self.cheese[self.selected_pos[0]][self.selected_pos[1]] != 3:
                if self.turn_opportunity >= 1:
                    self.turn_opportunity = self.turn_opportunity - 1
                else:
                    self.select_status = 0
                    return None
            else:
                if self.turn_opportunity >= 2:
                    self.turn_opportunity = self.turn_opportunity - 2
                else:
                    self.select_status = 0
                    return None
            self.select_status = 0
            temp_chess[index_x][index_y] = self.cheese[self.selected_pos[0]][self.selected_pos[1]]
            temp_chess[self.selected_pos[0]][self.selected_pos[1]] = 0

        return temp_chess


    def capture(self, index_x, index_y):
        if self.turn_opportunity >= 2:
            temp_chess = self.cheese
            if index_x == self.selected_pos[0] - 1 or index_x == self.selected_pos[0] + 1:
                if index_y == self.selected_pos[1] - 1 or index_y == self.selected_pos[1] + 1:
                    if temp_chess[index_x][index_y] + temp_chess[self.selected_pos[0]][self.selected_pos[1]] == 3 or temp_chess[index_x][index_y] + temp_chess[self.selected_pos[0]][self.selected_pos[1]] == 4:
                        if temp_chess[index_x][index_y] != temp_chess[self.selected_pos[0]][self.selected_pos[1]]:
                            temp_chess[index_x][index_y] = temp_chess[self.selected_pos[0]][self.selected_pos[1]]
                            temp_chess[self.selected_pos[0]][self.selected_pos[1]] = 0
                            self.select_status = 0
                            self.turn_opportunity = self.turn_opportunity - 2
                            return temp_chess
        self.select_status = 0
        return None


    def run(self, runmode, p_flag = 1,depth =1):

        #runmode = 0/two people 1/1people 1AI 2/two AI

        Sliver = Cplayer.ChessPlayer(1)
        Golden = Cplayer.ChessPlayer(2)
        gamelog = []

        running = True
        while running:
            BackGround = pygame.Surface((960, 840), flags=0)
            BackGround.fill(self.WHITE)

            self.draw_background(BackGround, self.BoardHeight, self.BoardWidth, self.GridWidth)
            # 设置屏幕刷新频率
            self.clock.tick(self.FPS)
            if runmode == 0:
            # 处理不同事件
                for event in pygame.event.get():
                    # 检查是否关闭窗口
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.restore_cheese()
                        x, y = pygame.mouse.get_pos()
                        index_x = int(x / self.GridWidth) - 1
                        index_y = int(y / self.GridWidth) - 1

                        if index_x > 10 or index_x < 0 or index_y > 10 or index_y < 0:
                            break
                        print('x:' + str(index_x) + 'y:' + str(index_y))
                        if self.turn_opportunity > 0:
                            if self.select_status ==1 and self.cheese[index_x][index_y] != 0:
                                temp_chesss = self.capture(index_x,index_y)
                            else:
                                temp_chesss = self.moving(index_x, index_y)
                            if temp_chesss is not None:
                                self.cheese = temp_chesss
                if self.turn_opportunity < 1:
                    self.active_flag = int(not self.active_flag)
                    self.turn_opportunity = 2

            if runmode == 1:
                # player operate it
                if self.active_flag == p_flag:
                    for event in pygame.event.get():
                        # 检查是否关闭窗口
                        if event.type == pygame.QUIT:
                            running = False
                            pygame.quit()
                            exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.restore_cheese()
                            x, y = pygame.mouse.get_pos()
                            index_x = int(x / self.GridWidth) - 1
                            index_y = int(y / self.GridWidth) - 1

                            if index_x > 10 or index_x < 0 or index_y > 10 or index_y < 0:
                                break
                            if self.turn_opportunity > 0:
                                if self.select_status == 1 and self.cheese[index_x][index_y] != 0:
                                    temp_chesss = self.capture(index_x, index_y)
                                else:
                                    temp_chesss = self.moving(index_x, index_y)
                                if temp_chesss is not None:
                                    self.cheese = temp_chesss
                    if self.turn_opportunity < 1:
                        self.active_flag = int(not self.active_flag)
                        self.turn_opportunity = 2
                # player operate golden, AI operate sliver
                if p_flag == 1 and self.active_flag != p_flag:

                    # for event in pygame.event.get():
                    #     if event.type == self.COUNT:
                    #         self.counts = self.counts - 1

                    value, Str_act,consider_act, board=ABsearch("", self.cheese, self.active_flag, depth, Sliver)
                    print(Str_act)
                    print(value)
                    self.cheese = board
                    self.active_flag = int(not self.active_flag)
                    gamelog.append(Str_act)
                # player operate golden, AI operate Golden
                if p_flag == 0 and self.active_flag != p_flag:

                    # for event in pygame.event.get():
                    #     if event.type == self.COUNT:
                    #         self.counts = self.counts - 1

                    value, Str_act,consider_act, board = ABsearch("", self.cheese, self.active_flag, depth, Golden)
                    print(Str_act)
                    print(value)
                    self.cheese = board
                    self.active_flag = int(not self.active_flag)
                    gamelog.append(Str_act)

            # if runmode == 2: # two AI fight with each other
            #     if self.active_flag == 1:
            #         value, Str_act, consider_act, board = ABsearch("", self.cheese, self.active_flag, depth, Golden)
            #         print("Golden: " + Str_act)
            #         print("Golden_value: " + str(value))
            #         self.cheese = board
            #         self.active_flag = int(not self.active_flag)
            #         gamelog.append(Str_act)
            #     if self.active_flag == 0:
            #         value, Str_act, consider_act, board = ABsearch("", self.cheese, self.active_flag, depth,                                                         Sliver)
            #         print("Sliver:" + Str_act)
            #         print("Sliver_value:" + str(value))
            #         self.cheese = board
            #         self.active_flag = int(not self.active_flag)
            #         gamelog.append(Str_act)
            result_now = self.Wining_judege()
            self.update_board(BackGround, result_now,gamelog, runmode)
            # 画出棋盘
            self.screen.blit(BackGround, (0, 0))
            # 刷新屏幕
            pygame.display.flip()
            # if result_now == 1 or 0:
            #     running = False


    def training_evaluatingFunction(self, Sliver, Golden,depth = 1):
        golden_moving = {}
        sliver_moving = {}
        self.inital_board()
        running = True
        S_iterate_value = 0
        G_iterate_value = 0
        golden_loss = 0
        g_pre_value = 0
        g_GAP_max= -1
        Sliver_loss = 0
        S_pre_value = 0
        s_GAP_max= -1
        result_now = 0
        while running:
            if self.active_flag == 1:
                G_iterate_value, Str_act, consider_act, board = ABsearch("", self.cheese, self.active_flag, depth, Golden)
                #print("Golden: " + Str_act)
                #print("Golden_value: " + str(G_iterate_value))
                self.cheese = board
                get_TT(board,golden_moving)
                self.active_flag = int(not self.active_flag)
                if G_iterate_value > g_pre_value and G_iterate_value < 100000:
                    g_GAP = G_iterate_value - g_pre_value
                    golden_loss = golden_loss + g_GAP
                    if g_GAP > g_GAP_max:
                        g_GAP_max = g_GAP
                g_pre_value = G_iterate_value
            if self.active_flag == 0:
                S_iterate_value, Str_act, consider_act, board = ABsearch("", self.cheese, self.active_flag, depth,Sliver)
                #print("Sliver:" + Str_act)
                #print("Sliver_value:" + str(S_iterate_value))
                self.cheese = board
                get_TT(board, sliver_moving)
                self.active_flag = int(not self.active_flag)
                if S_iterate_value < S_pre_value and S_iterate_value < 100000:
                    S_GAP = S_pre_value - S_iterate_value
                    Sliver_loss = Sliver_loss + S_GAP
                    if S_GAP > s_GAP_max:
                        s_GAP_max = S_GAP
                S_pre_value = S_iterate_value
            if S_iterate_value >= 90000000 or S_iterate_value <= -90000000 or G_iterate_value >= 90000000 or G_iterate_value <= -90000000:
                running = False
            if self.cheese.max() < 3:
                result_now = 0
            flagship_index = np.squeeze(np.argwhere(self.cheese == 3))
            if len(flagship_index) == 0:
                result_now = 0
            elif flagship_index[0] == 0 or flagship_index[1] == 0 or flagship_index[0] == 10 or flagship_index[1]==10:
                result_now = 1
        with open('Golden_TT', 'a+') as file:
            file.write(str(golden_moving))
        with open('Sliver_TT', 'a+') as file:
            file.write(str(sliver_moving))
        return result_now,g_GAP_max,s_GAP_max,golden_loss, Sliver_loss
        #累计VALUE 为LOSS OR 队友最大变化VALUE 为loss


    def two_layer_model(self, layers_dims, learning_rate=0.0075, num_iterations=300, print_cost=False):


        Sliver = Cplayer.ChessPlayer(1)
        Golden = Cplayer.ChessPlayer(2)

        np.random.seed(1)
        (n_x, n_h, n_y) = layers_dims
        result_now = 0

        s_parameters = NF.initialize_parameters(n_x, n_h, n_y)
        s_W1 = s_parameters["W1"]
        s_b1 = s_parameters["b1"]
        s_W2 = s_parameters["W2"]
        s_b2 = s_parameters["b2"]
        s_grads = {}

        g_parameters = NF.initialize_parameters(n_x, n_h, n_y)
        g_W1 = g_parameters["W1"]
        g_b1 = g_parameters["b1"]
        g_W2 = g_parameters["W2"]
        g_b2 = g_parameters["b2"]
        g_grads = {}

        # Loop (gradient descent)
        for i in range(0, num_iterations):


            if result_now == 0: # Sliver Win, update golden
                #ss_x = MinMaxScaler()
                #X = ss_x.fit_transform(np.array([Golden.golden_parameters]).T)
                X = np.array([Golden.golden_parameters]).T
                X = X + 0.001
                print(X)
                A1, cache1 = NF.linear_activation_forward(X, g_W1, g_b1, 'relu')
                A2, cache2 = NF.linear_activation_forward(A1, g_W2, g_b2, 'tanh')
                #X_A2 = ss_x.inverse_transform(A2)

                Golden.set_goldenParameters(A2)

                result_now, g_GAP_max, s_GAP_max, golden_loss, Sliver_loss = self.training_evaluatingFunction(Sliver,
                                                                                                              Golden)
                if result_now == 1:
                    continue
                average_loss = np.zeros((7,1)) + (g_GAP_max + golden_loss)/n_x
                print(result_now)
                print(average_loss)

                dA2 = average_loss
                dA1, dW2, db2 = NF.linear_activation_backward(dA2, cache2, 'tanh')
                dA0, dW1, db1 = NF.linear_activation_backward(dA1, cache1, 'relu')
                #g_grads['dW1'] = dW1
                g_grads['db1'] = db1
                g_grads['dW2'] = dW2
                g_grads['db2'] = db2
                g_parameters = NF.update_parameters(g_parameters, g_grads, learning_rate)
                print(dA0)
                curren_X = X + dA0 * learning_rate
                print("Sliver win X"+str(i))
                print(curren_X)
                Golden.set_goldenParameters(curren_X)
                g_W1 = g_parameters["W1"]
                g_b1 = g_parameters["b1"]
                g_W2 = g_parameters["W2"]
                g_b2 = g_parameters["b2"]

            if result_now == 1: # Golden Win, update Sliver
                X = np.array([Sliver.sliver_parameters]).T
                X = X + 0.001
                print(X)

                A1, cache1 = NF.linear_activation_forward(X, s_W1, s_b1, 'relu')
                A2, cache2 = NF.linear_activation_forward(A1, s_W2, s_b2, 'tanh')
                Sliver.set_sliverParameters(A2)

                result_now, g_GAP_max, s_GAP_max, golden_loss, Sliver_loss = self.training_evaluatingFunction(Sliver,
                                                                                                              Golden)
                if result_now ==0:
                    continue

                average_loss = np.zeros((7, 1)) + (s_GAP_max + Sliver_loss) / n_x
                dA2 = average_loss

                dA1, dW2, db2 = NF.linear_activation_backward(dA2, cache2, 'tanh')
                dA0, dW1, db1 = NF.linear_activation_backward(dA1, cache1, 'relu')
                #s_grads['dW1'] = dW1
                s_grads['db1'] = db1
                s_grads['dW2'] = dW2
                s_grads['db2'] = db2
                s_parameters = NF.update_parameters(s_parameters, s_grads, learning_rate)
                curren_X = X + dA0 * learning_rate
                print("Golden win,X:")
                print(curren_X)
                Sliver.set_sliverParameters(curren_X)
                s_W1 = s_parameters["W1"]
                s_b1 = s_parameters["b1"]
                s_W2 = s_parameters["W2"]
                s_b2 = s_parameters["b2"]


        return Golden.golden_parameters, Sliver.sliver_parameters
