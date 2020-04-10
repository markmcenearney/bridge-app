class Players:
    names = {}
    
    def get_player_id(name):
        return (Players.names[name])
        
    def add_players(name_list):
        for name in name_list:
            if name not in Players.names:
                Players.names[name] = len(Players.names) + 1

west = 'Mark'
north = 'Carl'
east = 'Linda'
south = 'Bob'

Players.add_players([west,north,east,south])
print (west, Players.get_player_id(west))
print (north, Players.get_player_id(north))
print (east, Players.get_player_id(east))
print (south, Players.get_player_id(south))

west = 'Mark'
north = 'Carl'
east = 'Linda'
south = 'Jim    '

Players.add_players([west,north,east,south])
print (west, Players.get_player_id(west))
print (north, Players.get_player_id(north))
print (east, Players.get_player_id(east))
print (south, Players.get_player_id(south))