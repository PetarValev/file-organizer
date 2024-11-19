import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import shutil
from datetime import datetime


class FileOrganizer:
	def __init__(self):
		ctk.set_appearance_mode("dark")
		ctk.set_default_color_theme("blue")

		self.root = ctk.CTk()
		self.root.title("File Organizer")
		self.root.geometry("1000x800")

		self.selected_folder = None
		self.file_types = {
			'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
			'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.csv'],
			'Videos': ['.mp4', '.avi', '.mkv', '.mov'],
			'Audio': ['.mp3', '.wav', '.flac'],
			'Archives': ['.zip', '.rar', '.7z'],
			'Code': ['.py', '.js', '.html', '.css', '.java']
		}

		self.create_widgets()

	def create_widgets(self):
		title_frame = ctk.CTkFrame(self.root)
		title_frame.pack(fill='x', padx=20, pady=10)

		title = ctk.CTkLabel(
			title_frame,
			text="File Organizer",
			font=("Arial", 24)
		)
		title.pack(pady=10)

		main_container = ctk.CTkFrame(self.root)
		main_container.pack(fill='both', expand=True, padx=20, pady=10)

		left_frame = ctk.CTkFrame(main_container)
		left_frame.pack(side='left', fill='both', expand=True, padx=10)

		right_frame = ctk.CTkFrame(main_container)
		right_frame.pack(side='right', fill='both', expand=True, padx=10)

		self.path_label = ctk.CTkLabel(
			left_frame,
			text="No folder selected",
			wraplength=400
		)
		self.path_label.pack(pady=10)

		self.files_text = ctk.CTkTextbox(left_frame, height=400)
		self.files_text.pack(fill='both', expand=True, pady=10)

		button_frame = ctk.CTkFrame(right_frame)
		button_frame.pack(pady=10)

		ctk.CTkButton(
			button_frame,
			text="Select Folder",
			command=self.select_folder,
			width=200
		).pack(pady=5)

		ctk.CTkButton(
			button_frame,
			text="Organize Files",
			command=self.organize_files,
			width=200
		).pack(pady=5)

		ctk.CTkButton(
			button_frame,
			text="Find Duplicates",
			command=self.find_duplicates,
			width=200
		).pack(pady=5)

		ctk.CTkButton(
			button_frame,
			text="Show Statistics",
			command=self.show_statistics,
			width=200
		).pack(pady=5)

		log_label = ctk.CTkLabel(right_frame, text="Activity Log:")
		log_label.pack(pady=5)

		self.log_text = ctk.CTkTextbox(right_frame, height=300, state="disabled")
		self.log_text.pack(fill='both', expand=True, pady=5)

		ctk.CTkButton(
			right_frame,
			text="Clear Log",
			command=self.clear_log,
			width=200
		).pack(pady=5)

	def clear_log(self):
		self.log_text.configure(state="normal")
		self.log_text.delete('1.0', 'end')
		self.log_text.configure(state="disabled")

	def add_log(self, message):
		timestamp = datetime.now().strftime("%H:%M:%S")
		self.log_text.configure(state="normal")
		self.log_text.insert("end", f"[{timestamp}] {message}\n")
		self.log_text.see("end")
		self.log_text.configure(state="disabled")

	def display_files(self):
		if not self.selected_folder:
			return

		self.files_text.delete('1.0', 'end')

		try:
			self.files_text.insert('end', "📁 FOLDERS:\n")
			for item in os.listdir(self.selected_folder):
				full_path = os.path.join(self.selected_folder, item)
				if os.path.isdir(full_path):
					self.files_text.insert('end', f"    📁 {item}\n")

			self.files_text.insert('end', "\n📄 FILES:\n")
			for item in os.listdir(self.selected_folder):
				full_path = os.path.join(self.selected_folder, item)
				if os.path.isfile(full_path):
					size = os.path.getsize(full_path)
					if size < 1024:
						size_str = f"{size} B"
					elif size < 1024 * 1024:
						size_str = f"{size / 1024:.1f} KB"
					else:
						size_str = f"{size / (1024 * 1024):.1f} MB"
					self.files_text.insert('end', f"    📄 {item} ({size_str})\n")

		except Exception as e:
			self.files_text.insert('end', f"Error reading files: {str(e)}")

	def select_folder(self):
		folder = filedialog.askdirectory()
		if folder:
			self.selected_folder = folder
			self.path_label.configure(text=f"Selected: {folder}")
			self.add_log(f"Selected folder: {folder}")
			self.display_files()

	def organize_files(self):
		if not self.selected_folder:
			messagebox.showerror("Error", "Please select a folder first!")
			return

		try:
			files_moved = 0
			self.add_log("Starting file organization process...")
			for filename in os.listdir(self.selected_folder):
				file_path = os.path.join(self.selected_folder, filename)
				if os.path.isfile(file_path):
					file_ext = os.path.splitext(filename)[1].lower()

					category = 'Other'
					for cat, extensions in self.file_types.items():
						if file_ext in extensions:
							category = cat
							break

					category_path = os.path.join(self.selected_folder, category)
					if not os.path.exists(category_path):
						os.makedirs(category_path)

					shutil.move(file_path, os.path.join(category_path, filename))
					files_moved += 1
					self.add_log_no_time(f"- Moved {filename} to {category}")

			messagebox.showinfo("Success", f"Organized {files_moved} files!")
			self.add_log(f"Successfully organized {files_moved} files")
			self.display_files()

		except Exception as e:
			messagebox.showerror("Error", f"An error occurred: {str(e)}")
			self.add_log(f"Error: {str(e)}")

	def add_log_no_time(self, message):
		self.log_text.configure(state="normal")
		self.log_text.insert("end", f"{message}\n")
		self.log_text.see("end")
		self.log_text.configure(state="disabled")

	def find_duplicates(self):
		if not self.selected_folder:
			messagebox.showerror("Error", "Please select a folder first!")
			return

		try:
			size_dict = {}
			duplicates = []

			for dirpath, _, filenames in os.walk(self.selected_folder):
				for filename in filenames:
					file_path = os.path.join(dirpath, filename)
					file_size = os.path.getsize(file_path)

					if file_size in size_dict:
						duplicates.append((size_dict[file_size], file_path))
					else:
						size_dict[file_size] = file_path

			if duplicates:
				self.add_log("Found potential duplicates:")
				for orig, dup in duplicates:
					self.add_log_no_time(f"- Original: {os.path.basename(orig)}")
					self.add_log_no_time(f"- Duplicate: {os.path.basename(dup)}")
					self.add_log_no_time("-" * 60)
			else:
				self.add_log("No duplicates found!")

		except Exception as e:
			messagebox.showerror("Error", f"An error occurred: {str(e)}")
			self.add_log(f"Error: {str(e)}")

	def show_statistics(self):
		if not self.selected_folder:
			messagebox.showerror("Error", "Please select a folder first!")
			return

		try:
			stats = {cat: 0 for cat in self.file_types.keys()}
			stats['Other'] = 0
			total_size = 0

			for dirpath, _, filenames in os.walk(self.selected_folder):
				for filename in filenames:
					file_path = os.path.join(dirpath, filename)
					file_ext = os.path.splitext(filename)[1].lower()

					category = 'Other'
					for cat, extensions in self.file_types.items():
						if file_ext in extensions:
							category = cat
							break
					stats[category] += 1

					total_size += os.path.getsize(file_path)

			self.add_log("Folder Statistics:")

			self.add_log_no_time(f"- Total size: {total_size / (1024 * 1024):.2f} MB")
			for category, count in stats.items():
				if count > 0:
					self.add_log_no_time(f"- {category}: {count} files")

		except Exception as e:
			messagebox.showerror("Error", f"An error occurred: {str(e)}")
			self.add_log(f"Error: {str(e)}")

	def run(self):
		self.root.mainloop()


if __name__ == "__main__":
	app = FileOrganizer()
	app.run()