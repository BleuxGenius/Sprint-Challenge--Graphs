from room import Room
from player import Player
from world import World


import random
from ast import literal_eval

# Load world
world = World()

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)




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
# when the end of a path is reached, player needs to backtrack in the opposite direction 
reversed_direction = {
    'n':'s',
    's':'n',
    'w':'e',
    'e':'w'
}

def traversal_map(starting_room, visited_rooms = set()):

    starting_path = []
        # get all possible exists in the current room 
    for direction in player.get_exits():
        # when player travels to room in direction of the exit
        player.travel(direction)
        # check if new room has been visitied 
        if player.current_room.id not in visited_rooms:
        # room has not been visited 
        #  mark visited 
            visited_rooms.add(player.current_room.id)
        # add new direction to the path 
            starting_path.append(direction)
        # use recursion with new current_room and add to the path 
            starting_path = starting_path + traversal_map(player.current_room.id, visited_rooms)
        # retrace steps and go to a diffrent room 
            player.travel(reversed_direction[direction])
        # add retraced steps to he path to keep the track of steps 
            starting_path.append(reversed_direction[direction])
        else:
            # Room already visited so retrace steps and go to a diffrent room 
            player.travel(reversed_direction[direction])
    return starting_path
    






# TRAVERSAL TEST - DO NOT MODIFY
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
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
