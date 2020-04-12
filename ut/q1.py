from enum import Enum
import os
import hand

linVul = { '0' : 'None', 'o' : 'None', 'n' : 'NS', 'e' : 'EW', 'b' : 'All' }
#linScore = { 'I': scoring_methods[2] , 'P' : scoring_methods[0] , 'B' : scoring_methods[6]}

def hand_index (seat_wnes,deal_orientation_index):
    return ((wnes.index(seat_wnes) + deal_orientation_index + 2) % 4)

def get_deals(dir):
    #dir = os.fsencode(path)
    #dirname = os.fsdecode(dir)
    #print(dirname)

    auction = []
    data = {}
    play = []
    board = ""
    n_board = 0
    n_auction = 0
    line_num = 0
    deal = ""
    for filename in os.listdir(dir):
        #filename = os.fsdecode(file)
        if filename.endswith(".PBN"):
            f = open(os.path.join(dir, filename))
            data['Filename'] = filename
            data['Board'] = '1'
            print(os.path.join(dir, filename))
            lines = f.readlines()
            tok = ''
            for line in lines:
                #startsWith = line[0:10]
                #print ('startsWith: ',startsWith)
                #print('line: ',line)
                line_num += 1
                if line.startswith("[Auction"):
                    #print(line)
                    n_auction += 1
                    auction = []
                    tok = 'Auction'
                elif line.startswith("[Board"):
                    if line[line.find('"')+1 : line.rfind('"')] != '#':
                        data['Board'] = line[line.find('"')+1 : line.rfind('"')]
                elif line.startswith("[West"):
                    data['West'] = line[line.find('"')+1 : line.rfind('"')]
                elif line.startswith("[North"):
                    data['North'] = line[line.find('"')+1 : line.rfind('"')]
                elif line.startswith("[East"):
                    data['East'] = line[line.find('"')+1 : line.rfind('"')]
                elif line.startswith("[South"):
                    data['South'] = line[line.find('"')+1 : line.rfind('"')]
                elif line.startswith("[Contract"):
                    data['Contract'] = line[line.find('"')+1 : line.rfind('"')]
                elif line.startswith("[Dealer"):
                    data['Dealer'] = line[line.find('"')+1 : line.rfind('"')]
                elif line.startswith("[Deal"):
                    #print('line: ',line)
                    data['Deal'] = line[line.find('"')+1 : line.rfind('"')]
                elif line.startswith("[Play"):
                    tok = 'Play'
                    play = []
                elif line.startswith("[Vulnerable"):
                    data['Vulnerable'] = line[line.find('"')+1 : line.rfind('"')]
                    print('line: ',line)
                elif line.startswith("["):
                        pass
                elif line.startswith("*"):
                    data['Auction'] = auction
                    data['Play'] = play

                    print ("['Deal']: ",data['Deal'])
                    print ("['Dealer']: ",data['Dealer'])
                    print ("['Board']: ",data['Board'])
                    print ("['Vulnerable']: ",data['Vulnerable'])
                    print ("['West']: ",data['West'])
                    print ("['North']: ",data['North'])
                    print ("['East']: ",data['East'])
                    print ("['South']: ",data['South'])
                    print ("['Auction']: ",data['Auction'])
                    print("['Auction']: ",data['Play'])

                    d = hand.Board(data)
                    print ('d.id: ',d.id)

                    print ('dealer: ',d.auction.dealer)
                    print ('auction: ',d.auction.auction)
                    print('compressed_auction: ',d.auction.compressed_auction)
                    print('len(compressed_auction): ',len(d.auction.compressed_auction))
                    print ('auction_type: ',d.auction.auction_type())

                    print('d.opener().seat: ',d.opener().seat)
                    print('d.opener().wnes: ',d.opener().wnes)
                    print('d.opener().colors()',d.opener().colors)
                    print('d.opener().player: ',d.opener().player)
                    print('d.opener().cards17(): ',d.opener().cards17())
                    print('len(d.opener().spades()): ',len(d.opener().spades()))

                    print('d.responder().seat: ',d.responder().seat)
                    print('d.responder().wnes: ',d.responder().wnes)
                    print('d.responder().player: ',d.responder().player)
                    print('d.responder().cards17(): ',d.responder().cards17())
                    print('len(d.responder().spades()): ',len(d.responder().spades()))

                    print('opener is bal? ',d.opener().isBal())
                    print('opener is semibal? ',d.opener().isSemiBal())
                    d.MakeHVURL()

                else:
                    if tok == 'Auction':
                        auction = auction + line.rstrip().split()
                    elif tok == 'Play':
                        play = play + [line.rstrip()]

get_deals('deals')
