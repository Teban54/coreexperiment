import sys

from optimal_solution import dis
from kmedian import *
from utils import *
from local_search_capture import calc_kcenter_objective
# from queue import PriorityQueue
from data_parser import data_pt
import heapq
import math


agent_match = {} # dict mapping agent index to facility index matched
coalition_size = 0 # Hopefully not 1 as it can cause issues
open_facilities = set()


class agent_node_groups:
    def __init__(self, index, point, dist):
        self.index = index
        self.point = point
        self.dist = dist
        self.prev = None
        self.next = None # contains the reference to the next node


class facility_groups:
    """
    The following changes are made for protected groups:

    Procedure wise:
        - Opens a facility if there are alpha*N/k agents OF THE SAME GROUP in the ball.
        - Once it's opened, match all agents within the ball to the facility, regardless of their groups.
        - If an agent is covered by an already open facility, match it there regardless of the group.

    Object wise:
        - Instead of a single linked list of agents, there will be multiple linked lists, one for each protected group.
        - Facilities will be sorted based on the minimal pointer value of any linked list.
    """

    def __init__(self, index, data_list, groups_list, groups_index_list, distances):
        self.index = index
        self.groups_list = groups_list
        self.groups_index_list = groups_list
        self.point = data_list[index]
        self.agent_lists = [None] * len(groups_list)
        self.cur_pointers = [None] * len(groups_list)

        for group_index in range(len(groups_list)):
            group = groups_list[group_index]
            group_with_indexes = groups_index_list[group_index]

            # Generate distances and sort agents by distance
            agents = []
            for i in range(len(group)):
                agents.append(agent_node_groups(group_with_indexes[i], group[i], distances[self.point][group[i]]))
            agents.sort(key=lambda agent: agent.dist)

            # Convert sorted list to linked list
            agent_list_end = agents[0]
            agents[0].prev = None
            self.agent_lists[group_index] = agent_list_end
            for i in range(1, len(group)):
                #print(coalition_size)
                agent_list_end.next = agents[i]
                agents[i].prev = agent_list_end
                agent_list_end = agents[i]
                if i == coalition_size - 1: # Initially point at S-1
                    self.cur_pointers[group_index] = agent_list_end
                    # self.cur_pointer_pos = i

    def min_pointer_dist(self):
        """
        Gets the minimum distance across all agents that each pointer (for each group) is pointing to.
        Returns None if none of the pointers exist.
        """
        min_dist = sys.maxsize
        for pointer in self.cur_pointers:
            if pointer is not None:
                min_dist = min(min_dist, pointer.dist)
        if min_dist == sys.maxsize:
            return None
        return min_dist

    def __lt__(self, other):
        my_dist = self.min_pointer_dist()
        other_dist = other.min_pointer_dist()
        if my_dist is None:
            return False
        if other_dist is None:
            return True
        if my_dist == other_dist:
            return self.index - other.index < 0
        return my_dist < other_dist

    # def __str__(self):
    #     #return "%d %.2f" % (self.index, self.cur_pointer.dist)
    #     str = []
    #     agent = self.agent_list
    #     while agent is not None:
    #         str.append("(%d, %.2f)" % (agent.index, agent.dist))
    #         agent = agent.next
    #     return "%d %.2f %s" % (self.index, self.cur_pointer.dist, "[" + ', '.join(str) + "]")

    def remove_node(self, group_index, agent_node, update_pointer = True):
        if update_pointer and self.cur_pointers[group_index]:
            self.cur_pointers[group_index] = self.cur_pointers[group_index].next
        if agent_node == self.agent_lists[group_index]:
            self.agent_lists[group_index] = agent_node.next
            if self.agent_lists[group_index]:
                self.agent_lists[group_index].prev = None
        else:
            prev = agent_node.prev
            next = agent_node.next
            prev.next = next
            if next:
                next.prev = prev

    def remove_matched_agents(self, group_index, start, update_pointer = True):
        """
        Remove all agents matched to other facilities from start to cur_pointer.
        Stops when every agent is considered and cur_pointer itself is unmatched or is None.
        # Consider any agent up to the old cur_pointer, but if a new cur_pointer is unmatched, it stops there.
        :param match_here: whether unmatched agents should be matched to this facility
        :param update_pointer: whether pointer should be moved back by 1 per matched agent
        :return: bool of whether any matched agents were found and removed
        """
        found_match = False
        while start is not None and (start != self.cur_pointers[group_index] or start.index in agent_match): # stops when start is cur_pointer and not matched
            if start.index in agent_match:
                found_match = True
                next = start.next
                self.remove_node(group_index, start, update_pointer)
                start = next
            else:
                start = start.next
        return found_match

    def process(self):
        """
        Perform actions once the facility is removed from PriorityQueue.
        :return: bool representing whether the facility should be added back to pq
        """
        if self.index in open_facilities: # Already open
            # NOTE: Only match one agent (from any group) at a time, NOT one agent per group!
            # Need to find next agent with minimum dist
            min_dist = sys.maxsize
            min_dist_group = -1
            for group_index in range(len(self.groups_list)):
                if self.cur_pointers[group_index] is None:  # All agents in this group have been matched
                    continue
                found_match = self.remove_matched_agents(group_index, self.cur_pointers[group_index], True)
                if not found_match:  # agent can be matched
                    agent = self.cur_pointers[group_index]
                    if agent.dist < min_dist:
                        min_dist = agent.dist
                        min_dist_group = group_index
            if min_dist_group != -1:  # found at least 1 agent, match closest agent here
                agent_match[self.cur_pointers[min_dist_group].index] = self.index
                self.cur_pointers[min_dist_group] = self.cur_pointers[min_dist_group].next

        else: # Not open yet
            # NOTE: If multiple groups can be opened, open the one with the least distance, NOT all of them!
            min_dist = sys.maxsize
            min_dist_group = -1
            #print("starting agent_match: %s" % str(agent_match))
            for group_index in range(len(self.groups_list)):
                #if self.cur_pointers[group_index] is None:  # Insufficient agents in this group to form a blocking coalition
                #    continue
                found_match = self.remove_matched_agents(group_index, self.agent_lists[group_index], True)
                if not found_match:  # facility can be opened due to this group
                    agent = self.cur_pointers[group_index]
                    if agent and agent.dist < min_dist:  # agent can be None if all agents in the group are not matched, but there are insufficient agents
                        # to form a blocking coalition
                        min_dist = agent.dist
                        min_dist_group = group_index
            #print("intermediate agent_match: %s" % str(agent_match))
            if min_dist_group != -1:  # all S agents before cur_pointer (inclusive) in this group are unmatched, open facility
                open_facilities.add(self.index)
                # match agents in ALL groups whose distance <= min_dist to this facility
                for group_index in range(len(self.groups_list)):
                    agent = self.agent_lists[group_index]
                    while (agent is not None
                           and agent.dist <= min_dist
                           and not (self.cur_pointers[group_index] is not None and agent == self.cur_pointers[group_index].next)):
                        #print("Consider agent %d for facility %d" % (agent.index, self.index))
                        if agent.index in agent_match: # bug in code
                            raise RuntimeError
                        agent_match[agent.index] = self.index
                        #print("Agent %d matched to facility %d" % (agent.index, self.index))
                        agent = agent.next
                    #self.cur_pointer = self.cur_pointer.next
                    self.cur_pointers[group_index] = agent  # First agent that exceeds min_dist (not matched yet)
                    # Note the pointer for some groups might have been moved backwards
        return any(self.cur_pointers)


