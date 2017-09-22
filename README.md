# weristdas
Wer ist das? is a multiplayer buzzer game inspired by the german tv show 'Schlag den Raab'.

An image is shown on the display and the player who buzzers first can tell within 5 seconds who he thinks is displayed. The host/referee decides if the answer is correct and assingns points accordingly.

All you need is a repository with images files of 'famous' persons which filenames contain the solution as follows: the file 'George_Clooney.jpg will display the solution 'George Clooney'.

The settings are configured for a Playstation Buzz! Controller and a Keyboard for the referee, but you can modify acording to you needs and the devices you have available.

The game is programmed using pygame and Pillow for image support.

HOW TO START

Prepare a directory with image files which shall appear in the game. The higher the resolution, the better the game experience will be. Images that are wider than high are favourable.

Then, in your console execute the file 'GUI_Weristdas.py':
  python GUI_Weristdas.py
  
The file 'GUI_Weristdas.py' is used to set up the game with an GUI. The names of the players and the directory of the image files to be used in the game are set using the GUI. Executing 'Start game' will suprisingly start the game by calling the file 'Weristdas.py'.

Since I am a really unexperienced programmer, I developed this game just for fun and by trial and error priciple. So don't blame me for the bad style of programming but feel free to help me improve this game.
