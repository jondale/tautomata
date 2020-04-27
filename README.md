# tautomata
Terminal Cellular Automata

Just some fun little scripts with the following goals:

 - Implement cellular automata in a terminal
 - Require nothing that isn't usually installed by default


## Keys

Key(s) | Action
------ | ----------
Up/Down arrow | Change delay (speed up or slow down)
q | quit
Any other key | Reinitialize the board (usually randomly)



## Scripts

### automata.py
Library that implements the automataBoard and automata classes.  The goal is to make it where all you have to do is define your cell states and create an iterate function that accepts the board in one state and returns the board in the next generation state.


---

### colortest.py
Just a script to spit out the terminal colors with numbers.  So you can choose colors in the configs of each script.

---

### ant.py

[Langton's ant](https://en.wikipedia.org/wiki/Langton's_ant)  

![ant.py](screenshots/ant.gif)

---

### belousov.py

[Belousov-Zhabotinsky Reaction](https://softologyblog.wordpress.com/2017/02/04/the-belousov-zhabotinsky-reaction-and-the-hodgepodge-machine/)  

![belousov.py](screenshots/belousov.gif)


---

### brain.py

[Brian's Brain](https://en.wikipedia.org/wiki/Brian's_Brain)  

![brain.py](screenshots/brain.gif)


---

### faders.py

[Faders](https://www.fourmilab.ch/cellab/manual/rules.html#Faders)  
Described as a cross between Life and Brain  

![faders.py](screenshots/faders.gif)


---

### forest.py

[A Mathematical Approach to Forest Growth Dynamics](http://web.math.unifi.it/users/primicer/2016%20forest%20growth)  

![forest.py](screenshots/forest.gif)


---

### larger-than-life.py

[Larger than Life](https://www.emis.de/journals/DMTCS/pdfpapers/dmAA0113.pdf)  
Similar to the game of life except configurable neighborhood size, birth range, and survival range.  

![larger-than-life.py](screenshots/larger-than-life.gif)

---

### life.py

[Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)  
The most famous cellular automata.  

![life.py](screenshots/life.gif)

---

### reforestation.py

forest.py with the addition of fire

![reforestation.py](screenshots/reforestation.gif)

---

### rug.py

[RUG](https://www.fourmilab.ch/cellab/manual/rules.html#Rug)  

![rug.py](screenshots/rug.gif)  

---

### wildfire.py

[Stochastic Wildland Fire Spread Dynamics](https://iopscience.iop.org/article/10.1088/1742-6596/285/1/012038/pdf)  

![wildfire.py](screenshots/wildfire.gif)  
