from room import Room
from player import Player
from world import World
from util import Queue

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()


def room_recursive(starting_room, room_graph, room_paths=None, visited=None):
    '''
    Function to map out relationships between rooms
    '''

    # Initialize an empty list on first pass
    if visited is None:
        visited = []
    # Room paths is a dict
    if room_paths is None:
        room_paths = {}
    # Get the current room ID
    room_id = starting_room.id
    # If the room is not yet in the paths dict
    if room_id not in room_paths.keys():
        # Add the room to the visited list
        visited.append(room_id)
        # Then add it to the paths dict
        room_paths[room_id] = {}
        # Get the exits for the room
        directions = starting_room.get_exits()
        # For each exit you can take
        for dir in directions:
            # Update the paths dictionary with the directions and room IDs
            next_room = starting_room.get_room_in_direction(dir).id
            room_paths[room_id].update({dir: next_room})
        directions = starting_room.get_exits()
        # Travel in each direction available from the starting room
        for direction in directions:
            new_room = starting_room.get_room_in_direction(direction)
            # Now recursively perform this on the new room
            room_recursive(new_room, room_graph, room_paths, visited)
        if len(room_paths) == len(room_graph):
            return room_paths, visited


def bfs(starting_room, destination_room, room_paths):
    # Store already visited rooms in a set
    visited = set()

    # Queue to store rooms to visit
    roomsToVisit = Queue()

    # Queue to store directions to traverse
    directions = Queue()

    # Initialize the rooms queue with the start room
    roomsToVisit.enqueue([starting_room])

    # Initialize directions with a blank list
    directions.enqueue([])

    # While the queue is not empty
    while roomsToVisit.size() > 0:
        # Dequeue the next room
        vertex_path = roomsToVisit.dequeue()
        # Take the next direction from the directions queue
        dir_path = directions.dequeue()
        # The room at the end of the path is the latest room
        vertex = vertex_path[-1]
        # If the room hasn't been visited
        if vertex not in visited:
            # Add it to visited
            visited.add(vertex)
            # If the room is the destination, return the path
            if vertex == destination_room:
                return dir_path
            # For each direction a room has stored in it
            for direction in room_paths[vertex]:
                # Store the room and direction path
                path_copy = vertex_path.copy()
                dirpath_copy = dir_path.copy()

                # Update the copied path with the latest information
                path_copy.append(room_paths[vertex][direction])
                dirpath_copy.append(direction)
                roomsToVisit.enqueue(path_copy)
                directions.enqueue(dirpath_copy)


# This will be where we store our results
traversal_path = []

# Initialize the player in the starting room for the given world
player = Player(world.starting_room)

# Visit each of the rooms
room_dict, visited = room_recursive(world.starting_room, room_graph)

# For each room visited
for i in range(len(visited)-1):
    # Use a BFS to find the shortest path between the two rooms
    path = bfs(visited[i], visited[i+1], room_dict)
    # Add the directions to get between those rooms to the result
    traversal_path.extend(path)


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

print(traversal_path)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, \
{len(visited_rooms)} rooms visited")
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
