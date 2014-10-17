import getpass, platform, os

UNAME = getpass.getuser()
OP_SYS = platform.system()
WIN_APPDATA = "C:\\Users\\" + UNAME + "\\AppData\\"
LINUX_HOME = "/home/" + UNAME + "/"

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

# chrome useful file
GCHROME_PROFILE_WIN = WIN_APPDATA + "Local\\Google\\Chrome\\User Data"
GCHROME_PROFILE_LINUX = LINUX_HOME + ".config/google-chrome"
GCHROME_LOGIN_FILE = "Login Data"
BOOKMARKS = "Bookmarks"
GCHROME_COOKIES = "Cookies"
HISTORY = "History"
WEB_DATA = "Web Data"

# Cloud 
DROPBOX_WIN = WIN_APPDATA + "Roaming\\Dropbox"
DROPBOX_LINUX = LINUX_HOME + ".dropbox"
GDRIVE = WIN_APPDATA + "Local\\Google\\Drive"
ONEDRIVE = WIN_APPDATA + "Local\\Microsoft\\SkyDrive"
