import numpy as np


def validate(question,bool_fxn=lambda i,args:i=='y' or i=='n',cast=[str],error_message="Please enter valid input.",*args):
    if not isinstance(cast,tuple) and cast != [str]:
        cast = [cast]
    ans = input(question + "\n")
    while not bool_fxn(ans, args):
        ans = input(error_message + "\n")
    for i in np.arange(len(cast)):
        try:
            return cast[i](ans)
        except ValueError:
            pass
        
def check_decimal(lr,*args):
    try:
        int(lr)
        return True
    except ValueError:
        pass
    try:
        float(lr)
        return True
    except ValueError:
        pass
    return False

def check_infinity(n,*args):
    return n == "infinity"

def check_posdecimal_finite(lr,*args):
    return check_decimal(lr) and float(lr) > 0

def check_nonnegdecimal_finite(lr,*args):
    return check_decimal(lr) and float(lr) >= 0

def check_posdecimal(lr,*args):
    return check_infinity(lr) or check_posdecimal_finite(lr)

def check_nonnegdecimal(lr,*args):
    return check_infinity(lr) or check_nonnegdecimal_finite(lr)

def check_int(n,*args):
    try:
        return isinstance(int(n),int)
    except ValueError:
        return False
        
def check_posint_finite(n,*args):
    return check_int(n) and int(n) > 0

def check_posint(n,*args):
    return check_infinity(n) or check_posint_finite(n)

def check_nonnegint_finite(n,*args):
    return check_int(n) and int(n) >= 0

def check_nonnegint(n,*args):
    return check_nonnegint_finite(n) or check_infinity(n)
