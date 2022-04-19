from re import L
import tkinter as tk
from tkinter import Frame, mainloop, ttk
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
from cellPresenceDetermination import Analyser
from PIL import Image, ImageTk
from configparser import ConfigParser
from utils import getInitDir
import csv
LARGEFONT = ("Verdana", 35)



class tkinterApp(tk.Tk):

	def Test(self):
		window = AnalysisWindow(self)
		#window.DisplayImage("Step_5_leukemic_cells_center_determination.PNG")



	def browseFilesTCell(self,reset): #return a list with all files locai
		if reset:
			self.listeTCell=[]
		folderVid = filedialog.askdirectory (initialdir = "/",title = "Select the directory which contains the images of T-cells")
		for root, dirs, files in os.walk(folderVid):
			for file in files:
				fichier = os.path.join(root,file)
				self.listeTCell.append(fichier)

	def browseFilesLeukemicCell(self,reset): #return a list with all files locai
		if reset:
			self.listeLeukemicCell=[]
		folderVid = filedialog.askdirectory (initialdir = "/",title = "Select the directory which contains the images of Leukemic cells")
		for root, dirs, files in os.walk(folderVid):
			for file in files:
				fichier = os.path.join(root,file)
				self.listeLeukemicCell.append(fichier)


	def BrowseBrightfield(self):
		self.folderBrightfield = filedialog.askopenfilename (initialdir = getInitDir(self.folderBrightfield), title = "Select the image with empty cells")
		self.Analyzer = None
	def BrowseLeukemicCell(self):
		#self.Analyzer.setRenderSuperPos(True) ### TODO : A déplacer sur un boutton
		#self.folderLeukemicCell = filedialog.askopenfilename (initialdir = getInitDir(self.folderLeukemicCell), title = "Select the last image of the leukemic Cells")
		self.browseFilesLeukemicCell(True)
	def BrowseTCell(self):
		#self.Analyzer.setRenderSteps(True) ### TODO : A déplacer sur un boutton
		#self.folderTCells = filedialog.askopenfilename (initialdir = getInitDir(self.folderTCells), title = "Select the last image of the Tcells")
		self.browseFilesTCell(True)

	def StartAnalysis(self):
		dif = len(self.listeTCell) - len(self.listeLeukemicCell)
		if dif > 0:
			self.listeTCell = self.listeTCell[dif:]
		elif dif < 0:
			self.listeLeukemicCell = self.listeLeukemicCell[abs(dif):]
		#try:
		if(self.Analyzer is None) : self.Analyzer = Analyser(self.folderBrightfield)
		if self.DisplayImage :
			self.topLevelListe = AnalysisWindow (self)
			self.topLevelListe.DisplayImage("Step_5_leukemic_cells_center_determination.PNG")

		for imgTcell,imgLcell in zip (self.listeTCell, self.listeLeukemicCell):
			interactionPositions, stat = self.Analyzer.getInteractionArray(imgLcell,imgTcell)
			self.stats["numberOfValidLeukemicCells"].append(stat["numberOfValidLeukemicCells"])
			self.stats["numberOfValidTCells"].append(stat["numberOfValidTCells"])
			self.stats["numberOfinteractions"].append(stat["numberOfinteractions"])
			self.stats["pourcentageOfValidLeukemicCells"].append(stat["pourcentageOfValidLeukemicCells"])
			self.stats["pourcentageOfValidTCells"].append(stat["pourcentageOfValidTCells"])
			self.stats["pourcentageOfInteractions"].append(stat["pourcentageOfInteractions"])
			
				#fenetreAnalyse.DisplayImage("Step_5_leukemic_cells_center_determination",1,1)
		if self.DisplayImage:
			self.topLevelListe.DisplayImage("Step_5_leukemic_cells_center_determination.PNG")


			
		print(self.stats)


		with open ("Statistics.csv" , "w") as excel:
			writer = csv.writer (excel, delimiter = ";")
			writer.writerow(self.stats.keys())
			writer.writerows(zip(*self.stats.values()))



		#except:
			#self.PopUp("Error","An error occured during the analysis")



	def ResetImgDir(self):
		self.folderBrightfield = ""
		self.folderLeukemicCell = ""
		self.folderTCells = ""
		self.PopUp("Reset","Images directories have been reset")

	def PopUp(self,titre,message):
		tk.messagebox.showinfo(titre,message)

	def changeTheme(self,text,**kwargs):
		self.theme = text
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
		print(type( self.folderBrightfield))
		config = ConfigParser(allow_no_value=True)
		config.add_section("Parameters")
		config.set("Parameters","folderBrightfield", self.folderBrightfield)
		config.set("Parameters","folderLeukemicCell", self.folderLeukemicCell)
		config.set("Parameters","folderTCells", self.folderTCells)
		config.set("Parameters","theme",self.theme)
		with open('config.ini', 'w') as conf:
			config.write(conf)
		self.destroy()

	def saveGraph(title):
		plt.savefig("Saved Files/" + title + '.png')

	def resetList(self):
		self.list_of_files=[]

	def PrintFilesDir(self):
		if len(self.list_of_files)>0:
			print(self.list_of_files)
		else:
			print("Error no valid files were found")

	def SetDisplayImage(self):
		if self.DisplayImage:
			self.DisplayImage=False
		else:
			self.DisplayImage = True

	def __init__(self, *args, **kwargs):		
		# __init__ function for class Tk
		tk.Tk.__init__(self, *args, **kwargs)
		self.listeLeukemicCell = []
		self.listeTCell = []
		self.Analyzer = None
		self.topLevelListe = []
		self.frames = {}
		self.wm_iconbitmap('Image/logo.ico')
		#self.title=("Analyse vidéo")
		self.geometry("1000x600")
		self.DisplayImage = False
		try: #Loading parameters
			self.config = ConfigParser()
			self.config.read("config.ini")
			self.folderBrightfield = self.config["Parameters"]["folderBrightfield"]
			self.folderLeukemicCell = self.config["Parameters"]["folderLeukemicCell"]
			self.folderTCells = self.config["Parameters"]["folderTCells"]
			self.theme = self.config["Parameters"]["Theme"]
		except: #if the loading fails, default parameters are used
			self.folderBrightfield = ""
			self.folderLeukemicCell = ""
			self.folderTCells = ""
			self.theme = "radiance"


		self.listeOfThemes = self.listeOfThemes = os.listdir('Themes')
		self.styleApp = ttk.Style()
		for i in self.listeOfThemes:
			self.tk.call("source", "Themes/"+i+"/"+i+".tcl")

		self.styleApp.theme_use(self.theme)
		self.dic = {}
		self.interactionPositions = []
		self.stats = {
			"numberOfValidLeukemicCells" : [],
			"numberOfValidTCells" : [],
			"numberOfinteractions": [],
			"pourcentageOfValidLeukemicCells": [],
			"pourcentageOfValidTCells": [],
			"pourcentageOfInteractions": []
		
		}

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
		frame.grid(row = 0, column = 0, sticky ="WN")

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

		#buttonDirAdd = ttk.Button(self,text = "Add Directory", command = partial(controller.browseFiles,False))
		#buttonDirAdd.grid(row=2,column=4 ,padx=10, pady=10,sticky='w')
		buttonTest = ttk.Button(self, text = "Test",command=partial(controller.Test))
		buttonTest.grid(row = 4, column = 2, padx = 10, pady = 10,sticky='w')



		buttonDisplayImages = ttk.Checkbutton(self, text = "Display Images live (lower performances)",command=partial(controller.SetDisplayImage))
		buttonDisplayImages.grid(row = 3, column = 2, padx = 10, pady = 10,sticky='w')

		buttonReset =  ttk.Button(self, text ="Reset", command = partial(controller.ResetImgDir))
		buttonReset.grid(row = 2, column = 2, padx = 10, pady = 10,sticky='w')


		buttonStatistics = ttk.Button(self, text ="Statistics", command = partial(controller.show_frame,Statistics))
		buttonStatistics.grid(row = 2, column = 1, padx = 10, pady = 10,sticky='w')

		buttonMenu = ttk.Button(self,text="Menu", state='disabled')
		buttonMenu.grid(row = 1, column = 1, padx = 10, pady = 10,sticky='w')

		## button to show frame 2 with text layout2
		buttonParameters = ttk.Button(self, text ="Parameters", command = partial(controller.show_frame,Parameters))
		buttonParameters.grid(row = 3, column = 1, padx = 10, pady = 10,sticky='w')

		buttonStartProg = ttk.Button(self,text="Start analysis", command = partial(controller.StartAnalysis))
		buttonStartProg.grid(row=1,column=2,padx=10,pady=10,sticky='w')


		buttonBrightfield = ttk.Button(self,text="Choose the folder with empty cells",command=partial(controller.BrowseBrightfield))
		buttonBrightfield.grid(row=1,column=3,padx=10,pady=10,sticky='w')

		buttonLeukemicCells = ttk.Button(self,text="Choose the LAST image with leukemic cells", command=partial(controller.BrowseLeukemicCell))
		buttonLeukemicCells.grid(row=2,column=3,padx=10,pady=10,sticky='w')

		buttonTcells = ttk.Button(self,text="Choose the LAST image with T-cells",command = partial(controller.BrowseTCell))
		buttonTcells.grid(row=3,column=3,padx=10,pady=10,sticky='w')

		#buttonSaveResult = ttk.Button(self,text="Save analysis")
		#buttonSaveResult.grid(row = 4, column = 5 , padx = 10 , pady = 10 ,sticky='w')

		buttonQuit = ttk.Button(self,text="Quit" , style = 'BW.TButton' ,command=controller.Close)
		buttonQuit.grid(row=4,column = 1, padx = 10 ,pady = 10 ,sticky='w')


