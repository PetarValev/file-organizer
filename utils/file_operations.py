import os
import shutil
from constants.file_types import FILE_TYPES
from utils.logger import add_log, add_log_no_time


def display_files(folder_path, files_text):
	files_text.delete('1.0', 'end')

	try:
		files_text.insert('end', "📁 FOLDERS:\n")
		for item in os.listdir(folder_path):
			full_path = os.path.join(folder_path, item)
			if os.path.isdir(full_path):
				files_text.insert('end', f"    📁 {item}\n")

		files_text.insert('end', "\n📄 FILES:\n")
		for item in os.listdir(folder_path):
			full_path = os.path.join(folder_path, item)
			if os.path.isfile(full_path):
				size = os.path.getsize(full_path)
				if size < 1024:
					size_str = f"{size} B"
				elif size < 1024 * 1024:
					size_str = f"{size / 1024:.1f} KB"
				else:
					size_str = f"{size / (1024 * 1024):.1f} MB"
				files_text.insert('end', f"    📄 {item} ({size_str})\n")

	except Exception as e:
		files_text.insert('end', f"Error reading files: {str(e)}")


def organize_files(folder_path, log_text):
	files_moved = 0
	add_log(log_text, "Starting file organization process...")

	for filename in os.listdir(folder_path):
		file_path = os.path.join(folder_path, filename)
		if os.path.isfile(file_path):
			file_ext = os.path.splitext(filename)[1].lower()

			category = 'Other'
			for cat, extensions in FILE_TYPES.items():
				if file_ext in extensions:
					category = cat
					break

			category_path = os.path.join(folder_path, category)
			if not os.path.exists(category_path):
				os.makedirs(category_path)

			shutil.move(file_path, os.path.join(category_path, filename))
			files_moved += 1
			add_log_no_time(log_text, f"- Moved {filename} to {category}")

	return files_moved


def find_duplicates(folder_path, log_text):
	size_dict = {}
	duplicates = []

	for dirpath, _, filenames in os.walk(folder_path):
		for filename in filenames:
			file_path = os.path.join(dirpath, filename)
			file_size = os.path.getsize(file_path)

			if file_size in size_dict:
				duplicates.append((size_dict[file_size], file_path))
			else:
				size_dict[file_size] = file_path

	return duplicates


def get_statistics(folder_path):
	stats = {cat: 0 for cat in FILE_TYPES.keys()}
	stats['Other'] = 0
	total_size = 0

	for dirpath, _, filenames in os.walk(folder_path):
		for filename in filenames:
			file_path = os.path.join(dirpath, filename)
			file_ext = os.path.splitext(filename)[1].lower()

			category = 'Other'
			for cat, extensions in FILE_TYPES.items():
				if file_ext in extensions:
					category = cat
					break
			stats[category] += 1

			total_size += os.path.getsize(file_path)

	return stats, total_size