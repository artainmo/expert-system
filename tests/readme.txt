# this is a comment
# input file created from this backward-chaining video example (https://www.youtube.com/watch?v=6DU42so8k48)

F & B -> Z        # F and B implies Z
C & D -> F        # C and B implies F
A     -> D        # A implies E

=AEBC             # Initial facts : A, E, B and C are true. All others are false.

?Z                # Queries: Is Z true or false?
