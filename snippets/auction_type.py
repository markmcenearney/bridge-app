from enum import Enum
class Auction_Type(Enum):
    none = 1
    passed_out = 2
    uncontested = 3
    contested = 4

for auction_type in Auction_Type: 
    print(auction_type)
    