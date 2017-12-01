import os, pygame, random
# Import a library of functions called 'pygame'
from PIL import Image
from pygame.locals import * #need this for 'FULLSCREEN' value
from time import sleep
from game_utilities import convert_image_to
from image import load_image

def wid(players, playerNamesList, im_dir):
	# Initialize the game engine
	pygame.init()
	
	# initialize joystick
	try:
		if pygame.joystick.get_count() == 1:
	    		print "One Controller recognized!"
	    		pygame.joystick.init()
	    		js = pygame.joystick.Joystick(0)
	    		js.init()
	
		print "number of joysticks:", pygame.joystick.get_count()
		print "Gamepad:", js.get_name()
	except:
		print "no buzzers connected!"
	    
	# declare and array for player names and initial score
	playerNames = playerNamesList
	playerScore = [0]*players
	# key definitions
	playerKeys = [0, 5, 10, 15] # these definitions are valid for PS2 Buzz! Controllers
	answer = [K_r, K_f] # K_r: correct, K_f: incorrect
	
	# Define the colours used in RGB format
	black = [ 0, 0, 0]
	white = [255,255,255]
	red = [255, 0, 0]
	
	print "number of players:", players
	
	# set the screen the highest resolution for this display
	screen=pygame.display.set_mode((1200,800), pygame.FULLSCREEN)
	# Get the width and height of the screen as we don't know it for fullscreen
	screenx, screeny = screen.get_size()
	# starting with a gap of 20 on the left and 20 on the right figure out the location for the squares.
	squarewidth = int(screenx/10)
	squaresize = int(squarewidth/5*4)
	
	# define picture format
	picture_width = 800
	picture_length = 600
	
	# text displayed at the beginning
	welcome = "Welcome to 'Wer ist das?'"
	
	# build image dictionary from image directory
	# images in image directory are converted into .bmp    
	im_path = im_dir
	
	im_dir_content_list = os.listdir(im_path)
	
	logo = "Schlag-den-Raab.bmp"
	picture = load_image(logo, 'images')
	
	os.chdir(im_path)
	
	image_dict = {}
	
	# function to build image dictionary with solution as key and image as value
	def build_image_dict(image):
		base=os.path.basename(im_path+image)
		name_o=os.path.splitext(base)[0]
		name=name_o.replace("_"," ")
		image_dict[name] = im_path+image

	for file_in in im_dir_content_list:
		# to avoid loading mac specific files that may be created
		if file_in == ".DS_Store":
	    		continue
		elif file_in.startswith("._") == True:
			continue
		# convert images to pygame friendly image format .bmp
		else:
	    		converted_file = convert_image_to(file_in, "bmp")
	    		build_image_dict(converted_file) 
                   
	amount_of_pictures = len(image_dict)
	print "number of pictures:", amount_of_pictures
	# randomly chosing image from image dictionary and updating image label
	# image that has been played is deleted from dictionary
	def random_pick_image():
		global random_im_key
		global random_im_val
		try:    
	    		random_im_key = random.choice(image_dict.keys())
	    		random_im_val = image_dict[random_im_key]
	    		del image_dict[random_im_key]
		except:
	    		random_im_val = os.path.join('images', logo)
	    		random_im_key = "All images played! Ending"
		random_image = load_image(random_im_val, im_dir)
		image_size = random_image.get_rect().size
		rela = image_size[0]/float(image_size[1])
		# adjusting image width/height to screen
		# image wider than high
		if rela >= 1:
		    image_size = (picture_width, int(min(picture_length, picture_width/rela)))
		# image higher than wide
		if rela < 1:
	    		image_size = (int(min(picture_width, picture_length/rela)), picture_length)            
	
		random_image = pygame.transform.scale(random_image, image_size)
		pygame.draw.rect(screen, white, ((screenx/2)-(picture_width/2), 5,picture_width, picture_length), 0)
		screen.blit(random_image, ((screenx/2)-(image_size[0]/2), (605-image_size[1])))
		if not bool(image_dict) and random_im_val == logo:
		    solution_label = myfont.render("All images played! Ending!", 1, red)
		    screen.blit(solution_label, (screenx/2 - len(random_im_key)*10/2, picture_length+squaresize+70))
		if random_im_key == '.DS Store':
		    random_pick_image()
		return random_im_key
	
	# print solution in solution label     
	def show_solution():
		solution = myfont.render(random_im_key, 1, red)
		screen.blit(solution, (screenx/2 - len(random_im_key)*10/2, picture_length+squaresize+70))
	
	#countdown printed in solution label
	def countdown(count_from):
		for i in range(1,count_from + 1):
		    time_left = count_from - i
		    time_left =str(time_left)
		    countdown = myfont.render(time_left, 1, red)
		    screen.blit(countdown, (screenx/2 -20, picture_length+squaresize+70))
		    pygame.display.flip()
		    pygame.time.wait(1000)
		    pygame.draw.rect(screen, white, (0, picture_length+squaresize+70, 1000,50),0)
	    	    pygame.display.flip()
	
	# Fill the screen White
	screen.fill(white)
	# Put something in the application Bar
	pygame.display.set_caption("Wer ist das?")
	
	# Set the font for the text. Windows computer so usd Ariel
	myfont = pygame.font.SysFont("Ariel", 35)
	# set font for score
	scorefont = pygame.font.SysFont("Ariel", 40)
	
	# Created Variable for the text on the screen
	picture = pygame.transform.scale(picture, (picture_width, picture_length))
	solution_label = myfont.render(welcome, 1, red)
	lockout = myfont.render("X", 1, black)
	picture_nr = 1
	progress = myfont.render(str(picture_nr)+"/"+str(amount_of_pictures))
	# put the picture and text on the screen
	screen.blit(progress, ((screen/2)-10, 5))
	screen.blit(picture, ((screenx/2)-(picture_width/2), 20))
	screen.blit(solution_label, (screenx/2 - len(welcome)*10/2, picture_length+squaresize+80))
	
	# Draw name of players, 4 empty rectangles and players score
	for n in range (0, players):
		if players % 2 == 0:
		    xpos = (screenx/2)-(((players/2)-n)*squarewidth)
		if players % 2 != 0:
		    xpos = (screenx/2)-(((players/2)-n)*squarewidth)-(squarewidth/2)
		screen.blit(myfont.render(playerNames[n],1,black),(xpos,picture_length+5))
		pygame.draw.rect(screen, black, (xpos, picture_length+30,squaresize,squaresize), 0)
		screen.blit(scorefont.render(str(playerScore[n]),1,black),(xpos, picture_length+squaresize+30))
	
	# show the whole thing
	pygame.display.flip()
	
	first = 0 # used to signify the first key pressed and stops other being used
	waitReset = 1 # Reset section for the while loop
	show_solution_var = 1 # variable to indicate if game is in the solution phase
	initialize = 1 # variable to indicate if game has been initialized by referee
	
	while True:
		while initialize == 1:
			for event in pygame.event.get():   
			        if event.type == pygame.KEYDOWN:
					# terminate game with escape
				 	if event.key == K_ESCAPE:
						pygame.quit()
					# referee uses return key to control the game
					if event.key == K_RETURN:
						pygame.draw.rect(screen, white, (0, picture_length+squaresize+65, 1500,50),0)
		                    		pygame.display.flip()                            
		                    		random_pick_image()                                              
		                    		pygame.display.flip()
						initialize = 0
					else:
                                                pass
						
		# Stay in the loop until one of the 'buzzer' keys is pressed or referee shows next image manually
		while first == 0:
		    for event in pygame.event.get():   
		        if event.type == pygame.KEYDOWN:
			 	if event.key == K_ESCAPE:
					pygame.quit()
				if event.key == K_RETURN:
					first = 1
					try:
						show_solution_var = 1
					except:
						show_solution_var = 2
		        # one buzzer is pressed        
		        if event.type == pygame.JOYBUTTONDOWN
		            buttonpressed = event.button
		                
		            for n in range (0,players):
		                if buttonpressed == playerKeys[n]:
		                    first_buzz = playerKeys.index(buttonpressed)
		                    if players % 2 == 0:
		                        xpos = (screenx/2)-(((players/2)-first_buzz)*squarewidth)
		                    if players % 2 != 0:
		                        xpos = (screenx/2)-(((players/2)-first_buzz)*squarewidth)-(squarewidth/2)
		
				    # indicates which player buzzered first with an red square
		                    pygame.draw.rect(screen, red, (xpos, picture_length+30,squaresize,squaresize), 0)
		                    first = 1
				    # countdown starts to leave player 5 seconds to answer
		                    countdown(5)
		                
		            pygame.display.flip()
		            # a 'buzzer' was pressed and shown on screen
		            # now go to the reset code
		
		# loop waiting until the 'buzzers' are reset
		waitReset=0
		# put an x on the screen to show it is in lockout mode
		screen.blit(scorefont.render("X",1,black),(screenx-40, 10))
		pygame.display.flip()
		
		# reset mode (decision if answer was correct and points are given by referee, red square is reset to black)
		while waitReset == 0:
		        for event in pygame.event.get():	
		            if event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
		                pygame.quit()
		                
		            # User pressed down on a key
			    if event.type == pygame.KEYDOWN:
		                keypressed = event.key
		                                       
		                # points are given for player who buzzered
		                if keypressed in answer:
		                    # blank out score label
		                    pygame.draw.rect(screen, white, (xpos, picture_length+squaresize+30, squaresize, 30),0)
		                    if keypressed == answer[0]:
		                        playerScore[first_buzz] = playerScore[first_buzz] + 1
		                    if keypressed == answer[1]:
		                        playerScore[first_buzz] = playerScore[first_buzz] - 1
		                    screen.blit(scorefont.render(str(playerScore[first_buzz]),1,black),(xpos, picture_length+squaresize+30))
		                    pygame.display.flip()
		                
		            # After buzzer was pressed, referee shows solution and decides if answer was right or wrong
		                if keypressed == K_RETURN and show_solution_var == 2:
		                    pygame.draw.rect(screen, white, (0, picture_length+squaresize+65, 1500,50),0)
		                    pygame.display.flip()
		                       # Draw the 4 empty rectangles for the players
		                    for n in range (0, players):
		                    	pygame.draw.rect(screen, black, (xpos, picture_length+30,squaresize,squaresize), 0)  
		                    first=0
		                    waitReset=1
		                                           
		                    pygame.display.flip()
		                    show_solution_var = 0
		            # solution is shown    
				if keypressed == K_RETURN and show_solution_var == 1:
		                    try:
		                        show_solution()
		                    except:
		                        pass
		                    pygame.display.flip()
		                    show_solution_var = 2
		            # next picture is shown        
		                if keypressed == K_RETURN and show_solution_var == 0:
		                    pygame.draw.rect(screen, white, (0, picture_length+squaresize+65, 1500,50),0)
		                    pygame.display.flip()                            
		                    random_pick_image()                                              
		                    pygame.display.flip()
		                    show_solution_var = 1
                
    
if __name__ == "__main__":
    wid(players, PlayersNameList, im_dir)
