from z3 import *

def unique(s, xs):
    m = s.model()
    for x in xs:
        s.push()
        s.add(x != m.eval(x, model_completion=True))
        if s.check() == sat:
            return False
        s.pop()
    return True

def trial1():
    r1, r2 = Bools("r1 r2")
    # ri True means there is a lady in room i
    # ri False --> tiger!

    sign1 = r1 & ~r2
    sign2 = r1 != r2

    s = Solver()

    s.add(sign1 != sign2)

    return s
    
def trial2():
    r1, r2 = Bools("r1 r2")
    # ri True means there is a lady in room i
    # ri False --> tiger!

    sign1 = r1 | r2
    sign2 = ~r1

    cond  = sign1 == sign2

    s = Solver()
    s.add(cond)

    return s

def trial3():
    r1, r2 = Bools("r1 r2")  # r1 for Room I, r2 for Room II

    # Sign I: Either a tiger in Room I or a lady in Room II
    sign1 = Or(Not(r1), r2) 

    # Sign II: A lady is in Room II
    sign2 = r2

    # Both signs are either both true or both false
    signs_same = sign1 == sign2

    s = Solver()
    s.add(signs_same)

    return s

def trial4():
    r1, r2 = Bools("r1 r2")
    # ri True means there is a lady in room i
    # ri False --> tiger!

    sign1 = r1 & r2
    sign2 = sign1

    cond1 = r1 == sign1
    cond2 = r2 != sign2

    s = Solver()
    s.add(cond1, cond2)

    return s

def trial5():
    r1, r2 = Bools("r1 r2")  # r1 and r2 represent rooms 1 and 2

    # Sign 1: At least one room contains a lady
    sign1 = r1 | r2

    # Sign 2: The other room contains a lady
    sign2 = Implies(r1, r2) & Implies(r2, r1)

    # Adding conditions: Both signs cannot be false
    s = Solver()
    s.add(sign1, sign2)

    return s

def trial6():
    r1, r2 = Bools("r1 r2")  # r1 and r2 represent rooms 1 and 2

    # Sign 1: It makes no difference which room you pick
    sign1 = r1 == r2

    # Sign 2: There is a lady in the other room
    sign2 = Implies(r1, r2) & Implies(r2, r1)

    s = Solver()
    s.add(sign1 != sign2)

    return s

def trial7():
    r1, r2 = Bools("r1 r2")  # r1 and r2 represent rooms 1 and 2

    # Sign 1: It does make a difference which room you pick
    sign1 = r1 != r2

    # Sign 2: You are better off choosing the other room
    sign2 = Implies(r1, Not(r2)) & Implies(r2, Not(r1))

    s = Solver()
    s.add(sign1, sign2)

    return s



def trial8():
    r1, r2 = Bools("r1 r2")
    # ri True means there is a lady in room i
    # ri False --> tiger!

    sign2 = ~r2
    sign1 = ~r1 & ~r2

    cond1 = r1 == sign1
    cond2 = r2 != sign2

    s = Solver()
    s.add(cond1, cond2)

    return s



def trial9():
    r1, r2, r3 = Bools("r1 r2 r3")
    # ri True means there is a lady in room i
    # ri False --> tiger!
    # one_lady = (r1 & ~r2 & ~r3) | (~r1 & r2 & ~r3) | (~r1 & ~r2 & r3)
    one_lady = Sum([If(r, 1, 0) for r in [r1, r2, r3]]) == 1
    
    sign1 = ~r1
    sign2 = r2
    sign3 = ~r2

    # one_sign = (sign1 & ~sign2 & ~sign3) | (~sign1 & sign2 & ~sign3) | (~sign1 & ~sign2 & sign3) | (~sign1 & ~sign2 & ~sign3)
    one_sign = Sum([If(sign, 1, 0) for sign in [sign1, sign2, sign3]]) <= 1
    
    s = Solver()
    s.add(one_lady)
    s.add(one_sign)

    return s



def trial10():
    r1, r2, r3 = Bools("r1 r2 r3")  # r1, r2, r3 represent Rooms I, II, III
    # True for lady, False for tiger

    # Sign interpretations
    sign1 = Not(r2)  # A tiger is in Room II
    sign2 = Not(r3)  # A tiger is in Room III
    sign3 = Not(r1)  # A tiger is in Room I

    # One lady condition
    one_lady = Sum([If(r, 1, 0) for r in [r1, r2, r3]]) == 1

    # Sign conditions
    sign_conditions = And(
        Implies(r1, sign1),  # Sign on the door of the lady's room is true
        Or(Not(sign2), Not(sign3))  # At least one of the other two signs is false
    )

    s = Solver()
    s.add(one_lady)
    s.add(sign_conditions)

    return s


def trial11():
    r1, r2, r3 = Ints("r1 r2 r3")
    # ri = 0, if tiger in room i
    #      1, if lady in room i
    #      2, if room i is empty
    rs = [r1, r2, r3]
    range_cond = [(0 <= r) & (r <= 2) for r in rs]
    distinct_cond = Distinct(rs)

    sign1 = r3 == 2
    sign2 = r1 == 0
    sign3 = r3 == 2
    signs = [sign1, sign2, sign3]
    
    sign_cond = [Implies(rs[i] == 0, ~signs[i]) & \
                 Implies(rs[i] == 1, signs[i]) for i in range(3)]

    s = Solver()
    s.add(range_cond)
    s.add(distinct_cond)
    s.add(sign_cond)

    return s


def trial12():
    # Define room states: 0 for tiger, 1 for lady, 2 for empty
    rs = [Int(f"rs[{i}]") for i in range(9)]
    range_cond = [And(rs[i] >= 0, rs[i] <= 2) for i in range(9)]

    # Exactly one room contains a lady
    one_lady = Sum([If(rs[i] == 1, 1, 0) for i in range(9)]) == 1

    # Define the signs
    sign1 = rs[0] == 1  # The lady is in an odd-numbered room
    sign2 = rs[1] == 2  # This room is empty
    sign3 = Or(sign5, Not(sign7))  # Either Sign V is right or Sign VII is wrong
    sign4 = Not(sign1)  # Sign I is wrong
    sign5 = Or(sign2, sign4)  # Either Sign II or Sign IV is right
    sign6 = Not(sign3)  # Sign III is wrong
    sign7 = rs[0] != 1  # The lady is not in Room I
    sign8 = And(rs[7] == 0, rs[8] == 2)  # This room contains a tiger and Room IX is empty
    sign9 = And(rs[8] == 0, sign6)  # This room contains a tiger and VI is wrong

    # Define conditions for each room's sign
    sign_cond = [
        Implies(rs[i] == 1, signs[i]),  # If the room has a lady, the sign is true
        Implies(rs[i] == 0, Not(signs[i]))  # If the room has a tiger, the sign is false
        # Sign on empty rooms can be either true or false, no additional constraints needed
        for i, signs in enumerate([sign1, sign2, sign3, sign4, sign5, sign6, sign7, sign8, sign9])
    ]

    # Solver setup
    s = Solver()
    s.add(range_cond)
    s.add(one_lady)
    s.add(sign_cond)

    return s



