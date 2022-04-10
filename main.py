import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
import numpy as np
from functools import partial


LARGEFONT =("Verdana", 35)

class tkinterApp(tk.Tk):
	def browseFiles(self,reset): #return a list with all files locai
		if reset:
			self.list_of_files=[]
		self.folderVid = filedialog.askdirectory (initialdir = "/",title = "Selectionner un dossier")
		for root, dirs, files in os.walk(self.folderVid):
			for file in files:
				fichier = os.path.join(root,file)
				if fichier[-3:]=="png":
					#self.list_of_files.append(os.path.join(root,file))
					self.list_of_files.append(file)
	

	def changeTheme(self,text,**kwargs):
		print(len(text))
		self.styleApp.theme_use(text)


	def changeSaveFolder(self,text):
		self.saveFolder = filedialog.askdirectory (initialdir = "/",title = "Selectionner un dossier")
		text.insert(tk.INSERT, self.saveFolder)

	def plotGraphInside(self,x,y,title,win):
		plt.clf()
		figure = Figure(figsize=(3, 3), dpi=100)
		plot = figure.add_subplot(1, 1, 1)
		plot.plot(x, y)
		plt.title(title)
		canvas = FigureCanvasTkAgg(figure, win)
		canvas.get_tk_widget().grid(row=3, column=3)

	def pltGraphOutside(self,x,y,title):
		plt.plot(x,y)
		plt.title(title)
		plt.show()

	def Close(self):
		self.destroy()

	def saveGraph(title):
		plt.savefig("Saved Files/" + title + '.png')

	def resetList(self):
		self.list_of_files=[]


	def Display_Image():
		#VarTheme
		print("Rien pour l'instant")

	def PrintFilesDir(self):
		if len(self.list_of_files)>0:
			print(self.list_of_files)
		else:
			print("Error no valid files were found")


	def __init__(self, *args, **kwargs):		
		# __init__ function for class Tk
		tk.Tk.__init__(self, *args, *args)
		
		self.folderVid =''
		self.list_of_files = []
		self.frames = {}
		self.wm_iconbitmap('Image/logo.ico')
		self.title=("Analyse vidéo")
		self.geometry("1000x600")

		self.parameters = { #different parameters
			"saveFolder" : os.getcwd() + "Result\\"
		}


		self.listeOfThemes = self.listeOfThemes = my_list = os.listdir('Themes')
		self.styleApp = ttk.Style()
		for i in self.listeOfThemes:
			self.tk.call("source", "Themes/"+i+"/"+i+".tcl")

		self.styleApp.theme_use("radiance")







		# creating a container
		container = tk.Frame(self)
		container.pack(side = "top", fill = "both", expand = True)

		container.grid_rowconfigure(0, weight = 1)
		container.grid_columnconfigure(0, weight = 1)

		# iterating through a tuple consisting
		# of the different page layouts
		for F in (Menu, Statistics, Parameters):
			frame = F(container, self)
			# initializing frame of that object from
			# Menu, Statistics, Parameters respectively with
			# for loop
			self.frames[F] = frame

			

		self.show_frame(Menu)

	# to display the current frame passed as
	# parameter
	def show_frame(self, cont):
		for F in self.frames.values():
			F.grid_forget()
		frame = self.frames[cont]
		frame.grid(row = 0, column = 0, sticky ="")

# first window frame Menu

