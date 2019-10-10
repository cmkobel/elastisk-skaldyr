import ctypes as c
import os

"""
TODO
* make getters for the datastructures
* set up tests for each algorithm

"""


class binded_HMM:

    def __init__(self, n_hiddenstates, n_observations, address_to_so = "hmmmlib/build/libHMMLIB.so"):
        
        class HMM(c.Structure): # Jeg kan ikke finde ud af at definere denne klasse udenfor __init__, medmindre det er udenfor binded_HMM
            """ creates a struct to match HMM """
            _fields_ = [("hiddenStates", c.c_uint),
                        ("observations", c.c_uint),
                        ("transitionProbs", c.POINTER(c.c_double)),
                        ("emissionProbs", c.POINTER(c.c_double)),
                        ("initProbs", c.POINTER(c.c_double))]
        
        # Load the shared library into ctypes.
        self.libhmm = c.CDLL(os.path.abspath(address_to_so))
        
        # Set restypes of needed functions.
        self.libhmm.HMMCreate.restype = c.POINTER(HMM)
        self.libhmm.valdidateHMM.restype = c.c_bool
        self.libhmm.printHMM.restype = c.c_void_p
        self.libhmm.HMMDeallocate.restype = c.c_void_p

        self.libhmm.forward.restype = c.POINTER(c.c_double)
        self.libhmm.backward.restype = c.POINTER(c.c_double)
        
        self.libhmm.viterbi.restype = c.POINTER(c.c_uint)


        # Create HMM object
        self.hmm = self.libhmm.HMMCreate(n_hiddenstates, n_observations)
        

        """ 
        print('The following variables are accessible from the HMM struct')
        for i in [i for i in dir(hmm[0]) if str(i)[0:1] != '_']:
            print('\t', i)
        """


    def presentHMM(self):
        hs = self.hmm[0].hiddenStates
        obs = self.hmm[0].observations

        print('Presenting the HMM with the presentHMM()-function from the python-binding')
        print(' hiddenStates =', hs)
        print(' observations =', obs)
        
        print()
        formattedInitProbs = ["{:7.3f}".format(self.hmm[0].initProbs[i]) for i in range(hs)]
        print(' initProbs:', ''.join(formattedInitProbs))


        print()
        print(' transitionProbs: [hs][hs]', end = '\n  ')
        for row in range(hs):
            for col in range(hs):
                print("{:7.3f}".format(self.hmm[0].transitionProbs[row*hs+col]), end = ' ')
            print(end = '\n  ')
        print()

        
        print(' emissionProbs: [hs][obs]', end = '\n  ') # [7][4] eller [hs][obs]
        for row in range(hs):
            for col in range(obs):
                #print(round(self.hmm[0].emissionProbs[row*obs+col], 3), end = '  ')
                print("{:7.3f}".format(self.hmm[0].emissionProbs[row*obs+col]), end = ' ')
            print(end = '\n  ') 
        print()
        print(' The internal validation state is:', self.libhmm.valdidateHMM(self.hmm))


    ## Setters ##
    def setInitProbs(self, pi):
        if len(pi) != self.hmm[0].hiddenStates:
            raise Exception(f'Failed to set initProbs[]. initProbs[] should contain {self.hmm[0].hiddenStates} values but {len(pi)} were given.')

        self.hmm[0].initProbs = (c.c_double * self.hmm[0].hiddenStates)(*pi)


    def setTransitionProbs(self, new_trans_p):
        if len(new_trans_p) != self.hmm[0].hiddenStates:
            raise Exception(f'Failed to set transitionProbs[]. transitionProbs[] should contain {self.hmm[0].hiddenStates} rows but {len(new_trans_p)} were given.')
        for row in new_trans_p:
            if len(row) != self.hmm[0].hiddenStates:
                raise Exception(f'Failed to set transitionProbs[]. transitionProbs[] should contain {self.hmm[0].hiddenStates} columns but {len(row)} were given.')

        one_dimensional = [j for sub in new_trans_p for j in sub]
        # print(one_dimensional)
        self.hmm[0].transitionProbs = (c.c_double * (self.hmm[0].hiddenStates * self.hmm[0].hiddenStates))(*one_dimensional)


    def setEmissionProbs(self, new_emiss_p):
        if len(new_emiss_p) != self.hmm[0].hiddenStates:
            raise Exception(f'Failed to set emissionProbs[]. emissionProbs[] should contain {self.hmm[0].hiddenStates} rows but {len(new_emiss_p)} were given.')
        for row in new_emiss_p:
            if len(row) != self.hmm[0].observations:
                raise Exception(f'Failed to set emissionProbs[]. emissionProbs[] should contain {self.hmm[0].observations} columns but {len(row)} were given.')

        one_dimensional = [j for sub in new_emiss_p for j in sub]
        # print(one_dimensional)
        self.hmm[0].emissionProbs = (c.c_double * (self.hmm[0].hiddenStates * self.hmm[0].observations))(*one_dimensional)


    ## Getters ##
    def getInitProbs(self):
        return [self.hmm[0].initProbs[i] for i in range(self.hmm[0].hiddenStates)]

    def getTransitionProbs(self):
        hs = self.hmm[0].hiddenStates
        return [[self.hmm[0].transitionProbs[row * hs + col] for col in range(hs)] for row in range(hs)]

    def getEmissionProbs(self):
        hs = self.hmm[0].hiddenStates
        obs = self.hmm[0].observations
        return [[self.hmm[0].emissionProbs[row*obs + col] for col in range(obs)] for row in range(hs)]
        

    ## Algorithms ##
    def forward(self, observation_data):
        scalefactor = len(observation_data) * [0]
        scalefactor_p = (c.c_double * len(observation_data))(*scalefactor)
        output = self.libhmm.forward(self.hmm,
                                     (c.c_int * len(observation_data))(*observation_data),
                                     len(observation_data),
                                     scalefactor_p)
        #print('after execution:', [scalefactor_p[i] for i in range(len(observation_data))])
        return [output[i] for i in range(len(observation_data)*self.hmm[0].hiddenStates)], scalefactor_p

    def backward(self, observation_data, scalefactor_from_forward):
        """ if scalefactor_from_forward == None:
            scalefactor_from_forward = len(observation_data) * [1] """
        output = self.libhmm.backward(self.hmm,
                                     (c.c_int * len(observation_data))(*observation_data),
                                     len(observation_data),
                                     (c.c_double * len(observation_data))(*scalefactor_from_forward))
        return [output[i] for i in range(len(observation_data)*self.hmm[0].hiddenStates)] # Evt. generator?

    

    def viterbi(self, observation_data):
        output = self.libhmm.viterbi(self.hmm, (c.c_uint * len(observation_data))(*observation_data), len(observation_data)) 
        return [output[i] for i in range(len(observation_data))] # Evt. generator?


    def deallocate(self):
        self.libhmm.HMMDeallocate(self.hmm) # Jeg ved ikke hvorfor denne ikke virker???



