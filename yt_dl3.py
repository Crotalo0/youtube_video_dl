import tkinter as tk
from tkinter import ttk, IntVar, messagebox, filedialog
from pytube import YouTube
from datetime import datetime
from ffmpeg import output, input

# Attenzione quando installi, Alessio, la libreria ffmpeg perche' serve ffmpeg-python.
# - - - - -- - - - - - -- - - - -
# Things to add:
# Random name for audio and video files. DONE
# Add right click menu for paste copy etc... to url_entry. DONE
# Add video thumbnail under video info.
# 
#
# - - - - -- - - - - - -- - - - -

now = datetime.now()


class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Wait..')
        self.create_widgets_dl()

    def create_widgets_dl(self):
        dl_frame = ttk.Frame(self)
        dl_frame.grid(row=1, column=1, sticky=tk.E + tk.W + tk.N + tk.S)

        dl_label = ttk.Label(dl_frame, text="Download in progress...")
        dl_label.grid(row=1, column=1, pady=10, padx=60)


class Window2(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Wait..')
        self.create_widgets_dl()

    def create_widgets_dl(self):
        dl_frame = ttk.Frame(self)
        dl_frame.grid(row=1, column=1, sticky=tk.E + tk.W + tk.N + tk.S)

        dl_label = ttk.Label(dl_frame, text="Merging in progress...\n\nThis could take a while, just wait.")
        dl_label.grid(row=1, column=1, pady=10, padx=60)


class App(tk.Tk):
    SAVE_PATH = ''

    def __init__(self):
        super().__init__()

        self.title("Youtube video/audio downloader")
        p1 = tk.PhotoImage('yt.png')
        self.iconphoto(False, p1)
        self.create_widgets()

        # place a button on the root window

    def create_widgets(self):
        self['padx'] = 10
        self['pady'] = 5

        # - - - - - - - - - - - - - - - - - - - - - 
        # Button command section

        def clear():
            url_entry.delete(0, "end")

        def do_popup(event):
            try:
                m.tk_popup(event.x_root, event.y_root)
            finally:
                m.grab_release()

        def save_path():
            App.SAVE_PATH = filedialog.askdirectory()
            if App.SAVE_PATH:
                sub2_path['text'] = App.SAVE_PATH
                return App.SAVE_PATH

        def get_info():
            link = url_entry.get()
            yt = YouTube(link)
            info_label['text'] = f"Title: {yt.title}"

        def downloader():
            video_dl = var1.get()
            audio_dl = var2.get()
            link = url_entry.get()

            merging_win = None

            try:
                yt = YouTube(link)

                dl_win = Window(self)
                dl_win.grab_set()
                dl_win.update()
                video_filename = now.strftime('%Y_%m_%d_%H_%M_%S') + '.mp4'
                audio_filename = now.strftime('%Y_%m_%d_%H_%M_%S') + '.mp4'

                if video_dl == 1 and audio_dl == 0:
                    new_path_video = str(App.SAVE_PATH) + r'\video'
                    yt.streams.filter(only_video=True).first().download(output_path=new_path_video,
                                                                        filename=video_filename)

                    dl_win.destroy()
                    messagebox.showinfo("Information", "Video downloaded successfully!")

                elif audio_dl == 1 and video_dl == 0:
                    new_path_audio = str(App.SAVE_PATH) + r'\audio'
                    yt.streams.filter(only_audio=True).first().download(output_path=new_path_audio,
                                                                        filename=audio_filename)

                    dl_win.destroy()
                    messagebox.showinfo("Information", "Audio downloaded successfully!")

                else:
                    new_path_video = str(App.SAVE_PATH) + r'\video'
                    new_path_audio = str(App.SAVE_PATH) + r'\audio'

                    yt.streams.filter(only_video=True, file_extension='mp4').first().download(
                        output_path=new_path_video, filename=video_filename)
                    yt.streams.filter(only_audio=True, file_extension='mp4').first().download(
                        output_path=new_path_audio, filename=audio_filename)

                    dl_win.destroy()
                    messagebox.showinfo("Information", "Audio and video downloaded successfully!")

                    final_path_video = str(App.SAVE_PATH) + r'/video' + f'/{video_filename}'
                    final_path_audio = str(App.SAVE_PATH) + r'/audio' + f'/{audio_filename}'

                    merging_win = Window2(self)
                    merging_win.grab_set()
                    merging_win.update()

                    for i in final_path_video:
                        if i == "/":
                            final_path_video.replace(i, '\\')
                            final_path_audio.replace(i, '\\')

                    print(final_path_audio, final_path_video)
                    video_stream = input(final_path_video)
                    audio_stream = input(final_path_audio)
                    new_title = str(App.SAVE_PATH) + f"/{yt.title}_new.mp4"

                    output(audio_stream, video_stream, new_title).run()
                    messagebox.showinfo("Information", "Merging Audio and Video ended!\nYour file is ready.")

            except Exception:
                messagebox.showerror('Error',
                                     'An error has occurred. \nCheck internet connection and make sure the link is '
                                     'correct.')
            finally:
                if merging_win is not None:
                    merging_win.destroy()

        # - - - - - - - - - - - - - - - - - - - - -
        # The URL frame
        url_frame = ttk.LabelFrame(self, text=" URL ", relief=tk.RIDGE)
        url_frame.grid(row=1, column=1, sticky=tk.E + tk.W + tk.N + tk.S)

        url_label = ttk.Label(url_frame, text="Insert URL: ")
        url_label.grid(row=1, column=1, sticky=tk.W, pady=5, padx=10)

        url_entry = ttk.Entry(url_frame)
        url_entry.grid(row=1, column=2, sticky=tk.E, pady=5, padx=10, ipadx=90)

        # Adding a right click menu to entry url bar.
        right_click_bar = tk.Menu(self)

        m = tk.Menu(right_click_bar, tearoff=0)

        m.add_command(label="Cut", command=lambda: url_entry.event_generate('<Control-x>'))
        m.add_command(label="Copy", command=lambda: url_entry.event_generate('<Control-c>'))
        m.add_command(label="Paste", command=lambda: url_entry.event_generate('<Control-v>'))
        m.add_separator()
        m.add_command(label='Highlight all', command=lambda: url_entry.select_range(0, "end"))
        m.add_separator()
        m.add_command(label="Clear entry", command=clear)

        url_entry.bind("<Button-3>", do_popup)
        # Finishing to add right click menu bar.

        # - - - - - - - - - - - - - - - - - - - - -
        # Info frame
        info_frame = ttk.LabelFrame(self, text=" Video Info ", relief=tk.RIDGE)
        info_frame.grid(row=3, column=1, sticky=tk.E + tk.W + tk.N + tk.S)

        info_label = ttk.Label(info_frame, text="", justify=tk.CENTER, font=("Calibri", 10, "italic"))
        info_label.grid(row=1, column=1, sticky=tk.W, pady=5, padx=10)

        # - - - - - - - - - - - - - - - - - - - - -
        # The main bottom frame
        main_frame = ttk.Frame(self, padding=6)
        main_frame.grid(row=2, column=1, padx=6)

        # - - - - - - - - - - - - - - - - - - - - -
        # Additional info (sub1) frame
        sub1_frame = ttk.LabelFrame(main_frame, text=" Additional options ", relief=tk.RIDGE)
        sub1_frame.grid(row=2, column=1, sticky=tk.E + tk.N + tk.S, padx=6)

        var1 = IntVar()
        video_dl_check = ttk.Checkbutton(sub1_frame, text="Download only video", variable=var1, onvalue=True,
                                         offvalue=False)
        video_dl_check.grid(row=1, column=1, pady=3, padx=5)

        var2 = IntVar()
        audio_dl_check = ttk.Checkbutton(sub1_frame, text="Download only audio", variable=var2, onvalue=True,
                                         offvalue=False)
        audio_dl_check.grid(row=2, column=1, pady=3, padx=5)

        sub1_label = ttk.Label(sub1_frame, text="If nothing checked, \nwill download \naudio and video",
                               justify=tk.CENTER, font=("Calibri", 9, "italic"))
        sub1_label.grid(row=3, column=1, sticky=tk.W, pady=3, padx=25)

        # - - - - - - - - - - - - - - - - - - - - -
        # Button (sub2) frame
        sub2_frame = ttk.LabelFrame(main_frame, text=" Buttons ", relief=tk.RIDGE)
        sub2_frame.grid(row=2, column=2, sticky=tk.N + tk.S, padx=6)

        sub2_dir = ttk.Label(sub2_frame, text="Current save directory: ", font=("Calibri", 9, "italic"))
        sub2_dir.grid(row=1, column=1, pady=3, padx=3)

        sub2_path = ttk.Label(sub2_frame, text="Same folder as the program", font=("Calibri", 9, "italic"))
        sub2_path.grid(row=2, column=1, pady=3, padx=3)

        save_path = ttk.Button(sub2_frame, text="Set save path...", command=save_path)
        save_path.grid(row=3, column=1, pady=3, padx=58)

        video_info = ttk.Button(sub2_frame, text="Get video info", command=get_info)
        video_info.grid(row=4, column=1, pady=3, padx=58)

        dl_button = ttk.Button(sub2_frame, text="Start download!", command=downloader)
        dl_button.grid(row=5, column=1, sticky=tk.W, pady=5, padx=5, ipady=5, ipadx=58)

        # - - - - - - - - - - - - - - - - - - - - -
        # Menus
        menubar = tk.Menu(self)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=self.quitting)
        menubar.add_cascade(label="File", menu=filemenu)

        self.config(menu=menubar)

    def quitting(self):
        answer = messagebox.askyesno("Question", "Do you really want to quit?")
        if answer is True:
            # I need the () at the end if I am not giving the command to a button.
            self.quit()


if __name__ == "__main__":
    app = App()
    app.mainloop()