class Menu(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
		# label of frame Layout 2
		#label = ttk.Label(self, text ="Menu", font = LARGEFONT)
		#label.grid(row = 0, column = 4, padx = 10, pady = 10,sticky='w')


		#styleButton= ttk.Style(self)
		#styleButton.configure('BW.TButton', font =('calibri', 10),foreground = 'white',background='#107D31')
		

		# putting the button in its place by
		# using grid
		buttonDir = ttk.Button(self,text = "New Directory",command = partial(controller.browseFiles, True))
		buttonDir.grid(row=1,column=5 ,padx=10, pady=10,sticky='w')

		#buttonDirAdd = ttk.Button(self,text = "Add Directory", command = partial(controller.browseFiles,False))
		#buttonDirAdd.grid(row=2,column=4 ,padx=10, pady=10,sticky='w')


		buttonReset =  ttk.Button(self, text ="Reset", command = partial(controller.resetList))
		buttonReset.grid(row = 3, column = 5, padx = 10, pady = 10,sticky='w')


		buttonStatistics = ttk.Button(self, text ="Statistics", command = partial(controller.show_frame,Statistics))
		buttonStatistics.grid(row = 2, column = 1, padx = 10, pady = 10,sticky='w')

		buttonMenu = ttk.Button(self,text="Menu", state='disabled')
		buttonMenu.grid(row = 1, column = 1, padx = 10, pady = 10,sticky='w')

		## button to show frame 2 with text layout2
		buttonParameters = ttk.Button(self, text ="Parameters", command = partial(controller.show_frame,Parameters))
		buttonParameters.grid(row = 3, column = 1, padx = 10, pady = 10,sticky='w')

		buttonStartProg = ttk.Button(self,text="Start analysis")
		buttonStartProg.grid(row=2,column=5,padx=10,pady=10,sticky='w')

		buttonSaveResult = ttk.Button(self,text="Save analysis")
		buttonSaveResult.grid(row = 6, column = 5 , padx = 10 , pady = 10 ,sticky='w')

		buttonQuit = ttk.Button(self,text="Quit" , style = 'BW.TButton' ,command=controller.Close)
		buttonQuit.grid(row=7,column = 5, padx = 10 ,pady = 10 ,sticky='w')


# second window frame Statistics
class Statistics(tk.Frame):
	
	def __init__(self, parent, controller):


		tk.Frame.__init__(self, parent)
		#label = ttk.Label(self, text ="Statistics", font = LARGEFONT)
		#label.grid(row = 0, column = 4, padx = 10, pady = 10,sticky='w')

		buttonPlot= ttk.Button(self, text="Plot graph",command = partial(controller.pltGraphOutside,np.arange(1,4),np.arange(1,4),"VarTheme"))
		buttonPlot.grid(row = 1, column = 4, padx =10, pady = 10,sticky='w')

		buttonVarTheme=ttk.Button(self, text="Print files directory", command = controller.PrintFilesDir)
		buttonVarTheme.grid(row=2, column = 4, padx = 10, pady = 10,sticky='w')


		buttonMenu = ttk.Button(self, text ="Menu",command = partial(controller.show_frame,Menu))
		buttonMenu.grid(row = 1, column = 1, padx = 10, pady = 10,sticky='w')

		buttonStatistics = ttk.Button(self,text = "Statistics",state='disabled')
		buttonStatistics.grid(row = 2, column = 1, padx = 10, pady = 10,sticky='w')

		buttonParameters = ttk.Button(self, text ="Parameters",command = partial(controller.show_frame,Parameters))
		buttonParameters.grid(row = 3, column = 1, padx = 10, pady = 10,sticky='w')

		buttonQuit = ttk.Button(self,text="Quit" , style = 'BW.TButton' ,command=controller.Close)
		buttonQuit.grid(row=3,column = 4, padx = 10 ,pady = 10 ,sticky='w')





# third window frame Parameters
class Parameters(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		#label = ttk.Label(self, text ="Parameters", font = LARGEFONT)
		#label.grid(row = 0, column = 4, padx = 10, pady = 10,sticky='w')



		buttonParameters = ttk.Button(self, text ="Parameters",state='disabled')
		buttonParameters.grid(row = 3, column = 1, padx = 10, pady = 10,sticky='w')


		buttonStatistics = ttk.Button(self, text ="Statistics", command = partial(controller.show_frame,Statistics))
		buttonStatistics.grid(row = 2, column = 1, padx = 10, pady = 10,sticky='w')


		buttonMenu = ttk.Button(self, text ="Menu", command = partial(controller.show_frame,Menu))
		buttonMenu.grid(row = 1, column = 1, padx = 10, pady = 10,sticky='w')

		SaveFileFolderSave = tk.Text(self, height=1,width=25)
		SaveFileFolderSave.insert(tk.INSERT, controller.parameters["saveFolder"])
		SaveFileFolderSave.grid(row = 2, column = 4, padx = 10, pady = 10,sticky='w')

		buttonSaveFolder = ttk.Button(self,text='Change Folder for saved files',command = partial(controller.changeSaveFolder,SaveFileFolderSave))
		buttonSaveFolder.grid(row = 1, column = 4, padx = 10, pady = 10,sticky='w')

		
		buttonQuit = ttk.Button(self,text="Quit" , style = 'BW.TButton' ,command=controller.Close)
		buttonQuit.grid(row=7,column = 4, padx = 10 ,pady = 10 ,sticky='w')


		label = ttk.Label(self, text ="Change Theme")
		label.grid(row = 5, column = 4, padx = 10, pady = 10,sticky='w')

		self.VarTheme = tk.StringVar(self)
		self.VarTheme.set(controller.listeOfThemes[0])
		buttonTheme = ttk.OptionMenu(self,self.VarTheme,*controller.listeOfThemes, command = controller.changeTheme)
		buttonTheme.grid(row=6,column = 4, padx = 10 ,pady = 10 ,sticky='w')
# Driver Code

app = tkinterApp()
app.mainloop()
