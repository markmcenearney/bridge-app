from enum import Enum

SWNE = ['S','W','N','E']
WNES = ['W','N','E','S']
WNESWNES = ['W','N','E','S','W','N','E','S']
hvVul = { 'None' : '-' , 'All' : 'b' , 'NS' : 'n' , 'EW' : 'e'}
oneSuit = ['A','K','Q','J','T','9','8','7','6','5','4','3','2']

def cardoutranks(card,othercard,trump):

    #print ('card,othercard:',card,othercard)
    if card[0] == othercard[0]:  #same suit
        if oneSuit.index(card[1]) < oneSuit.index(othercard[1]): return True
    elif card[0] == trump: return True

    return False

def winningcardindex(cards,cardled,trump):
    index = cards.index(cardled)
    highestrankedcard  = cardled
    for m in range(len(cards)):
        if cardoutranks(cards[m],highestrankedcard,trump):
            #print('m, len(cards): ',m,len(cards))
            #print('{} outranks {}'.format(cards[m],highestrankedcard))
            highestrankedcard = cards[m]
            index = m
    return index

class Auction_Type(Enum):
    NoAuction = 1
    PassedOut = 2
    Uncontested = 3
    Contested = 4

class Auction:
    def __init__(self, auction, dealer):
        self.auction = self.remap(auction)
        self.dealer = dealer
        self.dealer_index = WNES.index(dealer)
        self.compressed_auction = self.compress_auction(self.auction)

    def compress_auction(self,auction):
        #tbd fix passed out cases
        if auction == ['ap']:
            return auction
        ca = []
        for i in range(0,len(auction)-1):
            if auction[i] != 'p':
                for j in range(i,len(auction)-1):
                    ca.append(auction[j])
                for j,e in reversed(list(enumerate(ca))):
                    if e != 'p': break
                    del ca[j]
                return ca
        return ca

    def HV(self):
        # example: 'mb|p|mb|1S|mb|p|mb|2N|an|jacoby 2nt|mb|p|mb|4S|mb|p|mb|p|mb|p|'
        hvstr = ''
        for call in self.auction:
            if call == 'ap':
                hvstr = hvstr + 'mb|p|mb|p|mb|p|'
            else:
                hvstr = hvstr + 'mb|' + call + '|'
        return hvstr

    def auction_type(self):
        if self.compressed_auction == []:
            return Auction_Type['NoAuction']
        elif self.compressed_auction == ['AP']:
            return Auction_Type['PassedOut']
        else:
            n = 0
            for call in self.compressed_auction:
                n += 1
                #print ('n: ',n,'call: ',call)
                if call != 'p' and n % 2 == 0:
                    return Auction_Type['Contested']
            return Auction_Type['Uncontested']

    def opener_index(self):
        i = 0
        for call in self.auction:
            if call != 'p' and call != 'ap':
                return (self.dealer_index + i) % 4
            i += 1
        return None

    def OpeningBid(self):
        return self.compressed_auction[0]

    def intevener_index(self):
        i = 0
        for call in self.compressed_auction[1:]:
            if call != 'p' and call != 'ap' and i % 2 == 0:
                return (self.opener_index() + i + 1) % 4
            i += 1
        return None

    def IsFiveLevelHand(self):
        if self.auction == None:
             return False
        else:
            for call in self.auction:
                if len(call)>0 and call[0] in ['5','6','7']:
                    return True
            return False

    def remap(self,auction):
        bmap = { "pass" : 'p', "x" : 'd' , "xx" : 'r', "pass!" : 'p!', "x!" : 'd!', "xx!" : 'r!'}
        a = []
        for call in auction:
            call_lower = call.lower()
            if call_lower in bmap:
                a.append(bmap[call_lower])
            else:
                if call_lower[1:] == 'nt':
                    a.append(call_lower[0:2])
                else:
                    a.append(call_lower)
        return a

