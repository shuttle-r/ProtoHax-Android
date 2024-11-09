import os
import subprocess
import time

CRD_SSH_Code = input("Google CRD SSH Code : ")
username = "user"
password = "root"
Pin = 123456
Autostart = True

os.system(f"useradd -m {username}")
os.system(f"echo '{username}:{password}' | sudo chpasswd")
os.system("sed -i 's/\/bin\/sh/\/bin\/bash/g' /etc/passwd")

class CRDSetup:
    def __init__(self, user):
        os.system("apt update -y")
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
        subprocess.run(['wget', 'https://dl.google.com/linux/direct/chrome-remote-desktop_current_amd64.deb'])
        subprocess.run(['dpkg', '--install', 'chrome-remote-desktop_current_amd64.deb'])
        subprocess.run(['apt', 'install', '-y', '--fix-broken'])
        print("Chrome Remote Desktop installed.")

    @staticmethod
    def installDesktopEnvironment():
        os.system("export DEBIAN_FRONTEND=noninteractive")
        os.system("apt install -y openbox lxterminal")
        os.system("echo 'exec openbox-session' > /etc/chrome-remote-desktop-session")
        print("Installed Openbox Desktop Environment.")

    @staticmethod
    def installGoogleChrome():
        subprocess.run(["wget", "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"])
        subprocess.run(["dpkg", "--install", "google-chrome-stable_current_amd64.deb"])
        subprocess.run(['apt', 'install', '-y', '--fix-broken'])
        print("Google Chrome installed.")

    @staticmethod
    def finish(user):
        if Autostart:
            os.makedirs(f"/home/{user}/.config/autostart", exist_ok=True)
            with open(f"/home/{user}/.config/autostart/colab.desktop", "w") as f:
                f.write("""[Desktop Entry]
Type=Application
Name=Colab
Exec=sh -c "sensible-browser www.google.com"
Icon=
Comment=Open a predefined notebook at session signin.
X-GNOME-Autostart-enabled=true""")
            os.system(f"chmod +x /home/{user}/.config/autostart/colab.desktop")
            os.system(f"chown {user}:{user} /home/{user}/.config")
        
        os.system(f"adduser {user} chrome-remote-desktop")
        command = f"{CRD_SSH_Code} --pin={Pin}"
        os.system(f"su - {user} -c '{command}'")
        os.system("service chrome-remote-desktop start")
        print("Setup complete. Log in with PIN: 123456")

try:
    if CRD_SSH_Code == "":
        print("Please enter the CRD authentication code.")
    elif len(str(Pin)) < 6:
        print("Enter a PIN with 6 or more digits.")
    else:
        CRDSetup(username)
except Exception as e:
    print(f"Error: {e}")
