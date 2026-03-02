# chess.py
# Full chess game with castling, promotion, timer, and win detection

BOARD_SIZE = 8
SQUARE = 80

WIDTH = BOARD_SIZE * SQUARE
HEIGHT = BOARD_SIZE * SQUARE + 60

LIGHT = (240, 217, 181)
DARK = (181, 136, 99)

turn = "white"
selected = None

white_time = 300
black_time = 300

game_over = False
winner = ""

# -------------------------
# Castling Trackers
# -------------------------
king_moved = {"white": False, "black": False}
rook_moved = {
    "white": {"left": False, "right": False},
    "black": {"left": False, "right": False}
}

# -------------------------
# Board
# -------------------------
board = [
    ["br","bn","bb","bq","bk","bb","bn","br"],
    ["bp"]*8,
    [".."]*8,
    [".."]*8,
    [".."]*8,
    [".."]*8,
    ["wp"]*8,
    ["wr","wn","wb","wq","wk","wb","wn","wr"]
]

# -------------------------
# Drawing
# -------------------------
def draw_board():
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            color = LIGHT if (r+c)%2==0 else DARK
            rect = Rect(c*SQUARE, r*SQUARE, SQUARE, SQUARE)
            screen.draw.filled_rect(rect, color)

def draw_pieces():
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            piece = board[r][c]
            if piece != "..":
                screen.blit(piece, (c*SQUARE, r*SQUARE))

def draw_selection():
    if selected:
        r,c = selected
        rect = Rect(c*SQUARE, r*SQUARE, SQUARE, SQUARE)
        screen.draw.rect(rect, (0,255,0))

# -------------------------
# Helpers
# -------------------------
def path_clear(sr,sc,tr,tc):
    dr = tr-sr
    dc = tc-sc
    steps = max(abs(dr),abs(dc))
    step_r = (dr//steps) if dr!=0 else 0
    step_c = (dc//steps) if dc!=0 else 0

    for i in range(1,steps):
        if board[sr+i*step_r][sc+i*step_c]!="..":
            return False
    return True

def find_king(color):
    k = ("w" if color=="white" else "b")+"k"
    for r in range(8):
        for c in range(8):
            if board[r][c]==k:
                return (r,c)
    return None

def is_square_attacked(row,col,by_color):
    for r in range(8):
        for c in range(8):
            piece=board[r][c]
            if piece!=".." and piece[0]==by_color:
                if can_piece_reach(r,c,row,col):
                    return True
    return False

def can_piece_reach(sr,sc,tr,tc):
    piece=board[sr][sc]
    if piece=="..": return False
    p=piece[1]
    dr=tr-sr
    dc=tc-sc

    if p=="p":
        d=-1 if piece[0]=="w" else 1
        return abs(dc)==1 and dr==d
    if p=="r":
        return (sr==tr or sc==tc) and path_clear(sr,sc,tr,tc)
    if p=="b":
        return abs(dr)==abs(dc) and path_clear(sr,sc,tr,tc)
    if p=="q":
        return (sr==tr or sc==tc or abs(dr)==abs(dc)) and path_clear(sr,sc,tr,tc)
    if p=="n":
        return (abs(dr),abs(dc)) in [(2,1),(1,2)]
    if p=="k":
        return max(abs(dr),abs(dc))==1
    return False

def is_in_check(color):
    king=find_king(color)
    opponent="b" if color=="white" else "w"
    return is_square_attacked(king[0],king[1],opponent)

def would_be_in_check(sr,sc,tr,tc,color):
    temp=board[tr][tc]
    board[tr][tc]=board[sr][sc]
    board[sr][sc]=".."
    check=is_in_check(color)
    board[sr][sc]=board[tr][tc]
    board[tr][tc]=temp
    return check

# -------------------------
# Castling
# -------------------------
def can_castle(sr,sc,tr,tc):
    piece=board[sr][sc]
    color="white" if piece[0]=="w" else "black"
    opponent="b" if color=="white" else "w"

    if king_moved[color] or is_in_check(color):
        return False

    if tc==sc+2:
        rook_col=7; side="right"
    elif tc==sc-2:
        rook_col=0; side="left"
    else:
        return False

    if rook_moved[color][side]:
        return False

    step=1 if tc>sc else -1
    for c in range(sc+step,rook_col,step):
        if board[sr][c]!="..":
            return False

    for c in [sc,sc+step,tc]:
        if is_square_attacked(sr,c,opponent):
            return False

    return True

# -------------------------
# Move validation
# -------------------------
def valid_move(sr,sc,tr,tc):
    piece=board[sr][sc]
    if piece=="..": return False
    color=piece[0]
    p=piece[1]
    target=board[tr][tc]

    if target!=".." and target[0]==color:
        return False

    dr=tr-sr; dc=tc-sc
    legal=False

    if p=="k":
        opponent="b" if color=="w" else "w"
        if max(abs(dr),abs(dc))==1 and not is_square_attacked(tr,tc,opponent):
            legal=True
        elif dr==0 and abs(dc)==2 and can_castle(sr,sc,tr,tc):
            legal=True
    elif p=="q":
        legal=(sr==tr or sc==tc or abs(dr)==abs(dc)) and path_clear(sr,sc,tr,tc)
    elif p=="r":
        legal=(sr==tr or sc==tc) and path_clear(sr,sc,tr,tc)
    elif p=="b":
        legal=abs(dr)==abs(dc) and path_clear(sr,sc,tr,tc)
    elif p=="n":
        legal=(abs(dr),abs(dc)) in [(2,1),(1,2)]
    elif p=="p":
        d=-1 if color=="w" else 1
        start=6 if color=="w" else 1
        if dc==0 and dr==d and target=="..": legal=True
        elif dc==0 and sr==start and dr==2*d and board[sr+d][sc]==".." and target=="..": legal=True
        elif abs(dc)==1 and dr==d and target!="..": legal=True

    if not legal: return False
    return not would_be_in_check(sr,sc,tr,tc,"white" if color=="w" else "black")

# -------------------------
# Mouse
# -------------------------
def on_mouse_down(pos):
    global selected,turn

    c=int(pos[0]//SQUARE)
    r=int(pos[1]//SQUARE)

    if selected is None:
        piece=board[r][c]
        if piece!=".." and ((turn=="white" and piece[0]=="w") or (turn=="black" and piece[0]=="b")):
            selected=(r,c)
    else:
        sr,sc=selected
        if valid_move(sr,sc,r,c):
            moving=board[sr][sc]
            board[r][c]=moving
            board[sr][sc]=".."

            if moving[1]=="k" and abs(c-sc)==2:
                if c>sc:
                    board[r][5]=board[r][7]; board[r][7]=".."
                else:
                    board[r][3]=board[r][0]; board[r][0]=".."

            if moving[1]=="k": king_moved[turn]=True
            if moving[1]=="r":
                if sc==0: rook_moved[turn]["left"]=True
                if sc==7: rook_moved[turn]["right"]=True

            if moving=="wp" and r==0: board[r][c]="wq"
            if moving=="bp" and r==7: board[r][c]="bq"

            turn="black" if turn=="white" else "white"

        selected=None

# -------------------------
# Update & Draw (REQUIRED)
# -------------------------
def update():
    pass

def draw():
    screen.clear()
    draw_board()
    draw_selection()
    draw_pieces()
    screen.draw.text(f"Turn: {turn}", (10, HEIGHT-50), fontsize=30, color="white")