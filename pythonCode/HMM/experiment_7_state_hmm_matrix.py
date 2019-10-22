from hmm import hmm

m = hmm("hmm-7-state.txt")

"""

    #
    # 7-state HMM from lecture
    #

    hidden
    1 2 3 4 5 6 7

    observables
    A C G T

    pi
    0.00 0.00 0.00 1.00 0.00 0.00 0.00

    transitions
    0.00 0.00 0.90 0.10 0.00 0.00 0.00
    1.00 0.00 0.00 0.00 0.00 0.00 0.00
    0.00 1.00 0.00 0.00 0.00 0.00 0.00
    0.00 0.00 0.05 0.90 0.05 0.00 0.00
    0.00 0.00 0.00 0.00 0.00 1.00 0.00
    0.00 0.00 0.00 0.00 0.00 0.00 1.00
    0.00 0.00 0.00 0.10 0.90 0.00 0.00

    emissions
    0.30 0.25 0.25 0.20
    0.20 0.35 0.15 0.30
    0.40 0.15 0.20 0.25
    0.25 0.25 0.25 0.25
    0.20 0.40 0.30 0.10
    0.30 0.20 0.30 0.20
    0.15 0.30 0.20 0.35

"""
print("\n\nFORWARD:")
alpha, scale = m.forward_with_scaling([0, 0, 0, 0, 0, 1, 1, 0, 0, 0])
print("""\nUsing forloops""")
for i in alpha:
    print(i)
    
print("\n\n")
alpha, scaling = m.forward_using_matrix([0, 0, 0, 0, 0, 1, 1, 0, 0, 0])
print("""\nUsing Matrix """)
for i in alpha:
    print(i)

print("\n\nBACKWARD:")
beta = m.backward_with_scaling([0, 0, 0, 0, 0, 1, 1, 0, 0, 0], scale)
print("""\nUsing forloops - no scaling""")
for i in beta:
    print(i)
    
beta = m.backward_using_matrix([0, 0, 0, 0, 0, 1, 1, 0, 0, 0], scaling)
print("""\nUsing matrix - no scaling""")
for i in beta:
    print(i)

