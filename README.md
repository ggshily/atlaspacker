atlaspacker
===========
A Simple tool to generate libGDX TextureAtlas.

### Requirements
atlaspacker needs Python (either 2.7 or 3, both are fine), and the [Pillow](http://python-imaging.github.io/) module, which you can easily install using [pip](https://pypi.python.org/pypi/pip) if it's not already available on your system. If you're using a Debian-based system, you can just ```sudo apt-get install python-imaging``` or ```sudo apt-get install python3-imaging```.

### Installation
GNU/Linux:
```bash
wget -O atlaspacker https://raw.github.com/ansdor/atlaspacker/master/atlaspacker.py
chmod +x atlaspacker
sudo mv atlaspacker /usr/bin/
```
Any other OS:
No idea, but you can probably figure it out.

### Usage
```bash
atlaspacker [-p2] [-sq] [-s] [-o] [-f {linear|nearest}] INPUT [...] OUTPUT
```

```INPUT``` can be a list of files, a folder, a list of folders or both mixed up. All images contained in the folder/list will be used in the TextureAtlas.

```OUTPUT``` is the name of the image and the text file to be created by the program.

Example:
```
atlaspacker background1.png background2.png sprites/ my_graphics
```

This would create a TextureAtlas named my_graphics.png and a descriptor file named my_graphics.txt using background1.png, background2.png and all the images inside the folder sprites.

### Optional arguments
```-p2``` forces a power-of-2 sized image (required by old versions of OpenGL).

```-sq``` forces a square output.

```-s {SPACING}``` defines the amount of spacing (in pixels) between the images and the border.

```-o``` will overwrite files with the same name without any prompts (useful when you have a script to automatically update your atlas)

```-f {linear|nearest}``` selects the TextureFilter used in the descriptor file. Defaults to Nearest.
