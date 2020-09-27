from .models import UserGame
import secrets
from django.db.models import Q


def check_valid_move(col_no,user_obj):
    global data
    ROW = r = 6
    COL = c = 7
    num1 = 1
    num2 = 2
    arr= user_obj.matrix1
    flag1=user_obj.flag
    user1_move = user_obj.user1_move
    user2_move = user_obj.user2_move

    for i in range(r-1, -2, -1):

        if arr[i][col_no] == 0 and i >= 0 and col_no !=COL:
            data = "Valid Move"
            arr[i][COL] += 1
            arr[ROW][col_no]+=1
            if flag1:
                arr[i][col_no] = num1
                user1_move.append(col_no+1)
                if arr[i][COL] >= 4:
                    user_obj.game_over = check_winner_horizontal(user_obj.matrix1, num1, i)
                elif arr[ROW][col_no]>=4 and col_no>2:
                    user_obj.game_over = check_winner_vertical(user_obj.matrix1,num1,i,col_no) or \
                                check_winner_right_diagonal(user_obj.matrix1,num1,i,col_no)
                elif arr[ROW][col_no]>=4 and col_no<4:
                    user_obj.game_over = check_winner_vertical(user_obj.matrix1, num1, i, col_no) or \
                                check_winner_left_diagonal(user_obj.matrix1,num1,i,col_no)
            else:
                arr[i][col_no] = num2
                user2_move.append(col_no+1)
                if arr[i][COL] >= 4:
                    user_obj.game_over = check_winner_horizontal(user_obj.matrix1, num2, i)
                elif arr[ROW][col_no] >= 4 and col_no > 2:
                    user_obj.game_over = check_winner_vertical(user_obj.matrix1, num2, i, col_no) or \
                                check_winner_right_diagonal(user_obj.matrix1, num2, i, col_no)
                elif arr[ROW][col_no] >= 4 and col_no < 4:
                    user_obj.game_over = check_winner_vertical(user_obj.matrix1, num2, i, col_no) or \
                                check_winner_left_diagonal(user_obj.matrix1, num2, i, col_no)
            break
        else:
            data = "Invalid Move"

    for j in arr:
        print(j)
    print("user1 move ",user1_move)
    print("user2 move ", user2_move)
    return arr


def check_winner_horizontal(game,num,rw):
    global data
    c = 7
    num1 = 1
    num2 = 2
    i = rw
    for j in range(0,c-2):
        if (game[i][j]== num) and (game[i][j+1]== num) and (game[i][j+2]== num) and (game[i][j+3]== num):
            if num == num1:
                data = "Yellow wins"
                return True
            elif num == num2:
                data = "Red wins"
                return True
    return False


def check_winner_vertical(game, num,rw,cl):
    global data
    num1 = 1
    num2 = 2
    i=rw
    j = cl
    if (game[i][j] == num) and (game[i + 1][j] == num) and (game[i + 2][j] == num) and (game[i + 3][j] == num):
        if num == num1:
            data = "Yellow wins"
            return True
        elif num == num2:
            data = "Red wins"
            return True
    return False


def check_winner_right_diagonal(game, num,rw,cl):
    global data
    ROW = r = 6
    c = 7

    num1 = 1
    num2 = 2
    val=rw+cl
    if val<=ROW-1:
        rw = val
        cl = 0
    else:
        rw = ROW
        cl = val-ROW
    for i in range(rw,r-4,-1):
        for j in range(cl,c-3):
                if (game[i][j]== num) and (game[i-1][j+1]== num) and (game[i-2][j+2]== num) and (game[i-3][j+3]== num):
                    if num == num1:
                        data = "Yellow wins"
                        return True
                    elif num == num2:
                        data = "Red wins"
                        return True
    return False


def check_winner_left_diagonal(game, num,rw,cl):
    global data
    ROW = r = 6
    COL = c = 7

    num1 = 1
    num2 = 2
    vc=(COL-1)-cl
    val = rw+vc
    if val<COL-1:
        rw = rw+vc
        cl = cl+vc
    else:
        val = ROW-1-rw
        rw = rw+val
        cl = cl+val

    for i in range(rw,r-4,-1):
        for j in range(cl,c-1):
            if (game[i][j] == num) and (game[i - 1][j - 1] == num) and (game[i - 2][j - 2] == num) and \
                    (game[i - 3][j - 3] == num):
                if num == num1:
                    data = "Yellow wins"
                    return True
                elif num == num2:
                    data = "Red wins"
                    return True
    return False


def game(request):
    success = False
    msg = "Operation Failed"
    global data
    data = "Invalid Operation"
    try:
        # import pdb
        # pdb.set_trace()
        COL = c = 7

        post_data = request.POST
        request_data = post_data.get('request',None)
        user1_token = post_data.get('user1 token',None)
        user2_token = post_data.get('user2 token',None)

        if request_data == 'START':
            user_game = UserGame(matrix1 =[[0] * 8 for i in range(7)])
            user_game.user1_move = []
            user_game.user2_move = []
            user_game.user1_token = secrets.token_hex(5)
            user_game.user2_token = secrets.token_hex(5)
            val = {"User1 Token": user_game.user1_token,
                   "User2 Token": user_game.user2_token
                   }
            user_game.save()
            data = val
        elif user1_token and user2_token:
            user_game = UserGame.objects.get(user1_token =user1_token,user2_token=user2_token,game_over='False')
            cn = int(request_data)
            col_num = cn - 1
            if user_game.matrix1[0][COL] == 7 or col_num > 6 or col_num < 0:
                data = "INVALID MOVE"
            else:
                if user_game.flag:
                    user_game.matrix1 = check_valid_move(col_num, user_game)
                    user_game.flag = False
                    user_game.save()
                else:
                    user_game.matrix1 = check_valid_move(col_num, user_game)
                    user_game.flag = True
                    user_game.save()

        success = True
        msg = "Operation Successful"
    except Exception as e:
        print(e.args)
    return {'success' : success, 'msg' : msg, 'data':data}

def game_get_moves(request):
    success = False
    msg = "Operation Failed"
    data = "Invalid Operation"
    try:
        get_data = request.GET
        request_data = get_data.get('userToken',None)
        if request_data:
            user_data = UserGame.objects.filter(Q(user1_token=request_data)|Q(user2_token=request_data)).\
                values('user1_move','user2_move','user1_token','user2_token')
            if request_data == user_data[0]['user1_token']:
               data = {"user1 moves ":user_data[0]['user1_move']}
            elif request_data == user_data[0]['user2_token']:
               data = {"user2 moves ":user_data[0]['user2_move']}
        success = 'Success'
        msg = "Operation Successful"

    except Exception as e:
        print(e.args)
    return {'success' : success, 'msg' : msg, 'data':data}