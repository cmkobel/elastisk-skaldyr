#include "baumWelch.h"
#include <stdlib.h>

void baumWelch(HMM *hmm, const int *Y, const int T, const int itterations){
    
    //Initial random init of HMM
    
    unsigned int i;
    unsigned int j;
    unsigned int l;
    
    // Gamma 2d matrix
    //
    // [time][state]
    //
    double ** gamma = calloc(T, sizeof(double*));
    for(i = 0; i < T; i++){
        gamma[i] = calloc(hmm->hiddenStates, sizeof(double));
    }
    
    // Xi 3d matrix
    //
    // [state][state][time]
    //
    double *** xi = (double ***)calloc(hmm->hiddenStates, sizeof(double**));
    for(i = 0; i < hmm->hiddenStates; i++){
        xi[i] = (double **)calloc(hmm->hiddenStates, sizeof(double*));
        for(j = 0; j < hmm->hiddenStates; j++){
            xi[i][j] = (double *)calloc(T, sizeof(double));
        }
    }

    for(int q = 0; q < itterations; q++) {
        double * scaleFactor = calloc(T, sizeof(double));
        double ** alpha = forward(hmm, Y, T, scaleFactor);
        double ** beta = backward(hmm, Y, T, scaleFactor);
        
        // Updating gamma
        for(i = 0; i < T; i++){
            for (j = 0; j < hmm->hiddenStates; j++) {
                double numerator = alpha[j][i]*beta[j][i];
                double denominator = 0.0;
                for(l = 0; l < hmm->hiddenStates; l++){
                    denominator += alpha[l][i]*beta[l][i];
                }
                gamma[i][j] = numerator/denominator;
            }
        }
        /*
        printf("Gamma\n");
        for(i = 0; i < T; i++) {
            for (j = 0; j < hmm->hiddenStates; j++){
                printf("%f, ", gamma[i][j]);
            }
            printf("\n");
        }
        printf("\n");
        */
        // xi denominator
        double * xiDenominator = calloc(T-1, sizeof(double));
        
        for(l = 0; l < T-1; l++){
            for(i = 0; i < hmm->hiddenStates; i++){
                for(j = 0; j < hmm->hiddenStates; j++){
                    xiDenominator[l] += alpha[i][l]*beta[j][l+1]*hmm->transitionProbs[i*hmm->hiddenStates+j]*hmm->emissionProbs[j*hmm->observations+Y[l+1]];
                }
            }
        }
        
        /*
        printf("XI Denominator\n");
        for(i = 0; i < T-1; i++){
            printf("%f, ", xiDenominator[i]);
        }
        printf("\n\n");
        */
        // Updating xi
        for(i = 0; i < hmm->hiddenStates; i++){
            for(j = 0; j < hmm->hiddenStates; j++){
                for(l = 0; l < T-1; l++){
                    double numerator = alpha[i][l]*beta[j][l+1]*hmm->transitionProbs[i*hmm->hiddenStates+j]*hmm->emissionProbs[j*hmm->observations+Y[l+1]];
                    double denominator = xiDenominator[l];
                    xi[i][j][l] = numerator/denominator;
                }
            }
        }
        
        //Updating initial probs
        for (i = 0; i < hmm->hiddenStates; i++) {
            hmm->initProbs[i] = gamma[0][i];
        }
        
        //Updating transition probs
        for (i = 0; i < hmm->hiddenStates; i++) {
            for (j = 0; j < hmm->hiddenStates; j++) {
                double xiSum = 0.0;
                double gammaSum = 0.0;
                for(l = 0; l < T-1; l++){
                    xiSum += xi[i][j][l];
                    gammaSum += gamma[l][i];
                }
                hmm->transitionProbs[i*hmm->hiddenStates+j] = xiSum/gammaSum;
            }
        }
        
        //Updating observations probs
        for (i = 0; i < hmm->hiddenStates; i++) {
            for (j = 0; j < hmm->observations; j++) {
                double numerator = 0.0;
                double denominator = 0.0;
                for(l = 0; l < T; l++){
                    if(Y[l] == j){
                        numerator += gamma[l][i];
                    }
                    denominator += gamma[l][i];
                }
                hmm->emissionProbs[i*hmm->observations+j] = numerator/denominator;
            }
        }
        
        //Normalization step
        for(i = 0; i < hmm->hiddenStates; i++){
            double sum = 0.0;
            for (j = 0; j < hmm->hiddenStates; j++) sum += hmm->transitionProbs[i*hmm->hiddenStates+j];
            for (j = 0; j < hmm->hiddenStates; j++) hmm->transitionProbs[i*hmm->hiddenStates+j] = hmm->transitionProbs[i*hmm->hiddenStates+j]/sum;
            sum = 0.0;
            for (j = 0; j < hmm->observations; j++) sum += hmm->emissionProbs[i*hmm->observations+j];
            for (j = 0; j < hmm->observations; j++) hmm->emissionProbs[i*hmm->observations+j] = hmm->emissionProbs[i*hmm->observations+j]/sum;
        }
    }
}

// Asign random variables to all initprobs, transprobs and obsprobs
void assignRandomValues(HMM *hmm){
    
    
    
}