from interface.main_window import create_window, setup_ui

def main():
    root = create_window()
    app = setup_ui(root)
    app.mainloop()

if __name__ == "__main__":
    main()