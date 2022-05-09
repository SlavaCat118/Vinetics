import processing
import fileManager as file

import tkinter            as tk
import tkinter.ttk        as ttk
import tkinter.filedialog as fileDialog

def main():

	PADDING = 5
	MINOFFSPRING = 1
	MAXOFFSPRING = 10

	r = tk.Tk()
	r.title("Vinetics")
	r.iconbitmap("VineticsIcon.ico")
	r.title("Vinetics")
	r.resizable(width=False, height=False)
	root = ttk.Frame(r)
	root.grid(padx = PADDING, pady = PADDING)

	offspringVar = tk.IntVar()
	crossProbVar = tk.DoubleVar()
	outputPath = tk.StringVar()


	expressionVar = tk.DoubleVar()
	baseParentPath = tk.StringVar()

	offspringVar.set(5)
	crossProbVar.set(80)
	outputPath.set("OUTPUT\\")

	def roundVar(var, n = 0):
		var.set(round(var.get(), n))

	def addParent(*args):
		files = fileDialog.askopenfiles(filetypes = [(".vital", ".vital")])
		for i in files:
			writeConsole("Added parent " + i.name)
			parentTree.insert(parent = "", index = 'end', text = file.baseName(i.name), values = (50.0, i.name))

	def removeParent(*args):
		for i in parentTree.selection():
			writeConsole("Removed parent " + parentTree.item(i)["text"])
			parentTree.delete(i)

	def setExpressionFrame(*args):
		expressionVar.set(parentTree.item(parentTree.focus())['values'][0])

	def setExpression(*args):
		for i in parentTree.selection():
			writeConsole("Expression " + parentTree.item(i)["text"] + " set to " + str(expressionVar.get()))
			parentTree.item(i, values = (expressionVar.get(), parentTree.item(i)['values'][1]))

	def generatePresets(*args):
		parentsSettings = []
		for i in parentTree.get_children():
			parentsSettings.append(list(parentTree.item(i)['values']))
		if sum([float(i[0]) for i in parentsSettings]) != 0:
			if file.exists(outputPath.get().strip()):
				if baseParentPath.get().strip() == "":
					baseParentPath.set("init.vital")
					writeConsole("No parent path set, set to " + baseParentPath.get())
				writeConsole("Generating...")
				writeConsole(processing.breed(baseParentPath.get().strip(), parentsSettings, offspringVar.get(), outputPath.get().strip(), crossProbVar.get()))
			else:
				writeConsole("Non valid output path")
		else:
			writeConsole("All expression can't be 0.0")

	def setBaseParent(*args):
		path = fileDialog.askopenfile(filetypes = [(".vital", ".vital")])
		if path != None:
			writeConsole("Base parent set to " + path.name)
			baseParentPath.set(path.name)
			baseParentButton.configure(text = file.baseName(baseParentPath.get()))

	def setOutputPath(*args):
		path = fileDialog.askdirectory(initialdir = outputPath.get())
		if path != "":
			writeConsole("Output path set to " + path)
			outputPath.set(path)

	def writeConsole(text):
		console.insert(tk.END, "\n> " + text)
		console.see(tk.END)


																				### PARENTS FRAME
	parentsFrame = ttk.LabelFrame(root, text = "Parents")

	parentTree = ttk.Treeview(parentsFrame, column = ("#1"))
	parentTree.heading("#0", text = "Parents", anchor = tk.W)
	parentTree.heading("#1", text = "Expression", anchor = tk.W)
	parentTree.column("#0", width = 100, anchor = tk.W)
	parentTree.column("#1", width = 75, anchor = tk.W)

	addParentButton = ttk.Button(parentsFrame, text = "Add", command = addParent)
	remParentButton = ttk.Button(parentsFrame, text = "Remove", command = removeParent)
	baseParentButton = ttk.Button(parentsFrame, text = "Base Parent: Browse", command = setBaseParent)

	parentTree.grid(row = 1, column = 0, columnspan = 2, sticky = tk.NSEW)
	baseParentButton.grid(row = 0, column = 0, sticky = tk.NSEW, columnspan = 2)
	addParentButton.grid(row = 2, column = 0, sticky = tk.NSEW)
	remParentButton.grid(row = 2, column = 1, sticky = tk.NSEW)
	parentsFrame.grid(row = 0, column = 0, sticky = tk.NSEW)

	parentTree.bind("<Double-1>", setExpressionFrame)

	expressionFrame = ttk.LabelFrame(parentsFrame, text = "Expression: ")
	expressionScale = ttk.Scale(expressionFrame, from_ = 0, to = 100, var = expressionVar, command = lambda x: roundVar(expressionVar, 2))
	expressionEntry = ttk.Entry(expressionFrame, textvariable = expressionVar, width = 5)
	expressionButton = ttk.Button(expressionFrame, text = " SET ", width = 0, command = setExpression)

	ttk.Label(expressionFrame, text = "%") .grid(row = 0, column = 2, sticky = tk.NSEW)

	expressionFrame.grid(row = 3, column = 0, columnspan = 2, sticky = tk.NSEW)
	expressionScale.grid(row = 0, column = 0, sticky = tk.NSEW)
	expressionEntry.grid(row = 0, column = 1, sticky = tk.NSEW)
	expressionButton.grid(row = 0, column = 3, sticky = tk.NSEW)

																				### BUILD FRAME
	buildFrame = ttk.LabelFrame(root, text = "Build: ")

	genButton = ttk.Button(buildFrame, text = "Generate", command = generatePresets)
	pathEntry = ttk.Entry(buildFrame, width = 20, textvariable = outputPath)
	browseButton = ttk.Button(buildFrame, text = "Browse", width = 0, command = setOutputPath)

	offspringScale = ttk.Scale(buildFrame, from_ = 1, to = 10, var = offspringVar, command = lambda x: roundVar(offspringVar))
	offspringEntry = ttk.Entry(buildFrame, textvariable = offspringVar, width = 5)

	genButton.grid(row = 0, column = 0, sticky = tk.NSEW, columnspan = 3)
	pathEntry.grid(row = 1, column = 0)
	browseButton.grid(row = 1, column = 1, columnspan = 2)

	ttk.Label(buildFrame, text = "Offspring:") .grid(row = 2, column = 0, sticky = tk.W)
	ttk.Label(buildFrame, text = "Cross Probability:") .grid(row = 4, column = 0, sticky = tk.W)

	offspringScale.grid(row = 3, column = 0, columnspan = 2, sticky = tk.NSEW)
	offspringEntry.grid(row = 3, column = 2)

	crossProbScale = ttk.Scale(buildFrame, from_ = 0, to = 100, var = crossProbVar, command = lambda x: roundVar(crossProbVar, 2))
	crossProbEntry = ttk.Entry(buildFrame, textvariable = crossProbVar, width = 5)

	crossProbScale.grid(row = 5, column = 0, columnspan = 2, sticky = tk.NSEW)
	crossProbEntry.grid(row = 5, column = 2)

	console = tk.Text(buildFrame, width = 10, height = 11, wrap = "word", font = ("consolas", 10), bg = "black", fg = "white")
	console.grid(row = 6, column = 0, sticky =  tk.NSEW, columnspan = 3)

	buildFrame.grid(row = 0, column = 1, sticky = tk.NSEW)

	r.mainloop()