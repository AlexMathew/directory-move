import Tkinter as tk
import os

class Application(tk.Frame):
	""" The Application class manages the GUI. 
	The create_widgets() method creates the widgets to be inserted in the frame.
	A button triggers an event that calls the perform_move() method.
	This function calls the recursive method move_directories(). """

	def __init__(self, master):
		tk.Frame.__init__(self, master)
		self.grid()
		self.create_widgets()

	def create_widgets(self):
		self.intro = tk.Label(self, text = "Do you want to move all files in one folder to another folder ?")
		self.intro.grid(row = 0, column = 0, columnspan = 3, sticky = tk.W)

		self.src_label = tk.Label(self, text = "Enter the complete path of the source (with single backslash b/w directories) ")
		self.src_label.grid(row = 2, column = 0, columnspan = 3, sticky = tk.W)

		self.src_entry = tk.Entry(self, width = 50)
		self.src_entry.grid(row = 3, column = 1, sticky = tk.W)

		self.dest_label = tk.Label(self, text = "Enter the complete path of the (already existing, but empty) destination (with single backslash b/w directories) ")
		self.dest_label.grid(row = 5, column = 0, columnspan = 3, sticky = tk.W)

		self.dest_entry = tk.Entry(self, width = 50)
		self.dest_entry.grid(row = 6, column = 1, sticky = tk.W)

		self.move_button = tk.Button(self, text = "MOVE IT !", command = self.perform_move)
		self.move_button.grid(row = 8, column = 1, sticky = tk.W)

		self.text = tk.Text(self, width = 50, height = 10, wrap = tk.WORD)
		self.text.grid(row = 12, column = 0, columnspan = 2, sticky = tk.W)

	def perform_move(self):
		msg = ""

		try:
			src = self.src_entry.get()
			dest = self.dest_entry.get()

			walker = os.walk(src)
			root, dirs, files = next(walker)
			
			for filename in files:
				old = os.path.join(root, filename)
				new = os.path.join(dest, filename)
				os.rename(old, new)

			for directory in dirs:
				self.move_directories(src, directory, dest)

			msg = "Done !!"

		except WindowsError:
			msg = "Give an existing empty directory for the destination."

		except StopIteration:
			msg = "Give a valid directory for the source."

		finally:
			self.text.delete(0.0, tk.END)
			self.text.insert(0.0, msg)

	def move_directories(self, src, directory, dest):
		src = os.path.join(src, directory)
		dest = os.path.join(dest, directory)
		os.mkdir(dest)
		
		walker = os.walk(src)
		root, dirs, files = next(walker)
		
		for filename in files:
			old = os.path.join(src, filename)
			new = os.path.join(dest, filename)
			os.rename(old, new)
		
		for directory in dirs:
			self.move_directories(src, directory, dest)

		os.rmdir(src)


# To create the frame and create the Application class object

def main():
	root = tk.Tk()
	root.title("Packers & Movers")
	root.geometry("700x500")

	app = Application(root)

	root.mainloop()

if __name__ == '__main__':
	main()