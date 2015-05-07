
####################################################

	
def recoverAll(group, x = 0, y = 0):
	mute()
	notify("{} recovers all of his/her cards".format(me))
	for card in group: 
		if card.controller == me:
			card.orientation &= ~Rot90			
			
def clearAll(group, x = 0, y= 0):
    notify("{} clears all targets and combat.".format(me))
    for card in group:
		if card.controller == me:
			card.target(False)
			card.highlight = None

def roll20(group, x = 0, y = 0):
    mute()
    n = rnd(1, 20)
    notify("{} rolls {} on a 20-sided die.".format(me, n))

def flipCoin(group, x = 0, y = 0):
    mute()
    n = rnd(1, 2)
    if n == 1:
        notify("{} flips heads.".format(me))
    else:
        notify("{} flips tails.".format(me))

def tap(card, x = 0, y = 0):
    mute()
    card.orientation ^= Rot90
    if card.orientation & Rot90 == Rot90:
		notify('{} rests {}'.format(me, card))
    else:
        notify('{} recovers {}'.format(me, card))
		  
def jactivate(card, x = 0, y = 0):
    mute()
    if card.isFaceUp:
        notify("{} J-Activates {} to {}".format(me, card, card.alternateProperty("jruler", "name")))
        card.switchTo('jactivate')
    else:
        card.switchTo()
        notify("{} reverts {} back to {}.".format(me, card.alternateProperty("jruler", "name"), card))
		
def jactivate(card, x = 0, y = 0):
    mute()
    if card.isFaceUp:
        notify("{} flips {} face down.".format(me, card))
        card.isFaceUp = False
    else:
        card.isFaceUp = True
        notify("{} flips {} face up.".format(me, card))

def discard(card, x = 0, y = 0):
	card.moveTo(me.piles['Discard Pile'])
	notify("{} discards {}".format(me, card))

def addCounter(card, x = 0, y = 0):
	mute()
	notify("{} adds 1 counter to {}.".format(me, card))
	card.markers[CounterMarker] += 1

def removeCounter(card, x = 0 , y = 0):
	mute()
	notify("{} removes 1 counter from {}.".format(me, card))
	card.markers[CounterMarker] -= 1
	  
def setCounter(card, x = 0, y = 0):
	mute()
	quantity = askInteger("How many counters", 0)
	notify("{} sets {} counters on {}.".format(me, quantity, card))
	card.markers[CounterMarker] = quantity	
		
def play(card, x = 0, y = 0):
	mute()
	src = card.group
	card.moveToTable(0, 0)
	notify("{} plays {} from their {}.".format(me, card, src.name))
	
def playFaceDown(card, x = 0, y = 0):
	mute()
	src = card.group
	card.isFaceUp = False
	card.moveToTable(0,0)
	notify("{} plays {} from their {} face down.".format(me, card, src.name))

def mulligan(group):
    mute()
    newCount = len(group) - 1
    if newCount < 0: return
    if not confirm("Mulligan down to %i ?" % newCount): return
    notify("{} mulls down to {}".format(me, newCount))
    librarycount = len(me.piles["Life Deck"])
    for card in group:
        n = rnd(0, librarycount)
        card.moveTo(me.piles["Life Deck"], n)
    me.piles["Life Deck"].shuffle()
    for card in me.piles["Life Deck"].top(newCount):
        card.moveTo(me.hand)

def randomDiscard(group):
	mute()
	card = group.random()
	if card == None: return
	notify("{} randomly discards {}.".format(me,card.name))
	card.moveTo(me.piles['Discard Pile'])

def draw(group, x = 0, y = 0):
	if len(group) == 0: return
	mute()
	group[0].moveTo(me.hand)
	notify("{} draws a card.".format(me))

def drawMany(group, count = None):
	if len(group) == 0: return
	mute()
	if count == None: count = askInteger("Draw how many cards?", 0)
	for card in group.top(count): card.moveTo(me.hand)
	notify("{} draws {} cards.".format(me, count))

