from binding import *


o = binded_HMM(7, 4)


o.setInitProbs([0.00, 0.00, 0.00, 1.00, 0.00, 0.00, 0.00])
o.setTransitionProbs([[0.00, 0.00, 0.90, 0.10, 0.00, 0.00, 0.00],
                      [1.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                      [0.00, 1.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                      [0.00, 0.00, 0.05, 0.90, 0.05, 0.00, 0.00],
                      [0.00, 0.00, 0.00, 0.00, 0.00, 1.00, 0.00],
                      [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 1.00],
                      [0.00, 0.00, 0.00, 0.10, 0.90, 0.00, 0.00]])

o.setEmissionProbs([[0.30, 0.25, 0.25, 0.20],
                    [0.20, 0.35, 0.15, 0.30],
                    [0.40, 0.15, 0.20, 0.25],
                    [0.25, 0.25, 0.25, 0.25],
                    [0.20, 0.40, 0.30, 0.10],
                    [0.30, 0.20, 0.30, 0.20],
                    [0.15, 0.30, 0.20, 0.35]])

o.presentHMM()


test_viterbi_data = [3, 0, 2, 0, 2, 3, 3, 2, 3, 3, 2, 1, 3, 1, 0, 2, 3, 1, 0, 1, 0, 1, 0, 1, 3, 0, 1, 0, 2, 1, 0, 3, 0, 0, 0, 2, 3, 2, 0, 3, 0, 2, 3, 0, 2, 3, 0, 2, 2, 0, 1, 0, 2, 1, 0, 0, 3, 1, 2, 3, 1, 0, 3, 1, 0, 3, 1, 2, 0, 1, 0, 2, 0, 2, 1, 3, 0, 1, 2, 0, 3, 1, 0, 2, 3, 0, 2, 0, 0, 2, 0, 1, 0, 3, 1, 0, 3, 0, 0]
test_viterbi_output = o.libhmm.viterbi(o.hmm_object, (c.c_int * len(test_viterbi_data))(*test_viterbi_data), len(test_viterbi_data))
test_viterbi_expected = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1]

for i, j in zip(test_viterbi_output, test_viterbi_expected):
    assert i == j

#o.deallocate()  # Jeg ved ikke hvorfor denne ikke virker???

