# coding=utf-8
import numpy as np
from Cplayer import ChessPlayer

def get_TT(chessboard,set):
    flagship_index = np.squeeze(np.argwhere(chessboard == 3))
    if flagship_index is None or len(flagship_index) == 0:
        return None
    if 3<=flagship_index[0]<=7 and 3<=flagship_index[1]<=7:
        TT = np.array(chessboard[flagship_index[0]-3:flagship_index[0]+4][flagship_index[1]-3:flagship_index[1]+4])
        key = hash(str(TT))
        set[key] = TT


def ABsearch(Str_act, CurrentBoard, ActiveFlag, depth, player,   purning_score = None):
    if ActiveFlag == 0: # maxmize plaer now, sliver
        if depth <= 0: #  should ues golden value, its contradict
            return ChessPlayer.golden_evaluate_value(CurrentBoard,player), Str_act, Str_act,CurrentBoard
        else:
            max = float("-inf")
            max_board = None
            max_actstr=''
            move_result, capture_result = player.sliver_possible_action(CurrentBoard)
            #possible_action = move_result.extend(capture_result)
            possible_action = move_result + capture_result

            if possible_action is None:
                raise Exception("possible_action is None")
            #self.Children = possible_action
            for action in possible_action:
                # time0 = datetime.datetime.now()
                actr_record = Str_act + ", " + action[0] + ";"
                next_flayer, Str_act1, str_record, action_board  = ABsearch(actr_record, action[1],  int(not ActiveFlag), depth - 1, player, max)
                if purning_score is not None and purning_score < next_flayer:
                    return next_flayer, Str_act1,str_record, action_board

                if next_flayer > max:
                    max = next_flayer
                    max_board = action[1]
                    max_actstr = str_record
                    Str_act = action[0]
                #time1 = datetime.datetime.now()
                # interval = (time1 - time0).total_seconds()  # 如果时间差在1秒内，.seconds方法得出的结果为0
                # print(interval)
            return max, Str_act, max_actstr, max_board
    if ActiveFlag == 1: # golden minmize player
        if depth <= 0:
            return ChessPlayer.sliver_evaluate_value(CurrentBoard,player), Str_act, Str_act, CurrentBoard
        else:
            min = float("inf")
            min_board = None
            min_actstr = ''
            golden_mov,golden_capture, flag_move, flag_capture = player.golden_possible_action(CurrentBoard)
            possible_action = golden_mov + golden_capture + flag_move + flag_capture
            for action in possible_action:
                acstr_record ="depth:"+str(depth) + Str_act + ", " + action[0] + ";"
                next_flayer, Str_act1, str_record, action_board = ABsearch(acstr_record, action[1],
                                                                            int(not ActiveFlag), depth - 1, player,min)
                if purning_score is not None and purning_score > next_flayer:
                    return next_flayer, Str_act1,str_record, action_board

                if next_flayer < min:
                    min = next_flayer
                    min_board = action[1]
                    min_actstr = str_record
                    Str_act = action[0]
            return min, Str_act, min_actstr, min_board