def ball_growing_procedure_groups(data_list, groups_list, groups_index_list, k, alpha=1, distances=None,
                           client_list=None, remaining_k=-1):
    """
    Performs the ball-growing algorithm that gives 2.414-approx.

    Protected groups are dealt with in the following way:
        - Opens a facility if there are alpha*N/k agents OF THE SAME GROUP in the ball.
        - Once it's opened, match all agents within the ball to the facility, regardless of their groups.
        - If an agent is covered by an already open facility, match it there regardless of the group.

    :param data_list: list of data points (serve as both agents and facilities)
    :param groups_list: A list of sublists that store clients in protected groups, one for each group.
        e.g. [[man1, man2], [woman1, woman2, woman3]]
    :param groups_index_list: A list of sublists that store indexes of clients in protected groups, one for each group.
        e.g. [[3, 5], [1, 2, 4]]
    :param k: number of centers to be opened (determines blocking coalition size)
    :param alpha: parameter that gives size of blocking coalition (see utils)
    :param client_list: list of indexes of available facilities to choose
        default: 0, 1, ..., len(data_list)-1
    :param remaining_k: number of remaining centers to be opened
        default: k
    :return: list of indexes of opened facilities
    """
    global agent_match
    global coalition_size
    global open_facilities
    global opened_something
    #global match_add_agents
    agent_match = {}
    open_facilities = set()
    #
    # match_add_agents = 0

    if not distances:
        distances = calc_distances(data_list)
    if not client_list:
        client_list = range(len(data_list))
    if remaining_k == -1:
        remaining_k = k
    num = len(data_list)
    coalition_size = math.ceil(alpha * num / k)
    pq = []
    for i in client_list:
        pq.append(facility_groups(i, data_list, groups_list, groups_index_list, distances))
    heapq.heapify(pq)

    while len(pq) > 0 and len(open_facilities) < remaining_k:
        cur_facility = heapq.heappop(pq)
        push_back = cur_facility.process()
        if push_back:
            heapq.heappush(pq, cur_facility)

    facility_indexes = list(open_facilities)
    if len(facility_indexes) == 0:
        # Each protected group is so small that no blocking coalitions could form
        # Generate something randomly
        return [client_list[random.randint(0, len(client_list)-1)] for x in range(remaining_k)]
    return facility_indexes


