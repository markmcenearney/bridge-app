from enum import Enum
import os
import hand

linVul = { '0' : 'None', 'o' : 'None', 'n' : 'NS', 'e' : 'EW', 'b' : 'All' }
#linScore = { 'I': scoring_methods[2] , 'P' : scoring_methods[0] , 'B' : scoring_methods[6]}

def hand_index (seat_wnes,deal_orientation_index):
    return ((wnes.index(seat_wnes) + deal_orientation_index + 2) % 4)

def get_deals(dirname):

    auction = []
    board = '1'
    data = {}
    data['Board'] = board 
    play = []
   
    n_board = 0
    n_auction = 0
    line_num = 0
    deal = ""
    for filename in os.listdir(dirname):
        if filename.endswith(".PBN"):
            f = open(os.path.join(dirname, filename))
            data['Filename'] = filename
            #print(os.path.join(dirname, filename))
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
                        board = line[line.find('"')+1 : line.rfind('"')]
                    data['Board'] = board    
                    #print (data['Board'] )
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
                elif line.startswith("["):
                        pass
                elif line.startswith("*"):
                    data['Auction'] = auction
                    #print(auction)
                    data['Play'] = play
                    d = hand.Board(data)

                    if d.auction.auction_type() == hand.Auction_Type['Contested'] and d.auction.OpeningBid() == '1n' and 13 < d.opener().hcp() < 18 and (d.opener().isBal() or d.opener().isSemiBal()):
                        pass

                    if d.auction.auction_type() == hand.Auction_Type['Contested']:
                        if (d.IsPreempt and d.IsRespondersFirstCallAbove4H() and d.opener().hcp()+d.responder().hcp() < 19) or (d.IsAdvancersFirstCallAbove4H() and d.opener().hcp()+d.responder().hcp() >21):
                            pass

                    #if d.auction.auction_type() == hand.Auction_Type['Contested'] and d.auction.OpeningBid() == '2d' and (len(d.opener().spades()) == 6 or len(d.opener().hearts()) == 6 ):
                        #overcall = d.auction.compressed_auction[1]
                        #print (d.auction.dealer,d.opener().seat,d.intervener().seat,overcall,d.intervener().cards17(),d.intervener().hcp() ,d.auction.compressed_auction)
                        #d.MakeHVURL()

                    if d.auction.OpeningBid() in ['1h','1s']:
                        if len(d.auction.compressed_auction) >= 5:
                            #print('d.auction.compressed_auction[2]: ',d.auction.compressed_auction[2])
                            if d.auction.compressed_auction[1] == 'p' and d.auction.compressed_auction[2] == '2n' and d.auction.compressed_auction[4] == '3n' :
                                print('File and board: ', d.id)
                                print (d.auction.dealer,d.opener().seat,d.opener().cards17(),d.opener().hcp(),d.responder().cards17(),d.responder().hcp(),d.auction.compressed_auction)
                                d.MakeHVURL()
                else:
                    if tok == 'Auction':
                        auction = auction + line.rstrip().split()
                    elif tok == 'Play':
                        play = play + [line.rstrip()]

get_deals('deals')
