#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/usr/bin/env python3
# -- coding: utf-8 --
"""
Created on Wed Apr  7 22:30:01 2021

@author: nicolasnahas
"""
import random
import numpy as np



def cfr (tour):
    regretP1 = np.array([[(0,0),(0,0),(0,0)],[(0,0),(0,0),(0,0)]]) # ([(pass,bet)_carte_0 ..], [(pass,bet)_carte_0_si_bet ...] )
    regretP2 = np.array([(0,0),(0,0),(0,0)]) #[(pass,bet),(0,0),(0,0)]
    
    stratP1 = np.array([[1.,1.,1.],[1.,1.,1.]]) # ([proba_carte_0 , proba_carte_1, proba_carte_2],[proba_carte_0_si_P2bet ,etc
    stratP2 = np.array([1.,1.,1.]) # ([proba_carte_0 , proba_carte_1, proba_carte_2]

    
    
    # On détermine la stratégie optimale
    for i in range(tour): 
        # On dstribue les cartes
        cartes = [0,1,2] 
        carteP1, carteP2 = random.sample(cartes,2)
        
        #On appelle jeu 
        r_P1, r_P2, h_P1, h_P2 = jeu (carteP1, carteP2, stratP1, stratP2)
        
        #calcul du regret du player 1 
        a,b = regretP1[0][carteP1]
        a,b = (a + (h_P1[0][0]-r_P1)),(b + (h_P1[0][1]-r_P1))
        if (a<=0):
            a=0
        if (b<=0):
            b=0 
        regretP1[0][carteP1] = (a,b)
        
        a,b = regretP1[1][carteP1]
        a,b = (a + (h_P1[1][0]-r_P1)),(b + (h_P1[1][1]-r_P1))
        if (a<=0):
            a=0
        if (b<=0):
            b=0 
        regretP1[1][carteP1] = (a,b)

        # calcul du regret du player 2 
        a,b = regretP2[carteP2]
        a,b = (a + (h_P2[0]-r_P2)),(b + (h_P2[1]-r_P2))
        if (a<=0):
            a=0
        if (b<=0):
            b=0 
        regretP2[carteP2] = a,b
        
        
        for i in range(0,3):
            a,b = regretP1[0][i]
            som=a+b
            if(som!=0):
                b = b/som
            else:
                b=0.5
            stratP1[0][i] = b
            
            
            a,b = regretP1[1][i]
            som=a+b
            if(som!=0):
                b = b/som
            else:
                b=0.5
            stratP1[1][i] = b
            
            a,b = regretP2[i]
            som=a+b
            if(som!=0):
                b = b/som
            else:
                b=0.5
            stratP2[i] = b
            
        
    return stratP1,stratP2 
    

    



def jeu(carteP1, carteP2, stratP1, stratP2):
    

    # variable de reward hypothétique 
    reward_hypoP1 =np.array([[0,0],[0,0]]) # [(pass_1er,bet_1er) , (pass_2nd,bet_2nd)]
    reward_hypoP2 =[0,0] # [pass,bet]
    
    # variable de reward réel 
    reward_reelP1 = 0
    reward_reelP2 = 0
    
    

    if (random.uniform(0, 1) < stratP1[0][carteP1]): 
        # P1 bet 
        
        if (random.uniform(0, 1) < stratP2[carteP2]):
            # P2 bet
            
            if (carteP1 > carteP2):
                reward_reelP1 = 2
                reward_hypoP1[0][1] = 2
                reward_hypoP2[1] = -2
            else :
                reward_reelP1 = -2
                reward_hypoP1[0][1] = -2
                reward_hypoP2[1] = 2
            
        else: # P2 pass
            reward_reelP1 = 1
            reward_hypoP1[0][0] = 1
            reward_hypoP2[0] = -1

    else: # P1 pass
        if (random.uniform(0, 1) < stratP2[carteP2]): 
            # P2 bet 
            
            if (random.uniform(0, 1) < stratP1[1][carteP1]): 
                # P1 bet 
                
                if (carteP1 > carteP2):
                    reward_reelP1 = 2
                    reward_hypoP1[1][1] = 2
                    reward_hypoP2[1] = -2
                else :
                    reward_reelP1 = -2
                    reward_hypoP1[1][1] = -2
                    reward_hypoP2[1] = 2
                    
            else :
                # P1 pass
                reward_reelP1 = -1
                reward_hypoP1[1][0] = -1
                reward_hypoP2[1] = 1
            
        else :
            # P2 pass
                reward_reelP1 = 0
                reward_hypoP1[0][0] = 0
                reward_hypoP2[0] = 0
                
    # calcul des reward hypothétiques
    
    # P1 bet et P2 bet
    if (carteP1 > carteP2):
        reward_hypoP1[0][1] = 2
        reward_hypoP2[1] = -2
    else :
        reward_hypoP1[0][1] = -2
        reward_hypoP2[1] = 2
    
    # P1 bet & P2 pass
    reward_hypoP1[0][0] = 1
    reward_hypoP2[0] = -1
    
    # P1 pass P2 bet puis P1 bet
    if (carteP1 > carteP2):
        reward_hypoP1[1][1] = 2
        reward_hypoP2[1] = -2
    else :
        reward_hypoP1[1][1] = -2
        reward_hypoP2[1] = 2
        
    # P1 pass P2 bet puis P1 pass
    reward_hypoP1[1][0] = -1
    reward_hypoP2[1] = 1
                        
 
    # le reward de P2 est le reward inverse de P1        
    reward_reelP2 = -reward_reelP1
            
        
        
    # return
    liste = [reward_reelP1, reward_reelP2, reward_hypoP1, reward_hypoP2]
    
    
    
    
    #print (liste)
    
    return liste 
    


     
a,b = cfr(10000)
print ("stratégie Player 1")
print ("Valet proba de succès -> " + str(a[0][0]))
print ("Reine proba de succès -> " + str(a[0][1]))
print ("Roi proba de succès -> " + str(a[0][2]))
print ("------")
print ("stratégie Player 1 après que le palyer 2 ait parlé")
print ("Valet proba de succès -> " + str(a[1][0]))
print ("Reine proba de succès -> " + str(a[1][1]))
print ("Roi proba de succès -> " + str(a[1][2]))
print ("------")

print ("stratégie Player 2")
print ("Valet proba de succès -> " + str(b[0]))
print ("Reine proba de succès -> " + str(b[1]))
print ("Roi proba de succès -> " + str(b[2]))


# In[ ]:




