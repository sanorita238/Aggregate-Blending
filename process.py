import json
# For doing all the matrix manipulations: transpose, inverse, matrix multiplication, etc.
import numpy as np


def calculate(input2, input3):
    try:
        print("Enter the number of sieves: ")
        m = len(input2)  # Input for M: Number of sieves
        print("Enter the total stockpiles/aggregates taken: ")
        n = len(input3[0])  # Number of# Input for N: Number of stockpiles

        def computeAlpha(weights):

            alpha = [[0 for i in range(len(weights[0]))]
                     for j in range(len(weights))]
            m = len(weights)
            n = len(weights[0])
            total_sum = [0 for i in range(len(weights[0]))]
            for i in range(len(weights[0])):
                for j in range(len(weights)):
                    total_sum[i] += weights[j][i]
            for i in range(len(weights[0])):
                sum = 0
                for j in range(len(weights)):
                    sum += weights[j][i]
                    alpha[j][i] = ((total_sum[i]-sum)/total_sum[i])*100
            return alpha

        print("Enter the retained weights")
        weights = input3  # Weight Matrix (M X N)
        # for i in range(m+1):
        #     a = []
        #     if(i < m):
        #         print("Sieve number ", i+1)
        #     else:
        #         print("Enter pan values: ")

        #     for j in range(n):
        #         if(i != m):
        #             print("Aggregate ", j+1, " retained weight: ")
        #         x = int(input())
        #         a.append(x)
        #     weights.append(a)

        print("The weight matrix is as follows: ")
        for i in range(m):
            for j in range(n):
                print(weights[i][j], end=" ")
            print()
        # entries=list(map(int,input().split()))
        # weights=np.array(entries).reshape(m+1,n)
        # alpha=[]
        # //finding Percentage passing values
        # Percentage Passing Matrix initialization (i.e. the actual values are yet to be filled)
        alpha = computeAlpha(weights)
        # removing the pan row
        alpha = alpha[:-1]
        print(alpha)

        # //matrix to store upper and lower bounds
        # Aggregate Gradation Matrix: To be taken as input (m X 2 matrix)
        beta = input2
        # for i in range(m):
        #     print("Lower:")
        #     lower = int(input())
        #     print("Upper:")
        #     upper = int(input())
        #     temp = []
        #     temp.append(lower)
        #     temp.append(upper)
        #     beta.append(temp)

        # function to store all the solutions present in the file
        # Reads the solution matrix from the respective file p22,p33,p44,p55
        def getSolutionMatrix(n):
            file_name = 'p'+str(n)+str(n)+'.txt'
            file = open(file_name, 'r')
            input = file.read(-1)
            return list(map(lambda x: json.loads(x), input.split(';')))

        # all solution is stored in gamma matrix
        # Integer Solution matrix, stores all the integer solutions
        gamma = getSolutionMatrix(n)

        # The [𝛿](delta)𝑇×M matrix stores the combined contribution of all the stockpiles corresponding to the
        # combined percent passing for each of the sieves entered for all the possible solutions 𝑇.
        delta = (np.matmul(gamma, np.transpose(alpha))) / \
            100  # Calculation of the delta matrix

        # -------------------------SEARCH ALGORITHM STARTS HERE--------------------------------
        # tau1[] and tau2[] binary matrices of the order 𝑇×M...T = total solutions, M = number of sieves
        tau1 = []
        tau2 = []

        # function for bound check
        def checkbounds(delta, beta):
            for i in range(len(delta)):
                pro1 = []
                pro2 = []
                for j in range(len(delta[i])):
                    #  A row in tau1 will be all 1s if gradation calculated for all the sieves is greater than or
                    # equal to the respective lower bounds
                    if(delta[i][j] >= beta[j][0]):
                        pro1.append(1)
                    elif(delta[i][j] < beta[j][0]):
                        pro1.append(0)
                    # a row in tau2 will be all 1s if gradation calculated for all the sieves is lesser than or equal
                    # to the respective upper bounds.
                    if(delta[i][j] <= beta[j][1]):
                        pro2.append(1)
                    elif(delta[i][j] > beta[j][1]):
                        pro2.append(0)

                tau1.append(pro1)
                tau2.append(pro2)

        # function call
        checkbounds(delta, beta)

        # Now apply the element-wise AND (&) operation between the two matrices tau1 and tau2.
        # This results in a third matrix of order 𝑇×𝑀, say [𝜑](phi) which is also a binary matrix.

        def and_of_tau1_tau2(tau1, tau2):
            phi = []
            for i in range(len(tau1)):
                phifinal = []
                for j in range(len(tau1[i])):
                    varnam = tau1[i][j] & tau2[i][j]
                    phifinal.append(varnam)
                phi.append(phifinal)
            return phi

        phi = []
        phi = and_of_tau1_tau2(tau1, tau2)

        # ----------------FINDING ALL POSSIBLE SOLUTIONS-----------------------
        omega = []
        for i in range(len(phi)):
            sac = False
            for j in range(len(phi[i])):
                if(phi[i][j] == 0):
                    sac = True
            if(sac == False):
                omega.append(1)
            else:
                omega.append(0)
        # psa=np.array(omega)
        # print(psa.shape)
        theta = []
        for i in range(len(omega)):
            if(omega[i] == 1):
                theta.append(i)

        # -----------PRINTING ALL POSSIBLE SOLUTIONS----------------
        print("The all required solutions:", len(theta), " is: ")
        result = []
        for i in range(len(theta)):
            # print(gamma[theta[i]], sep="\n")
            result.append(gamma[theta[i]])

        
        return {'status': 'success', 'data': result}
    except Exception as e:
        print(e)
        return {'status': 'error', 'description': str(e)}