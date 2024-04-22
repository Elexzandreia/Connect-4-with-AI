This is a Connect 4 game where a user can play against either a person on the same device or an AI opponent.

File organization:

- The image assets for each button and the background are in the ‘imageAssets’ folder. 
- The class to create the buttons is in its own file, ‘button.py’.
- The functions used specifically for the AI opponent are contained within ‘connect4AI.py’.
- The game’s main implementation and code is contained within ‘connect4game.py’.
- The shared functions used by both the ‘connect4game.py’ and the ‘connect4AI.py’ files are located in the file named ‘sharedFunctions.py’ so both files could import and utilize its functions (in order to avoid a circular import error).
- Lastly, there is an mp3 file, 'star-travelers.mp3', for the music that the users can enjoy while playing.


How to begin:

1. Clone this repository
    https://github.com/Elexzandreia/Connect-4-with-AI.git

2. Open repository in your desired code editor

3. Install dependencies
    - python3
    - pygame

4. Run connect4game.py

5. Have fun!


Credits:

Youtube tutorials followed from:
- https://www.youtube.com/watch?v=GMBqjxcKogA 
- https://www.youtube.com/@KeithGalli
- https://www.youtube.com/watch?v=UYgyRArKDEs&list=PLFCB5Dp81iNV_inzM-R9AKkZZlePCZdtV&pp=iAQB

Music from #Uppbeat (free for Creators!):
https://uppbeat.io/t/adi-goldstein/star-travelers
License code: B2ALRT5SQOZTCJ5I