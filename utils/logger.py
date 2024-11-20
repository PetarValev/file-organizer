from datetime import datetime

def add_log(text_widget, message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    text_widget.configure(state="normal")
    text_widget.insert("end", f"[{timestamp}] {message}\n")
    text_widget.see("end")
    text_widget.configure(state="disabled")

def add_log_no_time(text_widget, message):
    text_widget.configure(state="normal")
    text_widget.insert("end", f"{message}\n")
    text_widget.see("end")
    text_widget.configure(state="disabled")

def clear_log(text_widget):
    text_widget.configure(state="normal")
    text_widget.delete('1.0', 'end')
    text_widget.configure(state="disabled")