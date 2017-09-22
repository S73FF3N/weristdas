#! /usr/bin/python

## \file  example_simple.py
#  \brief A (very simple) example of using the menu system
#  \author Scott Barlow
#  \date 2009
#  \version 1.0.0
#
#  An example script to create a window and explore some of the features of the
#  menu class I've created.  This script just creates a very simple menu for
#  users that just want to see a plain and simply menu.  This could be made even
#  more simple, but I keep some features I deem "essential" (such as
#  non-blocking code and only updating the portion of the screen that changed).
#
#
#       Copyright 2009 Scott Barlow
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 3 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA or see <http://www.gnu.org/licenses/>.
#
#
#  Changelog
#     V1.0.0 - Initial Release
#     V1.0.1 - No change to this file
#     V1.0.2 - No change to this file
#     V1.0.3 - No change to this file
#


#-------------------------------------------------------------------------------
#---[ Imports ]-----------------------------------------------------------------
#-------------------------------------------------------------------------------
import sys, pygame
import os
from menu import *
from image import *
from Weristdas import wid

class wid_menu():
    def __init__(self):
        self.NumberPlayer = 4
        self.image_dir = "/home/pi/Desktop/venv/jpg_Weristdas/"
        

    ## ---[ main ]------------------------------------------------------------------
    #  This function runs the entire screen and contains the main while loop
    #
    def main(self):
       # Initialize Pygame
       pygame.init()
    
       # Create a window of 800x600 pixels
       screen = pygame.display.set_mode((800, 600))
    
       # Set the window caption
       pygame.display.set_caption("Wer ist das?")
       
       bkg = load_image('schlagdenRaab.bmp', 'images')
       bkg = pygame.transform.scale(bkg, (800,600))
       
       screen.blit(bkg, (0, 0))
       pygame.display.flip()
       
       self.NameVars = []
       init = 1
       init_loc = True
       
       def update_PlayerNameMenu():
           PlayersNameList = []
           for player in range(0,self.NumberPlayer):
               if init == 1:
                   self.NameVars.append('Player '+str(player+1))
                   new_Name = (self.NameVars[player], player+15, None)
               else:
                   new_Name = (self.NameVars[player], player+15, None)
               PlayersNameList.append(new_Name)
           back_button = ('Back', self.NumberPlayer+15, None)
           PlayersNameList.append(back_button)
           self.PlayersNameMenu = cMenu(50, 50, 20, 5, 'vertical', 100, screen, PlayersNameList)
       
       def update_menu_and_settings(state):
           rect_list, state = menu.update(e, state)
           rect_list, state = settings.update(e, state)
           pygame.display.update(rect_list)
        
       update_PlayerNameMenu()    
       
       menu = cMenu(50, 50, 20, 5, 'vertical', 100, screen,
                   [('Start Game', 1, None),
                    ('Options',    2, None),
                    ('Exit',       3, None)])
                    
       settings = cMenu(50, 50, 20, 5, 'vertical', 100, screen,
                        [('Number of Players', 4, None),
                         ('Player Names', 5, None),
                         ('Image Location',    6, None),
                         ('Back',              7, None)])
                        
       numberPlayersMenu = cMenu(50, 50, 20, 5, 'horizontal', 100, screen,
                             [('2', 8, None),
                              ('3', 9, None),
                              ('4', 10, None),
                              ('5', 11, None),
                              ('6', 12, None),
                              ('7', 13, None),
                              ('8', 14, None)])
                              
                              
       def print_Menu(menue, xpos, ypos):
           menue.set_position(xpos, ypos)
           menue.set_alignment('center', 'center')
           
       def print_location():
           screen.blit(menu.font.render(self.image_dir,True,(255, 0, 0)),(30,530))
           update_menu_and_settings(state)
           init_loc = False
    
       print_Menu(menu, 50, 30)                          
    
       # Create the state variables (make them different so that the user event is
       # triggered at the start of the "while 1" loop so that the initial display
       # does not wait for user input)
       state = 0
       prev_state = 1
       
           #rect_list, state = menue.update(e, state)
       # rect_list is the list of pygame.Rect's that will tell pygame where to
       # update the screen (there is no point in updating the entire screen if only
       # a small portion of it changed!)
       rect_list = []
    
       # Ignore mouse motion (greatly reduces resources when not needed)
       pygame.event.set_blocked(pygame.MOUSEMOTION)
    
       # The main while loop
       while 1:
          # Check if the state has changed, if it has, then post a user event to
          # the queue to force the menu to be shown at least once
          if prev_state != state:
             pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
             prev_state = state
    
          # Get the next event
          e = pygame.event.wait()
    
          # Update the menu, based on which "state" we are in - When using the menu
          # in a more complex program, definitely make the states global variables
          # so that you can refer to them by a name
          if e.type == pygame.KEYDOWN or e.type == EVENT_CHANGE_STATE:
             if state == 0:
                rect_list, state = menu.update(e, state)
             elif state == 1:
                print self.image_dir
                wid(self.NumberPlayer, self.NameVars, self.image_dir)
                state = 3
             elif state == 2:
                print_Menu(settings, 200, 30)
                rect_list, state = settings.update(e, state)            
             elif state == 3:
                print 'Exit!'
                pygame.quit()
                sys.exit()
             elif state == 4:
                print_Menu(numberPlayersMenu, 550, 30)
                rect_list, state = numberPlayersMenu.update(e, state)
             elif state == 5:
                print_Menu(self.PlayersNameMenu, 250, 250)
                rect_list, state = self.PlayersNameMenu.update(e, state)
             elif state == 6:
                 if init_loc == True:
                     self.image_dir = os.getcwd()
                 screen.blit(menu.font.render(self.image_dir,True,(255, 0, 0)),(30,530))
                 update_menu_and_settings(state)
                 back = False
                 while 1:
                     if back == True:
                         state = 2
                         break
                     for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                 if event.key in [pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d,
                                                             pygame.K_e, pygame.K_f, pygame.K_g, pygame.K_h,
                                                             pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l,
                                                             pygame.K_m, pygame.K_n, pygame.K_o, pygame.K_p,
                                                             pygame.K_q, pygame.K_r, pygame.K_s, pygame.K_t,
                                                             pygame.K_u, pygame.K_v, pygame.K_w, pygame.K_x,
                                                             pygame.K_y, pygame.K_z]:
                                    self.image_dir += event.unicode
                                    print_location()
                                    break
                                 if event.key == pygame.K_BACKSPACE:
                                     screen.blit(bkg, (0,0))
                                     self.image_dir = self.image_dir[:-1]
                                     print_location()
                                     break
                                 if event.key == pygame.K_RETURN:
                                     screen.blit(bkg, (0,0))
                                     update_menu_and_settings(state)
                                     back = True
                                 else:
                                     pass
             elif state == 7:
                screen.blit(bkg, (0,0))
                pygame.display.flip()
                state = 0
             elif state in range(8,16):
                self.NumberPlayer = state -6
                update_PlayerNameMenu()
                state = self.NumberPlayer + 15
             elif state == self.NumberPlayer + 15:
                screen.blit(bkg, (0,0))
                pygame.display.flip()
                rect_list, state = menu.update(e, state)
                state = 2
             elif state in range(15, self.NumberPlayer + 15):
                name_updated = False
                init = 2
                self.NameVars[state-15] = ""
                while 1:
                    if name_updated == True:
                        break
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key in [pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d,
                                             pygame.K_e, pygame.K_f, pygame.K_g, pygame.K_h,
                                             pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l,
                                             pygame.K_m, pygame.K_n, pygame.K_o, pygame.K_p,
                                             pygame.K_q, pygame.K_r, pygame.K_s, pygame.K_t,
                                             pygame.K_u, pygame.K_v, pygame.K_w, pygame.K_x,
                                             pygame.K_y, pygame.K_z]:
                                self.NameVars[state-11]+= event.unicode
                                update_PlayerNameMenu()
                                screen.blit(bkg, (0,0))
                                screen.blit(menu.font.render(self.NameVars[state-15],True,(255, 0, 0)),(400,250+((state-15)*29)))
                                update_menu_and_settings(state)
                            if event.key == pygame.K_BACKSPACE:
                                self.NameVars[state-15] = self.NameVars[state-15][:-1]
                                update_PlayerNameMenu()
                                screen.blit(bkg, (0,0))
                                screen.blit(menu.font.render(self.NameVars[state-15],True,(255, 0, 0)),(400,250+((state-15)*29)))
                                update_menu_and_settings(state)
                            if event.key == pygame.K_RETURN:
                                name_updated = True
                                state = 5
                                break
                        else:
                            pass
    
          # Quit if the user presses the exit button
          if e.type == pygame.QUIT:
             pygame.quit()
             sys.exit()
    
          # Update the screen
          pygame.display.update(rect_list)


## ---[ The python script starts here! ]----------------------------------------
# Run the script
if __name__ == "__main__":
   a = wid_menu()
   a.main()


#---[ END OF FILE ]-------------------------------------------------------------
