import os
import threading
import wx
import yt_dlp
btnText = "Download"

class windowclass(wx.Frame):


    def __init__(self, *args, **kwargs):
        super(windowclass, self).__init__(*args, **kwargs)
      
      
        self.InitUI()   
   
    def InitUI(self):
        panel = wx.Panel(self)
      
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.text = wx.StaticText(panel, label="Paste YouTube Video URL Link Here:", style=wx.ALIGN_CENTER)   
        vbox.Add(self.text, flag=wx.ALIGN_CENTER|wx.TOP, border=35)
        self.text_ctrl = wx.TextCtrl(panel)
        vbox.Add(self.text_ctrl, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=20)

        self.save_dir = os.getcwd()
        dir_box = wx.BoxSizer(wx.HORIZONTAL)
        self.dir_text = wx.TextCtrl(panel, value=self.save_dir, style=wx.TE_READONLY)
        browse_button = wx.Button(panel, label="Choose Folder")
        browse_button.Bind(wx.EVT_BUTTON, self.on_browse_folder)
        dir_box.Add(self.dir_text, 1, wx.EXPAND|wx.ALL, 5)
        dir_box.Add(browse_button, 0, wx.ALL, 5)
        vbox.Add(dir_box, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        #when clicked the button will call the load_and_download function
        download_button = wx.Button(panel, label=btnText)
        clear_button = wx.Button(panel, label="Clear")

        download_button.Bind(wx.EVT_BUTTON, self.load_and_download)
        clear_button.Bind(wx.EVT_BUTTON, self.clear_text)

        # Place the two buttons horizontally
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(download_button, 1, wx.EXPAND|wx.ALL, 10)
        hbox.Add(clear_button, 0, wx.EXPAND|wx.ALL, 10)

        vbox.Add(hbox, flag=wx.ALIGN_CENTER|wx.TOP, border=0)

         # 1. Instantiate the progress bar widget and its label
        self.gauge_label = wx.StaticText(panel, label="0%")
        self.gauge = wx.Gauge(panel, range=100, size=(250, 0)) 

        gauge_hbox = wx.BoxSizer(wx.HORIZONTAL)
        gauge_hbox.Add(self.gauge_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        gauge_hbox.Add(self.gauge, 1, wx.EXPAND)

        vbox.Add(gauge_hbox, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 35)
        
        panel.SetSizer(vbox)

        #status bar

        self.sb=self.CreateStatusBar()
   



    def on_browse_folder(self, event):
        dialog = wx.DirDialog(self, "Choose download folder", defaultPath=self.save_dir, style=wx.DD_DEFAULT_STYLE)
        if dialog.ShowModal() == wx.ID_OK:
            self.save_dir = dialog.GetPath()
            self.dir_text.SetValue(self.save_dir)
        dialog.Destroy()

    def clear_text(self, event):
        self.text_ctrl.SetValue("")  # Clear the text control
        #self.status_text.SetLabel("")  # Clear the status message
        self.sb.SetStatusText("")
    

    def load_and_download(self, event):
        video_url = self.text_ctrl.GetValue().strip()
        if not video_url:
            self.sb.SetStatusText("Error: You must enter a URL.")
            return

        #self.status_text.SetLabel("Downloading..."+ "\n")
        self.sb.SetStatusText(" Downloading...")
        self.sb.Refresh()   
        self.sb.Update()
        #self.status_text.Refresh()
        #self.status_text.Update()

        download_thread = threading.Thread(target=self.download_video, args=(video_url,), daemon=True)
        download_thread.start()

    

    def download_video(self, video_url):
        filename_template = os.path.join(self.save_dir, '%(title)s.%(ext)s')

        def custom_hook(d):
            if d['status'] == 'downloading':
                # Extract progress metrics
                total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
                downloaded = d.get('downloaded_bytes', 0)
                
                if total > 0:
                    percent = downloaded / total * 100
                    # Update the GUI progress bar safely from the background thread
                    # Update the GUI progress bar and label safely from the background thread
                    wx.CallAfter(self.gauge.SetValue, int(percent))
                    wx.CallAfter(self.gauge_label.SetLabel, f"{int(percent)}%")
            
            elif d['status'] == 'finished':
                wx.CallAfter(self.gauge.SetValue, 100)
                wx.CallAfter(self.gauge_label.SetLabel, "100%")
                print("Download finished! Packaging file...")
        
      
        ydl_opts ={
            # Use a single best format so ffmpeg is not required for merging.
            'format': 'best',
            'outtmpl': filename_template,
            'noplaylist': True,
            'progress_hooks': [custom_hook],
            #'quiet': True, # Suppress yt-dlp's default noisy terminal output
            
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
               
            
            wx.CallAfter(self.on_download_complete, True, "Download completed successfully!")
        except Exception as e:
            wx.CallAfter(self.on_download_complete, False, f"An error occurred: {e}")

    def on_download_complete(self, success, message):
        # Reset progress bar for the next task
        self.gauge.SetValue(0)
        self.gauge_label.SetLabel("0%")
        
        if success:
            #self.status_text.SetLabel(message)
            self.sb.SetStatusText(message)
        else:
            #self.status_text.SetLabel("Download failed.")
            self.sb.SetStatusText("Download failed.")
            wx.MessageBox(message, "Error", wx.OK | wx.ICON_ERROR)


#run the app
if __name__ == '__main__':        

    app = wx.App()
    frame = windowclass(None, title='YouTube Downloader', size=(500, 275))
    frame.Show()
    frame.Center()
    app.MainLoop()       