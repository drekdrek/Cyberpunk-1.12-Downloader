from getpass import getpass
from urllib.request import urlretrieve
from zipfile import ZipFile
from pathlib import Path
import subprocess, sys, msvcrt, math, os, time, shutil, stat


#CP2077 Downgrader
dotnet_link = r"https://download.visualstudio.microsoft.com/download/pr/c1bfbb13-ad09-459c-99aa-8971582af86e/61553270dd9348d7ba29bacfbb4da7bd/dotnet-sdk-5.0.400-win-x64.exe"
depot_link  = r"https://github.com/SteamRE/DepotDownloader/releases/download/DepotDownloader_2.4.4/depotdownloader-2.4.4.zip"
#ver 1.12

username = ""
password = ""


def on_read_error(func,path,exc_info):
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)

def password_input(prompt:str = "") -> str: #stolen from Stackoverflow ;)
    p_s = ''
    proxy_string = [' '] * 64
    while True:
        sys.stdout.write('\x0D' + prompt + ''.join(proxy_string))
        c = msvcrt.getch()
        if c == b'\r':
            break
        elif c == b'\x08':
            p_s = p_s[:-1]
            proxy_string[len(p_s)] = " "
        else:
            proxy_string[len(p_s)] = "*"
            p_s += c.decode()

    sys.stdout.write('\n')
    return p_s


#checks if dotnet is installed
def parse_tuple_ver(tup:tuple, ver_want:str):
    new_lst2 = []
    lst = list(tup)
    new_lst = lst[1].split("\n")
    if new_lst[0] == 'Unknown option: --list-sdks':
        return False
    for i in range(len(new_lst)):
        new_lst2.append(new_lst[i].split(" ["))
    for i in range(len(new_lst2)):
        ver = new_lst2[i][math.floor(i/2)]
        if ver == ver_want:
            return True
    return False


def download_dotnet():
    cwd = os.getcwd()
    time.sleep(1)
    print("Detecting if correct dotnet version is installed.", end="\r", flush=True)
    s = subprocess.getstatusoutput(f'dotnet --list-sdks')
    is_installed = parse_tuple_ver(s,"5.0.400")
    time.sleep(1)
    if not is_installed: 
        print("dotnet version 5.0.400 is not installed.               ", end="\r", flush=True )
        time.sleep(2)
        print("Downloading dotnet version 5.0.400 installer.", end="\r", flush=True)
        try:
            os.mkdir(cwd + "\\tmp")
        except FileExistsError:
            sys.stdout.write("")
        finally:
            cwd = cwd + '\\tmp'
            time.sleep(2)
            print("Downloading dotnet version 5.0.400 installer..", end="\r", flush=True)
        time.sleep(1)
        print("Downloading dotnet version 5.0.400 installer...   ", end="\r", flush=True)   
        download = urlretrieve(dotnet_link,cwd + "\\dotnet-sdk-5.0.400-win-x64.exe")
        time.sleep(2.5)
        print("please accept the User Account Control prompt    ", end="\r", flush=True)  
        print("installing dotnet.                               ", end="\r", flush=True)  
        cmd = cwd + r"\\dotnet-sdk-5.0.400-win-x64.exe /passive /norestart"
        try: 
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError:
            print("The UAC prompt was denied.")
            time.sleep(2)
            return
        s = subprocess.getstatusoutput(f'dotnet --list-sdks')
        if parse_tuple_ver(s,"5.0.400"):
            print("installed dotnet 5.0.400", end="\r", flush=True)  
    print("dotnet version 5.0.400 is installed.             ", end="\n", flush=True)


def download_depot():
    cwd = os.getcwd()
    time.sleep(1)
    
    try:
        os.mkdir(cwd + "\\tmp")
    except FileExistsError:
        sys.stdout.write("")
    finally:
        cwd = cwd + "\\tmp"
    file = Path(cwd+"\\depotdownloader-2.4.4.zip")
    if not file.is_file():
        print("Downloading Steam DepotDownloader from GitHub", end="\r", flush=True)
        time.sleep(1)
        print("Downloading Steam DepotDownloader from GitHub.", end="\r", flush=True)
    
        download = urlretrieve(depot_link,cwd + "\\depotdownloader-2.4.4.zip")
        time.sleep(2.5)
        print("Downloading Steam DepotDownloader from GitHub..", end="\r", flush=True)

    with ZipFile(cwd + "\\depotdownloader-2.4.4.zip", 'r') as zip_obj:
        zip_obj.extractall("tmp")
    if not file.is_file():
        print("Downloading Steam DepotDownloader from GitHub...", end="\r", flush=True)
        time.sleep(1)
        print("Downloaded Steam DepotDownloader from GitHub.       ", flush=True)
    else:
        print("Steam DepotDownloader is downloaded.             ", flush=True)
        time.sleep(1)
    

