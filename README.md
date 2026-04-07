
# Batch Video Downloader GUI

A lightweight, user-friendly graphical interface (GUI) for the powerful command-line tool `yt-dlp`. This tool is designed to simplify batch video downloading tasks on Windows.
<img width="2125" height="2030" alt="image" src="https://github.com/user-attachments/assets/5d756d94-85f8-4314-8d65-999a77f49fa0" />

## 📜 Disclaimer & Credits

This script is **only a GUI wrapper** for the incredible open-source software **yt-dlp**. It does not perform the downloading logic itself but rather generates and executes the necessary commands for you.

Please support the original developers of the backend engine by giving them a star on GitHub:
⭐ **[yt-dlp GitHub Repository](https://github.com/yt-dlp/yt-dlp)**

---

## 💻 Runtime Environment

To run this script, ensure you have the following:

1.  **Operating System**: Windows (Optimized for Windows file paths and encoding).
2.  **Python**: Version 3.1 or higher.
3.  **Required Binaries**:
    *   **yt-dlp.exe**: The core downloader engine.
    *   **FFmpeg**: Required for merging high-quality video and audio streams.
    *   **deno.exe**: (Optional) Required if the specific site requires JS-runtime for decryption.
For detailed instructions on using yt-dlp, please refer to the yt-dlp project.
**[yt-dlp GitHub Repository](https://github.com/yt-dlp/yt-dlp)**
---

## 🛠 Field Descriptions

| Field | Description |
| :--- | :--- |
| **yt-dlp Program Position** | Select the path to your `yt-dlp_x86.exe` (or `yt-dlp.exe`) file. |
| **ffmpeg Directory** | Select the folder containing `ffmpeg.exe` (usually the `bin` folder of your FFmpeg installation). |
| **Download Directory** | The local folder where your downloaded videos will be saved. |
| **Cookies Setting** | Enable this if the video requires authentication (e.g., age-restricted or member-only content). Select your exported `cookies.txt` file.Export the cookies with an extension such as **[this](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)** |
| **Video URL List** | Paste your video links here. Supports batch input (one URL per line). |
| **Operation Status** | A real-time console log showing download progress, file names, and speeds. |

---

## 🌟 Key Advantages

*   **Auto-Configuration Persistence**: Your paths and settings are automatically saved to a local `dl_config.json` file. You don't need to re-enter paths every time you open the app.
*   **Real-time Progress Tracking**: Unlike basic scripts, this UI captures `yt-dlp` output to show live download percentages and speeds without refreshing the entire log window.
*   **Non-Blocking Interface**: Built with Python multi-threading; the GUI remains responsive and won't "freeze" while a heavy download is in progress.
*   **Clean & Centered Layout**: The window automatically calculates your screen resolution to launch perfectly in the center of your monitor.
*   **Flexible Naming Convention**: Uses a standard `%(title)s_%(resolution)s.%(ext)s` format to keep your library organized.

---

## 🚀 How to Use

1.  Download the Python script to your computer.
2.  Install Python if you haven't already.
3.  Run the script: `python dl.py`.
4.  Configure your local file paths once.
5.  Paste your URLs and click **"Start Batch Download"**.