def drawBottom(group, x = 0, y = 0):
	if len(group) == 0: return
	mute()
	group.bottom().moveTo(me.hand)
	notify("{} draws a card from the bottom.".format(me))

def shuffle(group):
	group.shuffle()
  
#---------------------------------------------------------------------------
# Phases
#---------------------------------------------------------------------------

def showCurrentPhase(phaseNR = None): # Just say a nice notification about which phase you're on.
   if phaseNR: notify(phases[phaseNR])
   else: notify(phases[num(me.getGlobalVariable('phase'))])

def endMyTurn(opponent = None):
   if not opponent: opponent = findOpponent()
   me.setGlobalVariable('phase','0') # In case we're on the last phase (Force), we end our turn.
   notify("=== {} has ended their turn ===.".format(me))
   opponent.setActivePlayer() 
      
def nextPhase(group = table, x = 0, y = 0, setTo = None):  
# Function to take you to the next phase. 
   mute()
   phase = num(me.getGlobalVariable('phase'))
   if phase == 4: 
      endMyTurn()
      return  
   else:
      if not me.isActivePlayer and confirm("Your opponent does not seem to have ended their turn yet. Switch to your turn?"):
         remoteCall(findOpponent(),'endMyTurn',[me])
         rnd(1,1000) # Pause to wait until they change their turn
      phase += 1
      if phase == 1: goToDraw()
      elif phase == 2: goToRecover()
      elif phase == 3: goToMain()
      elif phase == 4: goToEnd()

def goToDraw(group = table, x = 0, y = 0): # Go directly to the Balance phase
   mute()
   me.setGlobalVariable('phase','1')
   showCurrentPhase(1)
         
def goToRecovery(group = table, x = 0, y = 0): # Go directly to the Balance phase
   mute()
   me.setGlobalVariable('phase','2')
   showCurrentPhase(2)
         
def goToMain(group = table, x = 0, y = 0): # Go directly to the Balance phase
   mute()
   me.setGlobalVariable('phase','3')
   showCurrentPhase(3)
         
def goToEnd(group = table, x = 0, y = 0): # Go directly to the Balance phase
   mute()
   me.setGlobalVariable('phase','4')
   showCurrentPhase(4)
  

#---------------------------------------------------------------------------
# Meta Functions
#---------------------------------------------------------------------------
def findOpponent(position = '0', multiText = "Choose which opponent you're targeting with this effect."):
   opponentList = fetchAllOpponents()
   if len(opponentList) == 1: opponentPL = opponentList[0]
   else:
      if position == 'Ask':
         choice = SingleChoice(multiText, [pl.name for pl in opponentList])
         opponentPL = opponentList[choice]         
      else: opponentPL = opponentList[num(position)]
   return opponentPL

def fetchAllOpponents(targetPL = me):
   opponentList = []
   if len(getPlayers()) > 1:
      for player in getPlayers():
         if player != targetPL: opponentList.append(player) # Opponent needs to be not us, and of a different type. 
   else: opponentList = [me] # For debug purposes
   return opponentList   

def playerside():
   if me.hasInvertedTable(): side = -1
   else: side = 1   
   return side
   
 
#------------------------------------------------------------------------------
# Button and Announcement functions
#------------------------------------------------------------------------------

def BUTTON_OK(group = None,x=0,y=0):
   notify("--- {} has no further reactions.".format(me))

def BUTTON_Wait(group = None,x=0,y=0):  
   notify("--- Wait! {} wants to react.".format(me))

def BUTTON_Actions(group = None,x=0,y=0):  
   notify("--- {} is waiting for opposing actions.".format(me))

def declarePass(group, x=0, y=0):
   notify("--- {} Passes".format(me))    

def useCard(card,x=0,y=0):
   tap(card,x,y)
