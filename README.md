# DesktopPet Companion

A fun, cute,interactive Python desktop pet that hangs out on your screen while you code or work. 
Built using tkinter, it runs on a transparent canvas so it looks like the pet is walking right on top of your desktop wallpaper,
instead of sitting inside a window block.

# Current Features
* Zero Borders: Transparent backgrounds make the pet look completely integrated into your desktop space.
* The Launcher Window: A clean startup menu (launcher.py) so you can select your pet before spawning it.
* Poke to Speak: Left-clicking the pet triggers a dynamic speech bubble over its head.
* Under-the-Hood Stats: Built-in tracking variables for happiness levels, movement speed, walking direction, and interaction clicks.
* Expanded Roster: Support for multiple pet selection buttons including Green Apple, Golden Mango, and Blue Citrus.
* 
  ## Roadmap
- [x] Implement basic screen boundary detection and directional movement loop.
- [ ] Add more pets to choose from in the launcher screen.
- [x] Make the pet blurt out random thoughts on a timer.
- [ ] Build a care mechanic where happiness drops over time if you ignore it.
- [ ] Package everything into a standalone .exe installer so friends can download it easily.
- [ ] A small test to decide pet according to user personality

## Built With
* Python 
* Tkinter (for the UI)
* Pillow/PIL (for handling image assets and animations)

## How to Run It
1. Make sure you're inside the project directory.
2. Fire up the launcher from your terminal:
   ```powershell
   python launcher.py
