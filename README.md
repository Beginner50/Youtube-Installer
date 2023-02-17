# Youtube-Installer
A Youtube Installer App with a File Explorer.

Features an easy to use video downloader with several video and audio resolutions supported
along with a file explorer tab with a rich set of tools
- Move Files
- Create Folders
- Set Download Paths
- Rename Files and Folders
- Delete Files and Folders

![YtDownloaderFront](https://user-images.githubusercontent.com/118896436/219302074-57e80a6a-b5fb-46e5-ac8b-411ab35b647c.png)

![YoutubeDownloaderFileExplorer](https://user-images.githubusercontent.com/118896436/219302205-b3fec99c-cb8b-4788-8eab-215265d20de7.png)


# Installation
### Python needs to be installed in order for the program to work
#### Skip to section 2 if you don't have git installed

### Section 1)
#### 1) Open up the terminal and type in the following commands
        git init
        git clone https://github.com/Beginner50/Youtube-Installer.git
        cd \Youtube-Installer
     
#### 2) Run the program
Note that it will take some time to download dependencies when first running the program

        python App.py
     
### Section 2)
#### 1) Download the zip file and extract it to a desired location
#### 2) Double click on App.py


## Known Bugs
#### 1) 1080p video resolution is not supported due to how YouTube processes and stores them. Contributors can help by fixing this bug.
##### (Hint: The program should download both the 1080p video and its corresponding audio file when 1080p is selected and merge them using ffmpeg)
#### 2) Not a bug, but the FileButtonManager interface should be reworked
##### (Code needs to be edited to provide a clearer and more consistent relationship between the explorer frames and the FileButtonManager interface)
