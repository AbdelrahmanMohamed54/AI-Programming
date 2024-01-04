"""
# Exercise 1

from z3 import *

Aus, Bra, Ger = Ints('Aus Bra Ger')
Cats, Dogs, Fishes = Ints('Cats Dogs Fishes')
Bas, Foot, Socc = Ints('Bas Foot Socc')
Blue, Green, Red = Ints('Blue Green Red')

s = Solver()

s.add([And(1 <= x, x <= 3) for x in [Aus, Bra, Ger, Cats, Dogs, Fishes, Bas, Foot, Socc, Blue, Green, Red]])

s.add(Distinct([Aus, Bra, Ger]))
s.add(Distinct([Cats, Dogs, Fishes]))
s.add(Distinct([Bas, Foot, Socc]))
s.add(Distinct([Blue, Green, Red]))

s.add(Bra != 2)
s.add(Dogs == Bas)
s.add(Foot + 1 == Red)
s.add(Fishes == Cats - 1)
s.add(Dogs == Green + 1)
s.add(Ger == 3)


s.check()
#sat

m = s.model()
m

Output:-

[Foot = 2,
Blue = 1,
Socc = 1,
Bas = 3,
Aus = 2,
Fishes = 1,
Bra = 1,
Green = 2,
Dogs = 3,
Cats = 2,
Red = 3,
Ger = 1]
"""

# Exercise 2

from z3 import *

# Define integer variables for nationalities, pets, sports, and house colors
Ame, Bri, Can, Iri = Ints('Ame Bri Can Iri')
Butterflies, Dolphins, Horses, Turtles = Ints('Butterflies Dolphins Horses Turtles')
Bowling, Handball, Swimming, Tennis = Ints('Bowling Handball Swimming Tennis')
Black, Blue, Red, White = Ints('Black Blue Red White')

# Create a solver instance
s = Solver()

# All variables should have values from 1 to 4, representing the house numbers
vars = [Ame, Bri, Can, Iri, Butterflies, Dolphins, Horses, Turtles, Bowling, Handball, Swimming, Tennis, Black, Blue, Red, White]
s.add([And(1 <= var, var <= 4) for var in vars])

# Each attribute (nationality, pet, sport, house color) must be unique to a house
s.add(Distinct([Ame, Bri, Can, Iri]))
s.add(Distinct([Butterflies, Dolphins, Horses, Turtles]))
s.add(Distinct([Bowling, Handball, Swimming, Tennis]))
s.add(Distinct([Black, Blue, Red, White]))

# Adding the given constraints
s.add(Bowling + 2 == Swimming)
s.add(Iri + 1 == Handball)
s.add(Black == 2)
s.add(Horses + 1 == Red)
s.add(Ame + 1 == Turtles)
s.add(Bowling > Tennis)
s.add(Handball + 1 == White)

# Check for satisfiability and print the model if a solution exists
if s.check() == sat:
    m = s.model()
    solution = {str(v): m[v] for v in vars}
else:
    solution = "No solution found"

# Print the solution
print(solution)
