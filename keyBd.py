# キー入力読み取り
#
import keyboard

UP     = "up"
DOWN   = "down"
SLUSH  = "/"
ATMK   = "@"
BKSPC  = "backspace"
ENTER  = "enter"
ESCAPE = "esc"
NUM    = ("0","1","2","3","4","5","6","7","8","9")
Nothing= "Nothing"
        
class getKey:
    
    def __init__(self):
        pass
        
    def val(self):
        xx=keyboard.read_key()
        if keyboard.is_pressed(UP):
            return(UP)
        elif keyboard.is_pressed(DOWN):
            return(DOWN)
        elif keyboard.is_pressed(SLUSH):
            return(SLUSH)
        elif keyboard.is_pressed(ATMK):
            return(ATMK)
        elif keyboard.is_pressed(BKSPC):
            return(BKSPC)
        elif keyboard.is_pressed(ENTER):
            return(ENTER)
        elif keyboard.is_pressed(ESCAPE):
            return(ESCAPE)
        else:
            for key in NUM:
                if keyboard.is_pressed(key):
                    return(key)
        return(Nothing)
    
if __name__ == '__main__':
    kk=getKey()
    while True:
        key=kk.val()
        print(key)
        if key==ESCAPE:
            break
        
        