def ask_polish(ask:bool=False):

    answers = ['n','y']
    ans = ""
    first = True
    while ans.lower() not in answers:
        if not first:
            print("please enter a valid answer", flush=True)
        if ask:
            print("Would you like to move the Polish Language file? [y/n]: ",end = "", flush=True)
        else:
            print("Would you like to download the Polish Language file? [y/n]: ",end = "", flush=True)
        ans = input()
        first = False
    if ans == "y": 
        return True
    return False

def ask_download(ask:bool=False):
    answers = ['n','y']
    ans = ""
    first = True
    while ans.lower() not in answers:
        if not first:
            print("please enter a valid answer", flush=True)
        if ask:
            print("Would you like to move the 1.12 version? [y/n]: ",end = "", flush=True)
        else:
            print("Would you like to download the 1.12 version? [y/n]: ",end = "", flush=True)
        ans = input()
        first = False
    if ans == "y": 
        return True
    return False

def download_polish(username:str,password:str):
    cwd = os.getcwd() + "\\tmp"
    cmd = "dotnet " + "\"" + cwd + "\\DepotDownloader.dll" + "\"" + " -app 1091500 -depot 1091502 -manifest 4734006406066421322 -username " + username + " -password " + password
    try:
        subprocess.check_call(cmd)
    except Exception as e:
        if str(e)[-2] == "1":
            print("there was an error, it could be one of the following:\n- You entered your Steam account credentials wrong\n- You entered your SteamGuard code wrong\n- You do not have a license for the game on Steam\n- Some other thing idk :shrug:")
            print("Please restart the script.")
            return False
    return True

def download_game(username:str,password:str):


    cwd = os.getcwd() + "\\tmp"
    cmd = "dotnet " + "\"" + cwd + "\\DepotDownloader.dll" + "\"" + " -app 1091500 -depot 1091501 -manifest 6404500526474240765 -username " + username + " -password " + password
    try:
        subprocess.check_call(cmd)
    except Exception as e:
        if str(e)[-2] == "1":
            print("there was an error, it could be one of the following:\n- You entered your Steam account credentials wrong\n- You entered your SteamGuard code wrong\n- You do not have a license for the game on Steam\n- Some other thing idk :shrug:")
            print("Please restart the script.")
            return False
    return True

def transfer_files(polish:bool,game:bool,ask:bool=False): 
    if ask:
        polish = ask_polish(True)
        game = ask_download(True)

    if game or polish:
        cwd = os.getcwd() + "\\depots"
        game_dir = os.getcwd() + "\\Cyberpunk"
        try:
            os.mkdir(game_dir)
        except FileExistsError:
            sys.stdout.write("")

   
    if game:
        try:
            all_files = os.listdir(cwd+"\\1091501\\6840310\\")
            for f in all_files:
                shutil.move(cwd+"\\1091501\\6840310\\" + f, game_dir + "\\" + f)
        except FileNotFoundError:
            sys.stdout.write("")
        except Exception as e:
            print(e)
    if polish:
        try:
            shutil.move(cwd+"\\1091502\\6840310\\archive\\pc\\content\\lang_pl_voice.archive", game_dir+"\\archive\\pc\\content\\lang_pl_voice.archive")
        except FileNotFoundError:
            sys.stdout.write("")


def delete_temp_files():
    print("deleting temp files.",end = "\r", flush=True)
    cwd = os.getcwd()
    time.sleep(1)
    print("deleting temp files..",end = "\r", flush=True)
    shutil.rmtree(cwd + "\\tmp", ignore_errors=True)
    time.sleep(1)
    print("deleting temp files...",end = "\r", flush=True)
    shutil.rmtree(cwd + "\\depots",ignore_errors=True)
    time.sleep(1)    
    print("deleted temp files    ", flush=True)

def main():
#[[--dotnet
    download_dotnet()
#--]]

#[[--depot
    download_depot()
#--]]

#[[--polish voice?
    
    polish = ask_polish()
#--]]

#[[--download 1.12?
    game = ask_download()
#--]]

    if polish or game:
        username = input("Please enter your Steam username: ")
        password = password_input("Please enter your Steam password: ")
    success = False
    if polish:
        success = download_polish(username,password)
    if game: 
        success = download_game(username,password)
    if not polish and not game:
        print("i see you didn't download any of the files, if you already downloaded\nthem but didnt have them move you can choose which ones you want to move now.")
        transfer_files(polish,game,True)
    transfer_files(polish,game)
    if not success:
        answers = ['n','y']
        ans = ""
        first = True
        while ans.lower() not in answers:
            if not first:
                print("please enter a valid answer", flush=True)
            print("Would you like to clear temp files? [y/n]: ",end = "", flush=True)
            ans = input()
            first = False
        if ans == "y":
            success = True
    if success:
        delete_temp_files()
    os.system('pause')
    

if __name__ == "__main__":
    main()
