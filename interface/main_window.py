import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from utils.logger import add_log, add_log_no_time, clear_log
from utils.file_operations import display_files, organize_files, find_duplicates, get_statistics


def create_window():
	root = ctk.CTk()
	root.title("File Organizer")
	root.geometry("1000x800")

	ctk.set_appearance_mode("dark")
	ctk.set_default_color_theme("blue")

	return root


def setup_ui(root):
	selected_folder = [None]

	title_frame = ctk.CTkFrame(root)
	title_frame.pack(fill='x', padx=20, pady=10)

	title = ctk.CTkLabel(title_frame, text="File Organizer", font=("Arial", 24))
	title.pack(pady=10)

	main_container = ctk.CTkFrame(root)
	main_container.pack(fill='both', expand=True, padx=20, pady=10)

	left_frame = ctk.CTkFrame(main_container)
	left_frame.pack(side='left', fill='both', expand=True, padx=10)

	right_frame = ctk.CTkFrame(main_container)
	right_frame.pack(side='right', fill='both', expand=True, padx=10)

	path_label = ctk.CTkLabel(left_frame, text="No folder selected", wraplength=400)
	path_label.pack(pady=10)

	files_text = ctk.CTkTextbox(left_frame, height=400)
	files_text.pack(fill='both', expand=True, pady=10)

	button_frame = ctk.CTkFrame(right_frame)
	button_frame.pack(pady=10)

	log_label = ctk.CTkLabel(right_frame, text="Activity Log:")
	log_label.pack(pady=5)

	log_text = ctk.CTkTextbox(right_frame, height=300, state="disabled")
	log_text.pack(fill='both', expand=True, pady=5)

	def select_folder_callback():
		folder = filedialog.askdirectory()
		if folder:
			selected_folder[0] = folder
			path_label.configure(text=f"Selected: {folder}")
			add_log(log_text, f"Selected folder: {folder}")
			display_files(folder, files_text)

	def organize_files_callback():
		if not selected_folder[0]:
			messagebox.showerror("Error", "Please select a folder first!")
			return

		try:
			files_moved = organize_files(selected_folder[0], log_text)
			messagebox.showinfo("Success", f"Organized {files_moved} files!")
			add_log(log_text, f"Successfully organized {files_moved} files")
			display_files(selected_folder[0], files_text)
		except Exception as e:
			messagebox.showerror("Error", f"An error occurred: {str(e)}")
			add_log(log_text, f"Error: {str(e)}")

	def find_duplicates_callback():
		if not selected_folder[0]:
			messagebox.showerror("Error", "Please select a folder first!")
			return

		try:
			duplicates = find_duplicates(selected_folder[0], log_text)

			if duplicates:
				add_log(log_text, "Found potential duplicates:")
				for orig, dup in duplicates:
					add_log_no_time(log_text, f"- Original: {os.path.basename(orig)}")
					add_log_no_time(log_text, f"- Duplicate: {os.path.basename(dup)}")
					add_log_no_time(log_text, "-" * 60)
			else:
				add_log(log_text, "No duplicates found!")
		except Exception as e:
			messagebox.showerror("Error", f"An error occurred: {str(e)}")
			add_log(log_text, f"Error: {str(e)}")

	def show_statistics_callback():
		if not selected_folder[0]:
			messagebox.showerror("Error", "Please select a folder first!")
			return

		try:
			stats, total_size = get_statistics(selected_folder[0])

			add_log(log_text, "Folder Statistics:")
			add_log_no_time(log_text, f"- Total size: {total_size / (1024 * 1024):.2f} MB")

			for category, count in stats.items():
				if count > 0:
					add_log_no_time(log_text, f"- {category}: {count} files")
		except Exception as e:
			messagebox.showerror("Error", f"An error occurred: {str(e)}")
			add_log(log_text, f"Error: {str(e)}")

	def clear_log_callback():
		clear_log(log_text)

	ctk.CTkButton(
		button_frame,
		text="Select Folder",
		command=select_folder_callback,
		width=200
	).pack(pady=5)

	ctk.CTkButton(
		button_frame,
		text="Organize Files",
		command=organize_files_callback,
		width=200
	).pack(pady=5)

	ctk.CTkButton(
		button_frame,
		text="Find Duplicates",
		command=find_duplicates_callback,
		width=200
	).pack(pady=5)

	ctk.CTkButton(
		button_frame,
		text="Show Statistics",
		command=show_statistics_callback,
		width=200
	).pack(pady=5)

	ctk.CTkButton(
		right_frame,
		text="Clear Log",
		command=clear_log_callback,
		width=200
	).pack(pady=5)

	return root