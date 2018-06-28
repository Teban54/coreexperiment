from optimal_solution import dis
import math

def calc_beta(client_list, center_list, alpha=1):
    """
    Calculate the smallest beta value in the solution (figuratively speaking, the maximum distance any
    blocking coalition is allowed to deviate).
    
    Beta is defined as:
        For all clients in a blocking coalition (if it exists), new_dist < beta * old_dist.
            where  new_dist is distance from the client to the potential new center,
            and    old_dist is original distance from the client to the nearest center in center_list.
        Beta is reciprocal of the "friction factor". E.g. When beta is 0.5, all clients in the blocking
            coalition will be better off by a factor of 2 (distance halved).
        The greater the value of beta, the stronger the fairness guarantee.
        (Note that when beta>1, the local search can't converge as keeping the same solution itself forms
        a blocking coalition) 
        
    Alpha is defined as:
        A blocking coalition needs to contain at least (alpha * N / k) clients.
        The smaller the value of alpha, the stronger the fairness guarantee.
        
    Note: client_list is a list of actual clients; center_list is a list of indexes referencing to 
        client_list.
    """
    num = len(client_list)
    k = len(center_list)

    # Compute current assignments (nearest center for each client)
    assignment = dict()
    for client in client_list:
        min = 10000000000000000
        for center in center_list:
            if dis(client_list[center], client) < min:
                min = dis(client_list[center], client)
                mincenter = center
        assignment[client] = mincenter

    min_beta = 10000000000000000
    for i in range(len(client_list)):
        potential_center = client_list[i]
        # Get a list of betas for all clients
        beta_list = []
        for client in client_list:
            if dis(client, client_list[assignment[client]]) <= 0: # old_dist is already 0, can't improve
                continue
            beta_list.append(dis(client, potential_center) / dis(client, client_list[assignment[client]]))

        if (len(beta_list) < alpha * num / k): # Insufficient number of deviating clients
            continue

        # Calculate smallest beta - formed by the first (alpha * num / k) clients with smallest beta
        beta_list.sort()
        beta = beta_list[int(math.ceil(alpha * num / k))]
        min_beta = beta if beta < min_beta else min_beta

    return min_beta