def ball_growing_groups(data_list, groups_list, groups_index_list, k, alpha=1, distances=None):
    """
    Runs the ball-growing algorithm that gives 2.414-approx.
    :param data_list: list of data points (serve as both agents and facilities)
    :param groups_list: A list of sublists that store clients in protected groups, one for each group.
        e.g. [[man1, man2], [woman1, woman2, woman3]]
    :param k: number of centers to be opened (determines blocking coalition size)
    :param alpha: parameter that gives size of blocking coalition (see utils)
    :return: - k-center objective value
             - k-median objective value
             - minimum beta value
    """

    if not distances:
        distances = calc_distances(data_list)
    facility_indexes = ball_growing_procedure_groups(data_list, groups_list, groups_index_list, k, alpha, distances=distances, client_list=range(len(data_list)), remaining_k=k)
    print("Ball growing algorithm picked %d facilities when k=%d" % (len(facility_indexes), k))
    kcenterobj = calc_kcenter_objective(data_list, facility_indexes, k, distances)
    kmedianobj = cal_dis(data_list, facility_indexes, distances)
    print("For %d median objective, ball growing value is %d" % (k, kmedianobj))
    return kcenterobj, kmedianobj, calc_beta_groups(data_list, groups_list, facility_indexes, k, alpha)


def ball_growing_k_median_groups(data_list, groups_list, groups_index_list, k, alpha=1, distances=None):
    """
    Runs the ball-growing algorithm followd by k-median algorithm.
    :param data_list: list of data points (serve as both agents and facilities)
    :param groups_list: A list of sublists that store clients in protected groups, one for each group.
        e.g. [[man1, man2], [woman1, woman2, woman3]]
    :param k: number of centers to be opened (determines blocking coalition size)
    :param alpha: parameter that gives size of blocking coalition (see utils)
    :return: - k-center objective value
             - k-median objective value
             - minimum beta value
    """

    if not distances:
        distances = calc_distances(data_list)
    remaining_indexes = set(range(len(data_list)))
    facility_indexes = ball_growing_procedure_groups(data_list, groups_list, groups_index_list, k, alpha, distances=distances, client_list=range(len(data_list)), remaining_k=k)
    remaining_indexes = remaining_indexes.difference(set(facility_indexes))
    remaining_k = k - len(facility_indexes)
    if remaining_k > 0:
        new_facility_indexes, _ = kmedian_procedure(data_list, k, alpha, distances=distances,
                                                   client_list=list(remaining_indexes), remaining_k=remaining_k)
        facility_indexes += new_facility_indexes

    print("Ball growing + k-median algorithm picked %d facilities when k=%d" % (len(facility_indexes), k))
    kcenterobj = calc_kcenter_objective(data_list, facility_indexes, k, distances)
    kmedianobj = cal_dis(data_list, facility_indexes, distances)
    print("For %d median objective, ball growing value is %d" % (k, kmedianobj))
    return kcenterobj, kmedianobj, calc_beta_groups(data_list, groups_list, facility_indexes, k, alpha)


def ball_growing_repeated_groups(data_list, groups_list, groups_index_list, k, alpha=1, distances=None):
    """
    Runs the ball-growing algorithm repeatedly, until exactly k centers are opened.
    :param data_list: list of data points (serve as both agents and facilities)
    :param groups_list: A list of sublists that store clients in protected groups, one for each group.
        e.g. [[man1, man2], [woman1, woman2, woman3]]
    :param k: number of centers to be opened (determines blocking coalition size)
    :param alpha: parameter that gives size of blocking coalition (see utils)
    :return: - k-center objective value
             - k-median objective value
             - minimum beta value
    """

    if not distances:
        distances = calc_distances(data_list)
    remaining_indexes = set(range(len(data_list)))
    facility_indexes = []
    remaining_k = k

    while remaining_k > 0:
        facility_indexes += ball_growing_procedure_groups(data_list, groups_list, groups_index_list, k, alpha, distances=distances, client_list=list(remaining_indexes), remaining_k=remaining_k)
        remaining_indexes = remaining_indexes.difference(set(facility_indexes))
        remaining_k = k - len(facility_indexes)

    print("Ball growing algorithm (repeated) picked %d facilities when k=%d" % (len(facility_indexes), k))
    kcenterobj = calc_kcenter_objective(data_list, facility_indexes, k, distances)
    kmedianobj = cal_dis(data_list, facility_indexes, distances)
    print("For %d median objective, ball growing value is %d" % (k, kmedianobj))
    return kcenterobj, kmedianobj, calc_beta_groups(data_list, groups_list, facility_indexes, k, alpha)
