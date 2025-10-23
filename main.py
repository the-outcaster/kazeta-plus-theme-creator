import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil
import toml
from PIL import Image
from pydub import AudioSegment
import pathlib

# Attempt to set the GDK backend to Wayland.
try:
    os.environ['GDK_BACKEND'] = 'wayland,x11'
except Exception:
    print("Could not set GDK_BACKEND, using default.")

class KazetaThemeCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("Kazeta+ Theme Creator")
        self.root.geometry("700x620")

        # --- Data Variables ---
        self.theme_name = tk.StringVar()
        self.author = tk.StringVar()
        self.description = tk.StringVar()
        self.menu_position = tk.StringVar()
        self.font_color = tk.StringVar()
        self.cursor_color = tk.StringVar()
        self.bg_scroll = tk.StringVar()
        self.color_shift = tk.StringVar()
        self.bgm_path = tk.StringVar()
        self.logo_path = tk.StringVar()
        self.background_path = tk.StringVar()
        self.font_path = tk.StringVar()
        self.sfx_path = tk.StringVar()

        # --- UI Creation ---
        self._create_widgets()

        self.progress_window = None # progress window

    def _create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        # Column 1 (the entry field) will expand
        main_frame.columnconfigure(1, weight=1)

        positions = ["BottomLeft", "BottomRight", "TopLeft", "TopRight", "Center"]
        colors = ["BLACK", "WHITE", "PINK", "RED", "ORANGE", "YELLOW", "GREEN", "BLUE", "PURPLE"]
        speeds = ["OFF", "SLOW", "NORMAL", "FAST"]

        row_idx = 0

        ttk.Label(main_frame, text="Theme Name:", font=('Helvetica', 10, 'bold')).grid(row=row_idx, column=0, sticky="w", pady=3)
        # Span 3 columns (Entry, Clear, Browse)
        ttk.Entry(main_frame, textvariable=self.theme_name).grid(row=row_idx, column=1, columnspan=3, sticky="ew", pady=3)
        row_idx += 1

        ttk.Label(main_frame, text="Author:", font=('Helvetica', 10, 'bold')).grid(row=row_idx, column=0, sticky="w", pady=3)
        ttk.Entry(main_frame, textvariable=self.author).grid(row=row_idx, column=1, columnspan=3, sticky="ew", pady=3)
        row_idx += 1

        ttk.Label(main_frame, text="Description:", font=('Helvetica', 10, 'bold')).grid(row=row_idx, column=0, sticky="nw", pady=3)
        self.desc_text = tk.Text(main_frame, height=3)
        self.desc_text.grid(row=row_idx, column=1, columnspan=3, sticky="ew", pady=3)
        row_idx += 1

        self._create_dropdown(main_frame, "Menu Position:", self.menu_position, positions, row_idx)
        row_idx += 1
        self._create_dropdown(main_frame, "Font Color:", self.font_color, colors, row_idx)
        row_idx += 1
        self._create_dropdown(main_frame, "Cursor Color:", self.cursor_color, colors, row_idx)
        row_idx += 1
        self._create_dropdown(main_frame, "BG Scroll Speed:", self.bg_scroll, speeds, row_idx)
        row_idx += 1
        self._create_dropdown(main_frame, "Color Shift Speed:", self.color_shift, speeds, row_idx)
        row_idx += 1

        main_frame.grid_rowconfigure(row_idx, minsize=20)
        row_idx += 1

        self._create_file_picker(main_frame, "BGM Track (.ogg):", self.bgm_path, [("Audio Files", "*.ogg *.wav *.mp3"), ("All files", "*.*")], row_idx)
        row_idx += 1
        self._create_file_picker(main_frame, "Logo Image (.png):", self.logo_path, [("Image Files", "*.png *.jpg *.jpeg *.bmp"), ("All files", "*.*")], row_idx)
        row_idx += 1
        self._create_file_picker(main_frame, "Background Image (.png):", self.background_path, [("Image Files", "*.png *.jpg *.jpeg *.bmp"), ("All files", "*.*")], row_idx)
        row_idx += 1
        self._create_file_picker(main_frame, "Font File (.ttf):", self.font_path, [("Font Files", "*.ttf"), ("All files", "*.*")], row_idx)
        row_idx += 1
        self._create_folder_picker(main_frame, "SFX Pack (Folder):", self.sfx_path, row_idx)
        row_idx += 1

        main_frame.grid_rowconfigure(row_idx, minsize=30, weight=1)
        row_idx += 1

        button_frame = ttk.Frame(main_frame)
        # Span all 4 columns
        button_frame.grid(row=row_idx, column=0, columnspan=4, pady=10)
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)

        load_button = ttk.Button(button_frame, text="Load Theme", command=self.load_theme)
        load_button.grid(row=0, column=0, padx=5, sticky="ew")

        export_button = ttk.Button(button_frame, text="Export Theme", command=self.export_theme)
        export_button.grid(row=0, column=1, padx=5, sticky="ew")

        about_button = ttk.Button(button_frame, text="About", command=self._show_about_dialog)
        about_button.grid(row=0, column=2, padx=5, sticky="ew")

    def _show_about_dialog(self):
        about_window = tk.Toplevel(self.root)
        about_window.title("About")
        about_window.geometry("400x200") # Fixed height
        about_window.resizable(False, False)
        about_window.transient(self.root)
        about_window.grab_set()

        about_frame = ttk.Frame(about_window, padding="15")
        about_frame.pack(expand=True, fill="both")
        title_label = ttk.Label(about_frame, text="Kazeta+ Theme Creator", font=('Helvetica', 12, 'bold'))
        title_label.pack(pady=(0, 10))
        desc_text = "This application helps you create and edit themes for Kazeta+ by bundling assets and generating a theme.toml file."
        desc_label = ttk.Label(about_frame, text=desc_text, wraplength=350, justify="center")
        desc_label.pack(pady=5)
        copyright_label = ttk.Label(about_frame, text="© 2025 Linux Gaming Central. All rights reserved.")
        copyright_label.pack(pady=(10, 15))
        ok_button = ttk.Button(about_frame, text="OK", command=about_window.destroy)
        ok_button.pack()
        self.root.wait_window(about_window)

    def _get_default_theme_dir(self):
        default_dir = os.path.expanduser('~/.local/share/kazeta-plus/themes/')
        return default_dir if os.path.isdir(default_dir) else os.path.expanduser('~')

    def _create_dropdown(self, parent, label_text, var, options, row):
        ttk.Label(parent, text=label_text, font=('Helvetica', 10, 'bold')).grid(row=row, column=0, sticky="w", pady=3)
        dropdown = ttk.Combobox(parent, textvariable=var, values=options, state="readonly")
        # Span all 3 "control" columns
        dropdown.grid(row=row, column=1, columnspan=3, sticky="ew", pady=3)
        if options:
            dropdown.current(0)

    def _create_file_picker(self, parent, label_text, var, file_types, row):
        ttk.Label(parent, text=label_text, font=('Helvetica', 10, 'bold')).grid(row=row, column=0, sticky="w", pady=3)

        entry = ttk.Entry(parent, textvariable=var, state="readonly")
        entry.grid(row=row, column=1, sticky="ew", pady=3, padx=(0, 5))

        # --- NEW Clear Button ---
        clear_button = ttk.Button(parent, text="Clear", command=lambda: var.set(""))
        clear_button.grid(row=row, column=2, sticky="ew", pady=3, padx=(0, 5))

        browse_button = ttk.Button(parent, text="Browse...", command=lambda: self._browse_file(var, file_types))
        browse_button.grid(row=row, column=3, sticky="ew", pady=3) # Moved to column 3

    def _create_folder_picker(self, parent, label_text, var, row):
        ttk.Label(parent, text=label_text, font=('Helvetica', 10, 'bold')).grid(row=row, column=0, sticky="w", pady=3)

        entry = ttk.Entry(parent, textvariable=var, state="readonly")
        entry.grid(row=row, column=1, sticky="ew", pady=3, padx=(0, 5))

        # --- NEW Clear Button ---
        clear_button = ttk.Button(parent, text="Clear", command=lambda: var.set(""))
        clear_button.grid(row=row, column=2, sticky="ew", pady=3, padx=(0, 5))

        browse_button = ttk.Button(parent, text="Browse...", command=lambda: self._browse_folder(var))
        browse_button.grid(row=row, column=3, sticky="ew", pady=3) # Moved to column 3

    def _browse_file(self, var, file_types):
        filepath = filedialog.askopenfilename(filetypes=file_types)
        if filepath:
            var.set(filepath)

    def _browse_folder(self, var):
        folderpath = filedialog.askdirectory()
        if folderpath:
            var.set(folderpath)

    def load_theme(self):
        initial_dir = self._get_default_theme_dir()
        toml_path = filedialog.askopenfilename(
            title="Select a theme.toml file",
            initialdir=initial_dir,
            filetypes=[("Theme TOML", "theme.toml"), ("All files", "*.*")]
        )
        if not toml_path: return

        try:
            with open(toml_path, 'r') as f: data = toml.load(f)
            theme_dir = os.path.dirname(toml_path)
            theme_folder_name = os.path.basename(theme_dir)
            self.theme_name.set(theme_folder_name)
            self.author.set(data.get('author', ''))
            self.desc_text.delete('1.0', tk.END)
            self.desc_text.insert('1.0', data.get('description', ''))
            self.menu_position.set(data.get('menu_position', 'BottomLeft'))
            self.font_color.set(data.get('font_color', 'WHITE'))
            self.cursor_color.set(data.get('cursor_color', 'WHITE'))
            self.bg_scroll.set(data.get('background_scroll_speed', 'OFF'))
            self.color_shift.set(data.get('color_shift_speed', 'OFF'))
            asset_map = {'bgm_track': self.bgm_path, 'logo_selection': self.logo_path,
                         'background_selection': self.background_path, 'font_selection': self.font_path,
                         'sfx_pack': self.sfx_path}
            for key, var in asset_map.items():
                asset_name = data.get(key, '')
                if asset_name and asset_name != "None":
                    full_path = os.path.join(theme_dir, asset_name)
                    var.set(full_path if os.path.exists(full_path) else '')
                else: var.set('')
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load theme file: {e}")

    def _create_progress_window(self):
        """Creates and displays a modal progress window."""
        self.progress_window = tk.Toplevel(self.root)
        self.progress_window.title("Exporting...")
        self.progress_window.geometry("350x100")
        self.progress_window.resizable(False, False)
        self.progress_window.transient(self.root)
        self.progress_window.grab_set() # Modal

        frame = ttk.Frame(self.progress_window, padding="15")
        frame.pack(expand=True, fill="both")

        self.progress_message = tk.StringVar(value="Preparing to export...")

        label = ttk.Label(frame, textvariable=self.progress_message, wraplength=320, justify="center")
        label.pack(pady=10)

        # Force the window to draw itself immediately
        self.progress_window.update_idletasks()

    def _update_progress(self, message):
        """Forces an update to the progress window's text."""
        if self.progress_window:
            self.progress_message.set(message)
            self.progress_window.update_idletasks() # This forces the GUI to refresh

    def _destroy_progress_window(self):
        """Safely destroys the progress window."""
        if self.progress_window:
            self.progress_window.destroy()
            self.progress_window = None

    def export_theme(self):
        theme_name_str = self.theme_name.get().strip()
        author_str = self.author.get().strip()

        if not theme_name_str or not author_str:
            messagebox.showerror("Error", "Theme Name and Author are mandatory fields.")
            return

        initial_dir = self._get_default_theme_dir()
        output_parent_dir = filedialog.askdirectory(title="Select where to save the theme folder", initialdir=initial_dir)
        if not output_parent_dir: return

        theme_dir = os.path.join(output_parent_dir, theme_name_str)

        if os.path.isdir(theme_dir):
            if not messagebox.askyesno("Confirm Overwrite", "A theme with this name already exists.\nDo you want to overwrite it?"):
                return

        safe_theme_name = theme_name_str.lower().replace(' ', '_')
        sfx_dir = os.path.join(theme_dir, f"{safe_theme_name}_sfx")

        try:
            # --- Create the progress window ---
            self._create_progress_window()

            self._update_progress("Setting up theme directories...")
            if self.sfx_path.get():
                os.makedirs(sfx_dir, exist_ok=True)
            else:
                if os.path.isdir(sfx_dir):
                    shutil.rmtree(sfx_dir)

            # Process BGM
            bgm_filename = f"{safe_theme_name}_bgm.ogg"
            if self.bgm_path.get():
                self._update_progress("Converting BGM track...")
                self._convert_and_copy_audio(self.bgm_path.get(), os.path.join(theme_dir, bgm_filename))

            # Process Logo
            logo_filename = f"{safe_theme_name}_logo.png"
            if self.logo_path.get():
                self._update_progress("Converting logo image...")
                self._convert_and_copy_image(self.logo_path.get(), os.path.join(theme_dir, logo_filename))

            # Process Background
            bg_filename = f"{safe_theme_name}_background.png"
            if self.background_path.get():
                self._update_progress("Converting background image...")
                self._convert_and_copy_image(self.background_path.get(), os.path.join(theme_dir, bg_filename))

            # Process Font
            font_filename = f"{safe_theme_name}_font.ttf"
            if self.font_path.get():
                self._update_progress("Copying font file...")
                self._safe_copy(self.font_path.get(), os.path.join(theme_dir, font_filename))

            # Process SFX
            sfx_pack_name = f"{safe_theme_name}_sfx"
            if self.sfx_path.get():
                self._update_progress("Processing SFX pack...")
                sfx_files = os.listdir(self.sfx_path.get())
                total_files = len(sfx_files)
                for i, filename in enumerate(sfx_files):
                    # This provides more granular feedback
                    self._update_progress(f"Processing SFX {i+1}/{total_files}:\n{filename}")
                    self._process_sfx_file(os.path.join(self.sfx_path.get(), filename), sfx_dir)

            # Create theme.toml
            self._update_progress("Writing theme.toml file...")
            theme_data = {'author': self.author.get(), 'description': self.desc_text.get("1.0", tk.END).strip(),
                          'menu_position': self.menu_position.get(), 'font_color': self.font_color.get(), 'cursor_color': self.cursor_color.get(),
                          'background_scroll_speed': self.bg_scroll.get(), 'color_shift_speed': self.color_shift.get(),
                          'bgm_track': bgm_filename if self.bgm_path.get() else "None",
                          'logo_selection': logo_filename if self.logo_path.get() else "None",
                          'background_selection': bg_filename if self.background_path.get() else "None",
                          'font_selection': font_filename if self.font_path.get() else "None",
                          'sfx_pack': sfx_pack_name if self.sfx_path.get() else "None"}
            with open(os.path.join(theme_dir, 'theme.toml'), 'w') as f:
                toml.dump(theme_data, f)

            # --- Close the progress window on success ---
            self._destroy_progress_window()
            messagebox.showinfo("Success", f"Theme '{theme_name_str}' exported successfully to:\n{theme_dir}")

        except Exception as e:
            # --- Close the progress window on failure ---
            self._destroy_progress_window()
            messagebox.showerror("Export Failed", f"An error occurred: {e}")

    def _safe_copy(self, src_path, dest_path):
        if os.path.abspath(src_path) != os.path.abspath(dest_path):
            shutil.copy2(src_path, dest_path)

    def _convert_and_copy_audio(self, src_path, dest_path):
        if os.path.abspath(src_path) == os.path.abspath(dest_path): return
        if pathlib.Path(src_path).suffix.lower() == ".ogg":
            self._safe_copy(src_path, dest_path)
            return
        AudioSegment.from_file(src_path).export(dest_path, format="ogg")

    def _convert_and_copy_image(self, src_path, dest_path):
        if os.path.abspath(src_path) == os.path.abspath(dest_path): return
        if pathlib.Path(src_path).suffix.lower() == ".png":
            self._safe_copy(src_path, dest_path)
            return
        with Image.open(src_path) as img:
            img.save(dest_path, "PNG")

    def _process_sfx_file(self, src_path, dest_dir):
        p = pathlib.Path(src_path)
        if not os.path.isfile(src_path): return

        if p.suffix.lower() == ".ogg":
            dest_path = os.path.join(dest_dir, f"{p.stem}.wav")
            AudioSegment.from_ogg(src_path).export(dest_path, format="wav")
        elif p.suffix.lower() == ".wav":
            self._safe_copy(src_path, os.path.join(dest_dir, p.name))

if __name__ == "__main__":
    root = tk.Tk()
    app = KazetaThemeCreator(root)
    root.mainloop()
