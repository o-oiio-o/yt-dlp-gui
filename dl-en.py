import os
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import json

CONFIG_FILE = "dl_config.json"

class VideoDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Batch Video Downloader - Developed by Colin")

        # --- Window Centering Logic ---
        width = 850
        height = 780
        # Get screen dimensions
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        # Calculate coordinates
        x = (screen_w // 2) - (width // 2)
        y = (screen_h // 2) - (height // 2)
        # Set geometry
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        # -----------------------
        self.root.configure(bg="#f0f0f0") # Set background color

        # Variable definitions
        self.yt_dlp_path = tk.StringVar()
        self.ffmpeg_path = tk.StringVar()
        self.download_dir = tk.StringVar()
        self.use_cookies = tk.BooleanVar(value=False)
        self.cookies_path = tk.StringVar()
        
        self.last_line_is_progress = False # Flag for overwriting progress lines

        self.create_widgets()
        self.load_config()

    def create_widgets(self):
        # Set global padding
        padx, pady = 20, 8
        
        # 1. Title (Developed by Colin)
        title_label = tk.Label(self.root, text="Batch Video Downloader", 
                               font=("Segoe UI", 18, "bold"), bg="#f0f0f0")
        title_label.grid(row=0, column=0, columnspan=3, pady=25)

        # Entry Style
        entry_style = {"font": ("Segoe UI", 10), "relief": "flat", "highlightthickness": 1, "highlightbackground": "#ccc"}

        # 2. yt-dlp Path
        tk.Label(self.root, text="yt-dlp Path:", bg="#f0f0f0").grid(row=1, column=0, sticky="e", padx=padx, pady=pady)
        tk.Entry(self.root, textvariable=self.yt_dlp_path, width=80, **entry_style).grid(row=1, column=1, padx=padx, pady=pady, sticky="ew")
        tk.Button(self.root, text="Browse", command=self.browse_yt_dlp, width=8).grid(row=1, column=2, padx=padx, pady=pady)

        # 3. ffmpeg Directory
        tk.Label(self.root, text="ffmpeg Directory:", bg="#f0f0f0").grid(row=2, column=0, sticky="e", padx=padx, pady=pady)
        tk.Entry(self.root, textvariable=self.ffmpeg_path, width=80, **entry_style).grid(row=2, column=1, padx=padx, pady=pady, sticky="ew")
        tk.Button(self.root, text="Browse", command=self.browse_ffmpeg, width=8).grid(row=2, column=2, padx=padx, pady=pady)

        # 4. Download Directory
        tk.Label(self.root, text="Download Dir:", bg="#f0f0f0").grid(row=3, column=0, sticky="e", padx=padx, pady=pady)
        tk.Entry(self.root, textvariable=self.download_dir, width=80, **entry_style).grid(row=3, column=1, padx=padx, pady=pady, sticky="ew")
        tk.Button(self.root, text="Browse", command=self.browse_download, width=8).grid(row=3, column=2, padx=padx, pady=pady)

        # 5. Cookies Settings
        tk.Label(self.root, text="Cookies Settings:", bg="#f0f0f0").grid(row=4, column=0, sticky="e", padx=padx, pady=pady)
        cookie_frame = tk.Frame(self.root, bg="#f0f0f0")
        cookie_frame.grid(row=4, column=1, sticky="ew")
        
        tk.Checkbutton(cookie_frame, text="Cookies are required", variable=self.use_cookies, bg="#f0f0f0").pack(side=tk.LEFT)
        tk.Entry(cookie_frame, textvariable=self.cookies_path, width=54, **entry_style).pack(side=tk.LEFT, padx=(10,0))
        
        tk.Button(self.root, text="Browse", command=self.browse_cookies, width=8).grid(row=4, column=2, padx=padx, pady=pady)

        # 6. Video URL List
        tk.Label(self.root, text="Video URL List:", bg="#f0f0f0").grid(row=5, column=0, sticky="ne", padx=padx, pady=pady)
        self.url_text = tk.Text(self.root, height=10, width=80, font=("Consolas", 10), relief="flat")
        self.url_text.grid(row=5, column=1, padx=padx, pady=pady, sticky="ew")

        # 7. Execution Log
        tk.Label(self.root, text="Execution Log:", bg="#f0f0f0").grid(row=6, column=0, sticky="ne", padx=padx, pady=pady)
        self.log_text = tk.Text(self.root, height=12, width=80, bg="#1e1e1e", fg="#ffffff", font=("Segoe UI", 9), relief="flat")
        self.log_text.grid(row=6, column=1, padx=padx, pady=pady, sticky="ew")

        # 8. Start Download Button
        self.start_btn = tk.Button(self.root, text="Start Batch Download", command=self.start_download_thread, 
                                   bg="#0078d7", fg="white", font=("Segoe UI", 10, "bold"), 
                                   height=2, width=25, relief="flat")
        self.start_btn.grid(row=7, column=1, pady=25)

        # Configure column weight
        self.root.grid_columnconfigure(1, weight=1)

    # --- Helpers ---
    def browse_yt_dlp(self):
        file = filedialog.askopenfilename(filetypes=[("EXE", "*.exe")]); 
        if file: self.yt_dlp_path.set(file.replace("/", "\\"))

    def browse_ffmpeg(self):
        path = filedialog.askdirectory(); 
        if path: self.ffmpeg_path.set(path.replace("/", "\\"))

    def browse_download(self):
        path = filedialog.askdirectory(); 
        if path: self.download_dir.set(path.replace("/", "\\"))

    def browse_cookies(self):
        file = filedialog.askopenfilename(filetypes=[("Text", "*.txt"), ("All", "*.*")]); 
        if file: 
            self.cookies_path.set(file.replace("/", "\\"))
            self.use_cookies.set(True)

    def log(self, message, is_progress=False):
        self.log_text.config(state='normal')
        if is_progress and self.last_line_is_progress:
            self.log_text.delete("end-2l", "end-1l")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.last_line_is_progress = is_progress
        self.log_text.config(state='disabled')

    def save_config(self):
        config = {
            "yt": self.yt_dlp_path.get(), "ff": self.ffmpeg_path.get(), 
            "dir": self.download_dir.get(), "ck": self.cookies_path.get(),
            "ck_on": self.use_cookies.get()
        }
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False)

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    c = json.load(f)
                    self.yt_dlp_path.set(c.get("yt", ""))
                    self.ffmpeg_path.set(c.get("ff", ""))
                    self.download_dir.set(c.get("dir", ""))
                    self.cookies_path.set(c.get("ck", ""))
                    self.use_cookies.set(c.get("ck_on", False))
            except: pass

    def start_download_thread(self):
        if not self.yt_dlp_path.get() or not self.url_text.get("1.0", tk.END).strip():
            messagebox.showwarning("Notice", "Please complete program paths and provide a URL list.")
            return
        self.save_config()
        threading.Thread(target=self.run_downloads, daemon=True).start()

    def run_downloads(self):
        self.start_btn.config(state='disabled', bg="#cccccc")
        
        # Extract global settings
        ffmpeg_bin = self.ffmpeg_path.get()
        yt_exe = self.yt_dlp_path.get()
        out_dir = self.download_dir.get()
        use_ck = self.use_cookies.get()
        ck_path = self.cookies_path.get()
        
        # 1. Temp PATH setup
        current_env = os.environ.copy()
        if ffmpeg_bin:
            current_env["PATH"] = ffmpeg_bin + os.pathsep + current_env["PATH"]

        urls = [u.strip() for u in self.url_text.get("1.0", tk.END).splitlines() if u.strip()]
        
        # Output template
        out_tpl = os.path.join(out_dir, r"%(title)s_%(resolution)s.%(ext)s")

        for i, url in enumerate(urls):
            self.log(f">>> Downloading [{i+1}/{len(urls)}]: {url}")
            
            # 2. Build command
            cmd = [yt_exe]
            if use_ck and ck_path:
                cmd.extend(["--cookies", ck_path])
            
            cmd.extend([
                "--js-runtimes", "node",
                "--newline", # Refresh progress per line
                "-o", out_tpl,
                url
            ])

            try:
                # 3. Execution
                process = subprocess.Popen(
                    cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    universal_newlines=True, env=current_env,
                    encoding='gbk', errors='replace', bufsize=1
                )

                for line in process.stdout:
                    msg = line.strip()
                    if not msg: continue
                    # Identify progress info
                    if "[download]" in msg and "%" in msg:
                        self.log(msg, is_progress=True)
                    else:
                        self.log(msg, is_progress=False)

                process.wait()
                if process.returncode == 0:
                    self.log(f"--- Task Completed ---")
                else:
                    self.log(f"!!! Download Interrupted (Error Code: {process.returncode})")

            except Exception as e:
                self.log(f"Error: {str(e)}")

        self.log("\n====== All Download Tasks Finished ======")
        self.start_btn.config(state='normal', bg="#0078d7")
        messagebox.showinfo("Done", "Batch processing finished.")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoDownloaderApp(root)
    root.mainloop()