class Board:
    def __init__(self, data):

        self.id = data['Filename'] + ' ' + data['Board']
        self.data = data
        self.board = data['Board']
        self.players = [data['South'],data['West'],data['North'],data['East']]
        self.auction = Auction(data['Auction'],data['Dealer'])
        self.hands = self.get_hands(data['Deal'])

    def get_hands(self,deal):
        input_orientation = deal[0]
        hands_str = deal[2:].split()
        hands=[]
        for wnes in WNES:
            hand_index = WNESWNES[WNES.index(input_orientation):].index(wnes)
            suits = hands_str[hand_index].split('.')
            seat = WNESWNES[self.auction.dealer_index:].index(wnes) + 1
            player = self.players[WNES.index(wnes)]
            hands.append(Hand(suits,wnes,seat,player))
        return hands

    def get_vul(self,seat):
        pass

    def encode_deal(self):
        ed = ''
        for hand in self.hands:
            isuit=0
            for suit in hand.suits:
                for card in suit:
                    ed = ed + chr(48+oneSuit.index(card)+isuit*13)
                isuit +=1
        return ed

    def opener(self):
        return self.hands[self.auction.opener_index()]

    def responder(self):
        return self.hands[(self.auction.opener_index() + 2) % 4]

    def intervener(self):
        return self.hands[self.auction.intevener_index()]

    def advancer(self):
        return self.hands[(self.auction.intevener_index() + 2) % 4]

    def opener_lho(self):
        return self.hands[(self.auction.opener_index() + 1) % 4]

    def opener_rho(self):
        return self.hands[(self.auction.opener_index() + 3) % 4]

    def west(self):
        return self.hands[0]

    def north(self):
        return self.hands[1]

    def east(self):
        return self.hands[2]

    def south(self):
        return self.hands[3]

    def IsPreempt(self):
        if self.auction.compressed_auction == ['AP'] or self.auction.compressed_auction == None:
             return False
        else:
            opening_bid = self.auction.compressed_auction[0]
            if opening_bid[0] > '1' and self.opener().hcp() < 15:
                return True
        return False

    def IsOvercallersFirstCallAbove4H(self):
        if len(self.auction.compressed_auction) > 1:
            call = self.auction.compressed_auction[1]
            if call in ['4H','4NT'] or call[0] in ['5','6','7']:
                return True
        return False

    def IsRespondersFirstCallAbove4H(self):
        if len(self.auction.compressed_auction) > 2:
            call = self.auction.compressed_auction[2]
            if call in ['4H','4NT'] or call[0] in ['5','6','7']:
                return True
        return False

    def IsAdvancersFirstCallAbove4H(self):
        if len(self.auction.compressed_auction) > 3:
            call = self.auction.compressed_auction[3]
            if call in ['4H','4NT'] or call[0] in ['5','6','7']:
                return True
        return False

    def MakeHVURL(self):
        hvurl='https://www.bridgebase.com/tools/handviewer.html?bbo=y&lin='
        hvpn='pn|' + self.players[0] + ',' + self.players[1] + ',' + self.players[2] + ',' + self.players[3] +'|'
        hvst='st||'
        hvmd='md|' + '{}'.format(SWNE.index(self.auction.dealer)+1) + self.south().cardsHV() + ',' + self.west().cardsHV()+ ',' + self.north().cardsHV()  + ',|'
        print('self.auction.dealer: ',self.auction.dealer)
        hvrh = 'rh||ah|Board {}|'.format(self.board)
        hvsv = 'sv|{}|'.format(hvVul[self.data['Vulnerable']])
        hvmb = self.auction.HV()

        trump = self.data['Contract'][1]
        tricks = self.data['Play']
        cards = tricks[0].split()

        play = cards #order of play of first 4 cards is same as order in trick[0]
        cardled = cards[0]  #by convention in PBN format
        indexofwinningcard = winningcardindex(cards,cardled,trump)
        for trick in tricks[1:-1]:
            cards = trick.split()
            cardled = cards[indexofwinningcard]
            for i in range(4):
                k = (i + indexofwinningcard) % 4
                play.append(cards[k])
            indexofwinningcard = winningcardindex(cards,cardled,trump)
        #last trick
        cards = tricks[-1].split()
        for i in range(4):
            k = (i + indexofwinningcard) % 4
            if cards[k] != '--':
                play.append(cards[k])
        print ('MakeHVURL.play: ',play)
        hvpc = ''
        for card in play:
            hvpc = hvpc + 'pc|{}|'.format(card)
        hvmc='mc|11|'
        hvstr=hvurl+hvpn+hvst+hvmd+hvrh+hvsv+hvmb+hvpc
        print(hvstr)

class Hand:
    def __init__(self, suits, wnes, seat, player):
        self.suits = suits
        self.wnes = wnes
        self.seat = seat
        self.player = player

    def cardsHV(self):
        #cards in HV format
        return 'S' + self.spades() + 'H' + self.hearts() + 'D' + self.diamonds() + 'C' + self.clubs()

    def cards17(self):
        #4bytes (1 per suit to hold count) + 13 bytes (one per card AKQ..2
        str = '{:x}{:x}{:x}{:x}{}{}{}{}'.format(len(self.spades()),len(self.hearts()),len(self.diamonds()),len(self.clubs()),self.spades(),self.hearts(),self.diamonds(),self.clubs())
        return str

    def spades(self):
        return self.suits[0]

    def hearts(self):
        return self.suits[1]

    def diamonds(self):
        return self.suits[2]

    def clubs(self):
        return self.suits[3]

    def hcp(self):
        hcp = 0
        for suit in self.suits:
            for card in suit:
                hcp += max(0,'JQKA'.find(card) + 1)
        return hcp

    def isBal(self):
        n_doubletons = 0
        for suit in self.suits:
            if len(suit) < 2:
                return False
            elif len(suit) == 2:
                n_doubletons += 1
        if n_doubletons > 1:
            return False
        else:
            return True

    def isSemiBal(self):
        n_doubletons = 0
        for suit in self.suits:
            if len(suit) < 2:
                return False
            elif len(suit) == 2:
                n_doubletons += 1
        if n_doubletons > 2:
            return False
        else:
            return True
