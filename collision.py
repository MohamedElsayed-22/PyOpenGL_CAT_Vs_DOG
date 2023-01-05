
# CHECKING COLLISION
def check_collision():
    global CAT_RESULT
    global DOG_RESULT
    global shot, x, y, theta, force, time, CURRENT_TURN, msgTime, msgText

    # Dog Points
    # If the Dog hit the cat
    if CURRENT_TURN == "DOG" and ball.bottom <= CAT.top:
        if CAT.right >= ball.left >= CAT.left:
            ## Print message
            msgTime = 200

            ## Dec result
            CAT_RESULT -= 1

            ## stop and begin the cat's turn
            shot = False
            ball.start("CAT")
            CURRENT_TURN = "CAT"

    # Cat Points
    # If the Dog hit the cat
    if CURRENT_TURN == "CAT" and ball.bottom <= DOG.top:
        if DOG.right >= ball.right >= DOG.left:
            ## Print message
            msgTime = 200

            ## Dec result
            DOG_RESULT -= 1

            ## stop and begin the DOG's turn
            shot = False
            ball.start("DOG")
            CURRENT_TURN = "DOG"