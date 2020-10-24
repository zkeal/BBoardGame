# coding=utf-8
import numpy as np


class BDInterface:
    def __init__(self,flag):
        self.flag = flag

    @staticmethod
    def get_possible_capture(index_x, index_y,chess_board):
        capture_action = []

        candidate_point = [[index_x + 1, index_y - 1], [index_x + 1, index_y + 1], [index_x - 1, index_y - 1], [index_x - 1, index_y + 1]]
        for point in candidate_point:
            if 0 <= point[0] <= 10 and 0 <= point[1] <= 10:
                if chess_board[point[0]][point[1]] !=0:
                    if chess_board[point[0]][point[1]] + chess_board[index_x][index_y] == 3 or (chess_board[point[0]][point[1]] + chess_board[index_x][index_y] == 4 and chess_board[point[0]][point[1]] != chess_board[index_x][index_y]):
                        capture_action.append(point)

        return capture_action

    #get the possible move of x,y
    @staticmethod
    def get_possible_move(index_x, index_y, chess_board):
        move_action = []

        move_x_r = index_x + 1
        move_x_l = index_x - 1
        while move_x_r < 11 or move_x_l > -1:
            if move_x_r < 11:
                if chess_board[move_x_r][index_y] == 0:
                    move_action.append([move_x_r,index_y])
                    move_x_r = move_x_r + 1
                else:
                    move_x_r = 11

            if move_x_l > -1:
                if chess_board[move_x_l][index_y] == 0:
                    move_action.append([move_x_l, index_y])
                    move_x_l = move_x_l - 1
                else:
                    move_x_l = -1

        move_y_r = index_y + 1
        move_y_l = index_y - 1
        while move_y_r < 11 or move_y_l > -1:
            if move_y_r < 11:
                if chess_board[index_x][move_y_r] == 0:
                    move_action.append([index_x, move_y_r])
                    move_y_r = move_y_r + 1
                else:
                    move_y_r = 11

            if move_y_l > -1:
                if chess_board[index_x][move_y_l] == 0:
                    move_action.append([index_x, move_y_l])
                    move_y_l = move_y_l - 1
                else:
                    move_y_l = -1

        return move_action

    @staticmethod
    def is_flagship_captured(chessboard):
        max_ship = chessboard.max()
        if max_ship < 3:
            return True
        else:
            return False

    @staticmethod
    def is_flagship_escaped(chessboard):
        flagship_index = np.squeeze(np.argwhere(chessboard == 3))
        if flagship_index is None or len(flagship_index) == 0:
            return False
        if flagship_index[0] == 0 or flagship_index[1] == 0 or flagship_index[0] == 10 or flagship_index[1] == 10:
            return True
        else:
            return False

    @staticmethod
    def ship_remaining(chessboard):
        SliverCount = len(np.argwhere(chessboard == 1))
        GoldenCount = len(np.argwhere(chessboard == 2)) + 1
        return SliverCount, GoldenCount

    @staticmethod
    def is_flagship_blocked(chessboard):
        flagship_index = np.squeeze(np.argwhere(chessboard == 3))
        if flagship_index is None or len(flagship_index) == 0:
            return True, 0
        possible_move = BDInterface.get_possible_move(flagship_index[0], flagship_index[1], chessboard)
        for moves in possible_move:
            if moves[0] == 0 or moves[0] == 10 or moves[1] == 0 or moves[1] == 10:
                return False, len(possible_move)
        return True, len(possible_move)

    @staticmethod
    def is_SliverWellArraied(chessboard):
        linked_amount = 0
        flagship_index = np.squeeze(np.argwhere(chessboard == 3))
        if flagship_index is None or len(flagship_index) == 0:
            return  0
        SliverShips = np.argwhere(chessboard == 1).tolist()
        F_possible_move = BDInterface.get_possible_move(flagship_index[0], flagship_index[1], chessboard)
        for Ship in SliverShips:
            S_possible_move = BDInterface.get_possible_move(Ship[0], Ship[1], chessboard)
            intersection = [j for j in F_possible_move if j in S_possible_move]
            linked_amount = linked_amount + len(intersection)
        return linked_amount

    @staticmethod
    def pre_capture(chessboard):
        Value = 0
        try:
            flagship_index = np.squeeze(np.argwhere(chessboard == 3))
            if flagship_index is None or len(flagship_index) == 0:
                return 0
            IterateShips = np.argwhere(chessboard == 1)
            goldenship_index = np.argwhere(chessboard == 2)
            for SShip in IterateShips:
                Arounding = [[SShip[0] + 1, SShip[1] - 1], [SShip[0] + 1, SShip[1] + 1], [SShip[0] - 1, SShip[1] - 1], [SShip[0] - 1, SShip[1] + 1]]
                if flagship_index.tolist() in Arounding:
                    Value = Value + 5#0.05 #5
                    for SShip2 in IterateShips:
                        if SShip2.tolist() in Arounding:
                            Value = Value + 30#0.3#30
                    for goldenship in goldenship_index:
                        if goldenship.tolist() in Arounding:
                            Value = Value - 10#0.1#10
        except Exception:
            print(flagship_index)
        return Value

    @staticmethod
    def is_sliverfeed(chessboard):
        arounding = 0
        Slivership_index = np.argwhere(chessboard == 1)
        goldenship_index = np.argwhere(chessboard == 2)
        for SShip in Slivership_index:
            Arounding = [[SShip[0] + 1, SShip[1] - 1], [SShip[0] + 1, SShip[1] + 1], [SShip[0] - 1, SShip[1] - 1], [SShip[0] - 1, SShip[1] + 1]]
            for Gship in goldenship_index:
                if Gship.tolist() in Arounding:
                    arounding = arounding - 1
                    for SShip2 in Slivership_index:
                        if SShip2.tolist() in Arounding:
                            arounding = arounding + 1
        return arounding


    @staticmethod
    def flagship_indanger(chessboard):
        SShip = np.squeeze(np.argwhere(chessboard == 3))
        if SShip is None or len(SShip) != 2:
            return False
        Arounding = [[SShip[0] + 1, SShip[1] - 1], [SShip[0] + 1, SShip[1] + 1], [SShip[0] - 1, SShip[1] - 1],
                     [SShip[0] - 1, SShip[1] + 1]]
        Slivership_index = np.squeeze(np.argwhere(chessboard == 1))
        if len(Slivership_index) == 0:
            return False
        for Sliver in Slivership_index:
            if Sliver.tolist() in Arounding:
                return True
        return False


    @staticmethod
    def is_ally_blocked(chessboard):
        value_counter = 0
        ally_counter = 0
        flagship_index = np.squeeze(np.argwhere(chessboard == 3))
        if len(flagship_index) == 0:
            return 0
        if flagship_index[0] >= 10 or flagship_index[1] >= 10:
            return 0
        for x in range(0,flagship_index[0]):
            ally_counter = ally_counter + chessboard[x][flagship_index[1]]
        if ally_counter == 2:
            value_counter = value_counter + 1

        ally_counter = 0
        for x in range(flagship_index[0] + 1, 11):
            ally_counter = ally_counter + chessboard[x][flagship_index[1]]
        if ally_counter == 2:
            value_counter = value_counter + 1

        ally_counter = 0
        for y in range(0,flagship_index[1]):
                ally_counter = ally_counter + chessboard[flagship_index[0]][y]
        if ally_counter == 2:
            value_counter = value_counter + 1

        ally_counter = 0
        for y in range(flagship_index[1]+1, 11):
                ally_counter = ally_counter + chessboard[flagship_index[0]][y]
        if ally_counter == 2:
            value_counter = value_counter + 1
        return value_counter







