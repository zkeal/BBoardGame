# coding=utf-8
import numpy as np
from BoardInterface import BDInterface

class ChessPlayer:
    def __init__(self, Flag):
        self.flag = Flag # 1= sliver 2 = golden
        #self.sliver_parameters = [300, 300, 50, 30, 10, 1, 5]
        self.sliver_parameters = [1.        , 1.        , 0.1638796 , 0.09698997, 0.03010033,
       0.        , 0.01337793]
        #self.golden_parameters = [300, 300, 100, 50, 30, 10, 5]
        self.golden_parameters = [1.        , 1.        , 0.3220339 , 0.15254237, 0.08474576,
       0.01694915, 0.00333471]

    def set_sliverParameters(self, np_array):
        self.sliver_parameters = (np.squeeze(np_array.T)).tolist()

    def set_goldenParameters(self, np_array):
        self.golden_parameters = (np.squeeze(np_array.T)).tolist()

    def sliver_decision(self, chess_board):
        move_result,capture_result = self.sliver_possible_action(chess_board)
        final_action = None
        final_value = -1000000
        for action in move_result:
            value = self.sliver_evaluate_value(action[1])
            if value > final_value:
                final_action = action
                final_value = value
        for action in capture_result:
            value = self.sliver_evaluate_value(action[1])
            if value > final_value:
                final_action = action
                final_value = value
        print("Final value : " + str(final_value))
        return final_action


    def golden_decision(self, chess_board):
        golden_mov,golden_capture, flag_move, flag_capture = self.golden_possible_action(chess_board)
        final_action = None
        final_value = 100000000000
        for action in golden_mov:
            value = self.golden_evaluate_value(action[1])
            if value < final_value:
                final_action = action
                final_value = value
        for action in golden_capture:
            value = self.golden_evaluate_value(action[1])
            if value < final_value:
                final_action = action
                final_value = value
        for action in flag_move:
            value = self.golden_evaluate_value(action[1])
            if value < final_value:
                final_action = action
                final_value = value
        for action in flag_capture:
            value = self.golden_evaluate_value(action[1])
            if value < final_value:
                final_action = action
                final_value = value
        print("Final value : " + str(final_value))
        return final_action

    @staticmethod
    def golden_evaluate_value(chess_board, player): #end_turn_counter
        estimate_value = 0
        if BDInterface.flagship_indanger(chess_board):
            estimate_value = estimate_value + 90000000
        if BDInterface.is_flagship_escaped(chess_board):
            estimate_value = estimate_value - 99999999
        SliverCount, GoldenCount = BDInterface.ship_remaining(chess_board)
        estimate_value = estimate_value + SliverCount * player.golden_parameters[0] #0.1
        estimate_value = estimate_value - GoldenCount * player.golden_parameters[1] #0.1
        bloacked, move_oppor = BDInterface.is_flagship_blocked(chess_board)
        if bloacked:
            estimate_value = estimate_value + player.golden_parameters[2]# 0.6
        estimate_value = estimate_value - move_oppor * player.golden_parameters[3]#0.02
        estimate_value = estimate_value + player.golden_parameters[4] * BDInterface.is_sliverfeed(chess_board)#0.01
        estimate_value = estimate_value + BDInterface.pre_capture(chess_board) * player.golden_parameters[5] #0.1
        estimate_value = estimate_value + float(BDInterface.is_SliverWellArraied(chess_board))/300
        estimate_value = estimate_value - BDInterface.is_ally_blocked(chess_board) * player.golden_parameters[6]
        return estimate_value

    @staticmethod
    def sliver_evaluate_value(chess_board, player):
        estimate_value = 0
        if BDInterface.is_flagship_captured(chess_board):
            estimate_value = estimate_value + 99999999
        SliverCount, GoldenCount = BDInterface.ship_remaining(chess_board)
        estimate_value = estimate_value + SliverCount * player.sliver_parameters[0]
        estimate_value = estimate_value - GoldenCount * player.sliver_parameters[1]
        bloacked, move_oppor = BDInterface.is_flagship_blocked(chess_board)
        if not bloacked:
            estimate_value = estimate_value - 99999999
        estimate_value = estimate_value - move_oppor * player.sliver_parameters[2]
        estimate_value = estimate_value + player.sliver_parameters[3] * BDInterface.is_sliverfeed(chess_board)
        estimate_value = estimate_value + BDInterface.pre_capture(chess_board) * player.sliver_parameters[4]
        estimate_value = estimate_value + BDInterface.is_SliverWellArraied(chess_board) * player.sliver_parameters[5]
        estimate_value = estimate_value - BDInterface.is_ally_blocked(chess_board) * player.sliver_parameters[6]
        return estimate_value

    def sliver_possible_action(self, chess_board):
        move_result= []
        self.search_possible_move(move_result, chess_board, self.flag, 2)
        capture_result = []
        self.search_possible_capture(capture_result, chess_board, self.flag)
        return move_result,capture_result

    def golden_possible_action(self, chess_board):
        golden_mov = []
        self.search_possible_move(golden_mov, chess_board, self.flag, 2)
        golden_capture = []
        self.search_possible_capture(golden_capture, chess_board, self.flag)
        flag_move = []
        self.search_possible_move(flag_move, chess_board, 3, 1)
        flag_capture = []
        self.search_possible_capture(flag_capture, chess_board, 3)

        return golden_mov,golden_capture, flag_move, flag_capture

    def search_possible_capture(self, result_board, chess_board, flag):
        availble_chess = np.argwhere(chess_board == flag)
        if len(availble_chess) != 0:
            for per_chess in availble_chess:
                Capture_r1 = BDInterface.get_possible_capture(per_chess[0], per_chess[1], chess_board)
                for cap in Capture_r1:
                    temp_chess_board=chess_board.copy()
                    temp_chess_board[cap[0]][cap[1]] = chess_board[per_chess[0]][per_chess[1]]
                    temp_chess_board[per_chess[0]][per_chess[1]] = 0
                    transition_str =  self.str_coordinate(per_chess) + " to " + self.str_coordinate(
                        cap) + ","
                    result_board.append((transition_str,temp_chess_board))


    def move_array(self, big_a, small_a):
        result = []
        for tem in big_a:
            if tem == small_a:
                continue
            else:
                result.append(tem)
        return result


    def search_possible_move(self,result_board, t_chess_board, flag,depth = 2, used_point = None, oritran_str = "",unique_board = None): # move twice
        depth = depth - 1
        #if flag == 1:
        if len(t_chess_board) == 2:
            chess_board = t_chess_board[1]
            oritran_str = t_chess_board[0]
        else:
            chess_board = t_chess_board
        if unique_board is None:
            unique_board = []
        availble_chess = np.argwhere(chess_board == flag).tolist()# 1 sliver 2,3 golden
        if depth == 0 and used_point is not None and used_point in availble_chess:
            availble_chess = self.move_array(availble_chess, used_point)
        if availble_chess is not None and len(availble_chess) != 0:
            # round 1-move
            possible_board_r1 = [] # tuple (describe, board)
            for per_chess in availble_chess:
                Move_r1 = BDInterface.get_possible_move(per_chess[0], per_chess[1], chess_board)
                for move in Move_r1:
                    temp_chess_board=chess_board.copy()
                    temp_chess_board[move[0]][move[1]] = chess_board[per_chess[0]][per_chess[1]]
                    temp_chess_board[per_chess[0]][per_chess[1]] = 0
                    transition_str = oritran_str + self.str_coordinate(per_chess) +" to "+ self.str_coordinate(move)+","
                    #possible_board_r1.append((transition_str, temp_chess_board))
                    if depth == 0:
                        hash_board = hash(str(temp_chess_board))
                        if hash_board not in unique_board:
                            result_board.append((transition_str, temp_chess_board))
                            unique_board.append(hash_board)
                    else:
                        self.search_possible_move(result_board, temp_chess_board, flag, depth, move, transition_str, unique_board)

    @staticmethod
    def str_coordinate(chesss_point):
        str_buffer=""
        x = chesss_point[0]
        if x == 0:
            str_buffer = str_buffer + "A"
        if x == 1:
            str_buffer = str_buffer + "B"
        if x == 2:
            str_buffer = str_buffer + "C"
        if x == 3:
            str_buffer = str_buffer + "D"
        if x == 4:
            str_buffer = str_buffer + "E"
        if x == 5:
            str_buffer = str_buffer + "F"
        if x == 6:
            str_buffer = str_buffer + "G"
        if x == 7:
            str_buffer = str_buffer + "H"
        if x == 8:
            str_buffer = str_buffer + "I"
        if x == 9:
            str_buffer = str_buffer + "J"
        if x == 10:
            str_buffer = str_buffer + "K"
        str_buffer = str_buffer + str(11 - chesss_point[1])
        return str_buffer


