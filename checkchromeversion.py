import os
import shutil
import requests
import win32api
import subprocess

def getFileProperties(fname) -> dict:
    """
    Read all properties of the given file and return them as a dictionary.
    """
    propNames = ('Comments', 'InternalName', 'ProductName',
                 'CompanyName', 'LegalCopyright', 'ProductVersion',
                 'FileDescription', 'LegalTrademarks', 'PrivateBuild',
                 'FileVersion', 'OriginalFilename', 'SpecialBuild')

    props = {'FixedFileInfo': None, 'StringFileInfo': None, 'FileVersion': None}

    try:
        fixedInfo = win32api.GetFileVersionInfo(fname, '\\')
        props['FixedFileInfo'] = fixedInfo
        props['FileVersion'] = "%d.%d.%d.%d" % (fixedInfo['FileVersionMS'] / 65536,
                                                fixedInfo['FileVersionMS'] % 65536,
                                                fixedInfo['FileVersionLS'] / 65536,
                                                fixedInfo['FileVersionLS'] % 65536)

        lang, codepage = win32api.GetFileVersionInfo(fname, '\\VarFileInfo\\Translation')[0]

        strInfo = {}
        for propName in propNames:
            strInfoPath = u'\\StringFileInfo\\%04X%04X\\%s' % (lang, codepage, propName)
            strInfo[propName] = win32api.GetFileVersionInfo(fname, strInfoPath)

        props['StringFileInfo'] = strInfo
    except:
        pass

    return props

class ChromeVersionChecker:
    def __init__(self, required_version):
        self.required_version = required_version

    def get_chrome_version(self):
        output = self.query_registry()
        version = self.extract_version(output)
        return version[:3] if version else None

    def query_registry(self):
        command = r'reg query "HKLM\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Google Chrome"'
        stream = os.popen(command)
        return stream.read()
    
    def extract_version(self, output):
        try:
            start_index = output.rindex('DisplayVersion    REG_SZ') + 24
            end_index = output.find('\n', start_index)
            version = output[start_index:end_index].strip()
            return version
        except (TypeError, ValueError):
            return None

    def check_version(self):
        current_version = self.get_chrome_version()
        return current_version == self.required_version

class ChromeDownloader:
    def __init__(self, download_url, file_name):
        self.download_url = download_url
        self.file_name = file_name

    def download_chrome(self):
        print("Downloading ... ")
        response = requests.get(self.download_url)
        with open(self.file_name, 'wb') as file:
            file.write(response.content)
        print("Download Complete!")

class ChromeInstaller:
    def __init__(self, file_name, current_version=None):
        self.file_name = file_name
        self.current_version = current_version

    def uninstall_chrome(self, versionChrome):
        if not self.current_version:
            print("Current version not found, skipping uninstallation.")
            return

        uninstaller_path = f'"C:\\Program Files\\Google\\Chrome\\Application\\{self.current_version}\\Installer\\setup.exe"'
        print(f"Start uninstalling Google Chrome: {uninstaller_path}")
        
        try:
            # subprocess.run([uninstaller_path, "--uninstall", "--channel=stable", "--system-level", "--verbose-logging", "--force-uninstall"], check=True)
            subprocess.run(["unistallChrome.bat", versionChrome], check=True)
            print("Google Chrome has been successfully uninstalled.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred during uninstallation: {e}")
        except FileNotFoundError:
            print("Uninstaller file not found.")
        except PermissionError:
            print("Permission error!")

    def install_chrome(self):        
        try:
            print("Installing ...")
            # subprocess.run([self.file_name], check=True)
            subprocess.run(["install_GoogleChrome.bat"], check=True)
            print("Installation completed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error during installation: {e}")
        except FileNotFoundError:
            print("Installation file not found.")
        except PermissionError:
            print("Permission error!")

def main():
    required_version = '126'
    path_to_chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

    try:
        version = getFileProperties(path_to_chrome).get("StringFileInfo").get("ProductVersion")
    except:
        version = None

    print(f'Current Chrome version: {version} ')

    if version and version[:3] == required_version:
        print('Google Chrome Browser Of The Correct Version!')
    else:
        print('Google Chrome Browser Incorrect Version!')
        print('The required version of Google Chrome will now be downloaded.')

        download_url = 'https://dw.uptodown.net/dwn/TG-cJBERbebTBCBZx9r6RqWVTS5J2OvN6W1_rek7D8xbPmgD_HUrfxHNRhnX-DfOGsSPbBwIOb-N9v_ESVo7mSU3y1dtExTTRHuxtlUTTnPCn0n_0XLHcHCdfUcHZhf2/pfFIhxXtcaJl5j8diW8gO38LfVG4BV9o6TCA1Ao69wYHxzX18RMJ4ZG_mEvmBkE79wuGfYaEFep_7V3yH2YeGJ4Wr-_5QbsovQu2XSVofsxykyUvzPLc_ooHpTiPtq5c/M3f2Vgb5xk2K7l4mowQwueuRPcgUUN9c45wS88X1jmvI7SOnoB0fTOsSpKHfhnOA13Xyn8gm3dQkqMFo7Gr40nDa0R7iQihEjMgM37IzsdQ=/google-chrome-126-0-6478-57.exe'
        file_name = 'google-chrome-126-0-6478-57.exe'

        downloader = ChromeDownloader(download_url, file_name)
        downloader.download_chrome()

        installer = ChromeInstaller(file_name, version[:3] if version else None)
        if version and version[:3] != required_version:
            installer.uninstall_chrome(version)

        installer.install_chrome()
        

if __name__ == "__main__":
    main()