# second window frame Statistics
class Statistics(tk.Frame):
	def DisplayImage(self,nameImg,row,column):
		photo = ImageTk.PhotoImage(Image.open("Processed/"+ nameImg).resize((150,150)))
		labelTmp = ttk.Label(self,image = photo)
		labelTmp.Image = photo
		labelTmp.grid(row=row, column = column,padx = 10, pady = 10)



	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		#label = ttk.Label(self, text ="Statistics", font = LARGEFONT)
		#label.grid(row = 0, column = 4, padx = 10, pady = 10,sticky='w')

		#buttonPlot= ttk.Button(self, text="Plot graph",command = partial(controller.pltGraphOutside,np.arange(1,4),np.arange(1,4),"VarTheme"))
		#buttonPlot.grid(row = 1, column = 4, padx =10, pady = 10,sticky='w')

		#buttonVarTheme=ttk.Button(self, text="Print files directory", command = controller.PrintFilesDir)
		#buttonVarTheme.grid(row=2, column = 4, padx = 10, pady = 10,sticky='w')


		buttonMenu = ttk.Button(self, text ="Menu",command = partial(controller.show_frame,Menu))
		buttonMenu.grid(row = 1, column = 1, padx = 10, pady = 10,sticky='w')

		buttonStatistics = ttk.Button(self,text = "Statistics",state='disabled')
		buttonStatistics.grid(row = 2, column = 1, padx = 10, pady = 10,sticky='w')

		buttonParameters = ttk.Button(self, text ="Parameters",command = partial(controller.show_frame,Parameters))
		buttonParameters.grid(row = 3, column = 1, padx = 10, pady = 10,sticky='w')

		buttonQuit = ttk.Button(self,text="Quit" , style = 'BW.TButton' ,command=controller.Close)
		buttonQuit.grid(row=4,column = 1, padx = 10 ,pady = 10 ,sticky='w')

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

		#SaveFileFolderSave = tk.Text(self, height=1,width=25)
		#SaveFileFolderSave.insert(tk.INSERT, controller.parameters["saveFolder"])
		#SaveFileFolderSave.grid(row = 2, column = 4, padx = 10, pady = 10,sticky='w')

		#buttonSaveFolder = ttk.Button(self,text='Change Folder for saved files',command = partial(controller.changeSaveFolder,SaveFileFolderSave))
		#buttonSaveFolder.grid(row = 1, column = 4, padx = 10, pady = 10,sticky='w')

		buttonQuit = ttk.Button(self,text="Quit" , style = 'BW.TButton' ,command=controller.Close)
		buttonQuit.grid(row=4,column = 1, padx = 10 ,pady = 10 ,sticky='w')

		label = ttk.Label(self, text ="Change Theme")
		label.grid(row = 3, column = 4, padx = 10, pady = 10,sticky='w')

		self.VarTheme = tk.StringVar(self)
		self.VarTheme.set(controller.listeOfThemes[0])
		buttonTheme = ttk.OptionMenu(self,self.VarTheme,*controller.listeOfThemes, command = controller.changeTheme)
		buttonTheme.grid(row=4,column = 4, padx = 10 ,pady = 10 ,sticky='w')


	

class AnalysisWindow(tk.Toplevel):
	def __init__(self, parent):
		tk.Toplevel.__init__(self, parent)
		self.canvasImg = tk.Canvas(self, width=600, height= 600)
		photo = ImageTk.PhotoImage(Image.open("Processed/"+ "Step_5_leukemic_cells_center_determination.PNG").resize((600,600)))
		self.canvasImg.create_image(50,10,image=photo)
		self.canvasImg.pack()




	def DisplayImage(self,nameImg):
		photo = ImageTk.PhotoImage(Image.open("Processed/"+ nameImg).resize((600,600)))
		self.canvasImg.create_image(image=photo)
        







if __name__ == "__main__":
	app = tkinterApp()
	app.mainloop()
