import getpass, platform

UNAME = getpass.getuser()
OP_SYS = platform.system()

TH_PROFILE_WIN = 'C:\\Users\\' + UNAME + "\AppData\Roaming\Thunderbird"

TH_PROFILE_LINUX = "/home/" + UNAME + "/.thunderbird"

# firefox useful file
FF_PROFILE_WIN = 'C:\\Users\\' + UNAME + "\AppData\Roaming\Mozilla\Firefox"
FF_PROFILE_LINUX = "/home/" + UNAME + "/.mozilla/firefox"
FF_COOKIES = "cookies.sqlite"
FORM_HISTORY = "formhistory.sqlite"
PLACES = "places.sqlite"
MOZ_LOGIN_FILE_DB = "signons.sqlite"
MOZ_LOGIN_FILE_JSON = "logins.json"
LIBNSS_WIN = "nss3.dll"
LIBNSS_LINUX = "libnss3.so"

LIBNSS = LIBNSS_LINUX if OP_SYS == "Linux" else LIBNSS_WIN

# chrome useful file
GCHROME_PROFILE_WIN = 'C:\Users\\' + UNAME + "\AppData\Local\Google\Chrome\User Data"
GCHROME_PROFILE_LINUX = "/home/" + UNAME + "/.config/google-chrome"
GCHROME_LOGIN_FILE = "Login Data"
BOOKMARKS = "Bookmarks"
GCHROME_COOKIES = "Cookies"
HISTORY = "History"
WEB_DATA = "Web Data"
