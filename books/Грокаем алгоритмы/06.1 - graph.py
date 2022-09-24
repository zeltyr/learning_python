graph = {}
graph["you"] = ["alice", "claire", "bob"]
graph["alice"] = ["peggy"]
graph["bob"] = ["peggy", "anuj"]
graph["claire"] = ["thom", "tony"]
graph["peggy"] = []
graph["anuj"] = []
graph["thom"] = []
graph["tony"] = []

from collections import deque
from telnetlib import theNULL


def person_is_seller(name):
    return name[-1] == 'b'


def search_in_queue(name): 

    search_queue = deque()
    search_queue += graph[name]
    searched = []
    while search_queue:
        person = search_queue.popleft()
        if person in searched: continue
        if person_is_seller(person):
            print(person + " is mango seller!")
            return True
        else:
            search_queue += graph[person]
            searched.append(person)
    return False

search_in_queue("you")
    