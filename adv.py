from room import Room
from player import Player
from world import World
from util import Queue

import random
from ast import literal_eval

# Load world
world = World()

# breadth first search for "?"
def bfs(starting_vertex):
    q = Queue()
    q.enqueue([starting_vertex])
    visited = set()
    while q.size() > 0:
        path = q.dequeue()
        v = path[-1]
        if v not in visited:
            for exit in graph[v]:
                if graph[v][exit] == "?":
                    return path
            visited.add(v)
            for vertex in graph[v]:
                new_path = list(path)
                new_path.append(graph[v][vertex])
                q.enqueue(new_path)
    return None 

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
graph = {}
directions = {"n": "s", "s": "n", "w": "e", "e": "w"}
starting_room = player.current_room.id

# find starting room, store in graph
if starting_room not in graph:
    # create graph with first starting room
    graph[starting_room] = {}
    # all exits start as unvisited
    for direction in player.current_room.get_exits():
        graph[starting_room][direction] = "?"
        
# while graph length is less than room graph length
while len(graph) < len(room_graph):
    # create list to store unvisited exits
    unvisited_exits = []
    current_room = graph[player.current_room.id]
    
    # check through each exit and append to unvisited exits if == "?"
    for exit in current_room:
        if current_room[exit] == "?":
            unvisited_exits.append(exit)
            
    # if current room has unvisited exits pick a random direction 
    if len(unvisited_exits) > 0:
        # choose random exit
        random.shuffle(unvisited_exits)
        new_path = unvisited_exits[0]
        # add to traversal path
        traversal_path.append(new_path)
        prev_room = player.current_room.id
        
        # move player to room
        player.travel(new_path)
        
        # add new room to graph
        if player.current_room.id not in graph:
            graph[player.current_room.id] = {}
            for rooms in player.current_room.get_exits():
                graph[player.current_room.id][rooms] = "?"
                
        # update graph
        graph[prev_room][new_path] = player.current_room.id
        graph[player.current_room.id][directions[new_path]] = prev_room
        
        # if path ends
    else:
        prev_move = bfs(player.current_room.id)
        direction = ""
        for room in prev_move:
            for exit in graph[player.current_room.id]:
                if room == graph[player.current_room.id][exit]:
                    direction = exit
    
    player.travel(direction)
    traversal_path.append(direction)        

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
