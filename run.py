import os
import subprocess
import shutil
import random
import time

CRD_SSH_Code = input("Google CRD SSH Code :")
username = "user" #@param {type:"string"}
password = "root" #@param {type:"string"}
os.system(f"useradd -m {username}")
os.system(f"adduser {username} sudo")
os.system(f"echo '{username}:{password}' | sudo chpasswd")
os.system("sed -i 's/\/bin\/sh/\/bin\/bash/g' /etc/passwd")

Pin = 123456 #@param {type: "integer"}
Autostart = True #@param {type: "boolean"}

class CRDSetup:
    def __init__(self, user):
        os.system("apt update -y > /dev/null 2>&1")
        time.sleep(1)
        self.installCRD()
        time.sleep(1)
        self.installDesktopEnvironment()
        time.sleep(1)
        self.installGoogleChrome()
        time.sleep(1)
        self.finish(user)

    @staticmethod
    def installCRD():
        subprocess.run(['wget', 'https://dl.google.com/linux/direct/chrome-remote-desktop_current_amd64.deb'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(['dpkg', '--install', 'chrome-remote-desktop_current_amd64.deb'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(['apt', 'install', '--assume-yes', '--fix-broken'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Desk installed.")

    @staticmethod
    def installDesktopEnvironment():
        os.system("export DEBIAN_FRONTEND=noninteractive")
        os.system("apt install --assume-yes xfce4 desktop-base xfce4-terminal > /dev/null 2>&1")
        os.system("bash -c 'echo \"exec /etc/X11/Xsession /usr/bin/xfce4-session\" > /etc/chrome-remote-desktop-session'")
        os.system("apt remove --assume-yes gnome-terminal > /dev/null 2>&1")
        os.system("apt install --assume-yes xscreensaver > /dev/null 2>&1")
        os.system("sudo apt purge light-locker > /dev/null 2>&1")
        os.system("sudo apt install --reinstall xfce4-screensaver > /dev/null 2>&1")
        os.system("systemctl disable lightdm.service > /dev/null 2>&1")
        print("Desk Enviro installed.")

    @staticmethod
    def installGoogleChrome():
        subprocess.run(["wget", "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["dpkg", "--install", "google-chrome-stable_current_amd64.deb"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(['apt', 'install', '--assume-yes', '--fix-broken'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Gchrome installed.")


    @staticmethod
    def finish(user):
        if Autostart:
            os.makedirs(f"/home/{user}/.config/autostart", exist_ok=True)
            link = "www.google.com"
            colab_autostart = """[Desktop Entry]
            print("Finishing touch.")

Type=Application
Name=Colab
Exec=sh -c "sensible-browser {}"
Icon=
Comment=Open a predefined notebook at session signin.
X-GNOME-Autostart-enabled=true""".format(link)
            with open(f"/home/{user}/.config/autostart/colab.desktop", "w") as f:
                f.write(colab_autostart)
            os.system(f"chmod +x /home/{user}/.config/autostart/colab.desktop > /dev/null 2>&1")
            os.system(f"chown {user}:{user} /home/{user}/.config > /dev/null 2>&1")
            
        os.system(f"adduser {user} chrome-remote-desktop > /dev/null 2>&1")
        command = f"{CRD_SSH_Code} --pin={Pin}"
        os.system(f"su - {user} -c '{command}' > /dev/null 2>&1")
        os.system("service chrome-remote-desktop start > /dev/null 2>&1")
        print("PIN: 123456") 
        while True:
            time.sleep(1)  # Wait for 1 second
            numberguess = random.randint(1, 922843)  # Generate a random number between 1 and 922843

            if numberguess == 23578:  # Check if the number matches the target
                print("guessed")  # Print "guessed" if it matches

try:
    if CRD_SSH_Code == "":
        print("Please enter authcode from the given link")
    elif len(str(Pin)) < 6:
        print("Enter a pin more or equal to 6 digits")
    else:
        CRDSetup(username)
except NameError as e:
    print("'username' variable not found, Create a user first")
