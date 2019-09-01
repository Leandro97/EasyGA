# Welcome to EasyGA!

**EasyGA** is a genetic algorithm definition tool for mathematical function optimization. Aimed at users of all skill levels, it facilitates the use of genetic algorithms by eliminating the need to write any line of code: all settings are made through the graphical interface.

# Using EasyGA
The tool is designed to run on Linux machines. It was written in Python and requires the [Kivy library](https://kivy.org/)  for the graphical interface to work.

## Installation
Before installing EasyGa, make sure that you have Python 3 on your machine. The following packages are also needed: 

- [pip](https://www.tecmint.com/install-pip-in-linux/) (python 3)
- [git](https://git-scm.com/download/linux)

Now follow the steps:

- Install virtualenv
	>$ pip install virtualenv
	
- Create a virtual environment
	>$ virtualenv EgaEnv
- Activate the virtualenv
	>$ source EgaEnv/bin/activate
	
- Install needed libraries
	>$ pip install kivy matplotlib six 
	
	>$ garden install matplotlib
	
- Clone the EasyGA repository
	> $ git clone https://github.com/Leandro97/EasyGA.git

## Running EasyGA
- Enter the cloned repository and run the script
	> $ python easyga.py
