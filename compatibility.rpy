init python:
    class CheckUpdateMods(Action, FieldEquality):
        identity_fields = [ "downloader" ]
        def __init__(self, downloader):
            self.downloader = downloader
        def __call__(self):
            return self.downloader.check_update()
    class StartInstall(Action, FieldEquality):
        identity_fields = [ "downloader" ]
        def __init__(self, downloader):
            self.downloader = downloader
        def __call__(self):
            return self.downloader.thread()
    class ModDownloader(object):
        import requests
        import json
        import os
        import zipfile
        import certifi
        import time

        url_json = "https://raw.githubusercontent.com/Vernulsi/compatibility/main/mods_versions.json"

        session = requests.Session()
        session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Вин64; x64) AppleWebKit/537.36 (KHTML, как Gecko) Chrome/109.0.0.0 Safari/537.36"})

        if not renpy.android:
            mods_path = os.path.join(config.gamedir, "mods")
        else:
            mods_path = os.path.join(config.savedir, "game", "mods")

        download_path = os.path.join(mods_path, "compatibility", "downloads")

        json_path = os.path.join(mods_path, "compatibility", "mods_versions.json")

        def ca_file(self):
            try:
                file = self.os.path.join(config.gamedir, self.certifi.where())
            except:
                    if renpy.android:
                        file = self.os.path.join(self.mods_path, "compatibility", "cacert.pem")

                        if not self.os.path.exists(file):
                            with open(file, "wb") as f:
                                try:
                                    f.write(renpy.file("python-packages/certifi/cacert.pem").read())
                                except:
                                    file = False
                    else:
                        file = False          
            return file
        
        def check_update(self):
            if persistent.mod_updater is None:
                persistent.mod_updater = {}
            persistent.mod_updater["ERROR"] = False
            data = self.session.get(self.url_json, stream=True, verify=self.ca_file()).json()
            with open(self.json_path, 'w') as f:
                self.json.dump(data, f)
            persistent.mod_updater["MODS"] = data
            persistent.mod_updater["TOGGLE_MODS"] = {}
            for key, _ in data.items():
                persistent.mod_updater["TOGGLE_MODS"][key] = False
            renpy.restart_interaction()
            return
        
        def download_mod(self, url):
            persistent.mod_updater["STATUS"] = "DOWNLOADING"
            if not self.os.path.exists(self.download_path):
                self.os.makedirs(self.download_path)
            file_name = self.os.path.join(self.download_path, url.split('/')[-1])
            file = self.session.get(url, stream=True, verify=self.ca_file())
            with open(file_name, "wb") as f:
                f.write(file.content)
            return file_name

        def delete_mod(self, name):
            persistent.mod_updater["STATUS"] = "DELETING"
            if not self.os.path.exists(name):
                return
            for obj in self.os.listdir(name):
                obj = self.os.path.join(name, obj)
                if self.os.path.isfile(obj):
                    self.os.remove(obj)
                if self.os.path.isdir(obj):
                    self.delete_mod(obj)
            self.os.rmdir(name)
            return

        def extract_mod(self, file_name, name):
            persistent.mod_updater["STATUS"] = "EXTRACTING"
            file_delete = [
                self.os.path.join(self.mods_path, name, ".gitattributes"), 
                self.os.path.join(self.mods_path, name, ".gitignore"),
                file_name
            ]
            path_new = self.os.path.join(self.mods_path, "new")
            with self.zipfile.ZipFile(file_name) as f:
                f.extractall(path_new)
            persistent.mod_updater["STATUS"] = "REPLACE"
            self.os.rename(self.os.path.join(path_new, name + "-main"), self.os.path.join(path_new,  name))
            self.delete_mod(self.os.path.join(self.mods_path, name))
            self.os.rename(self.os.path.join(path_new, name), self.os.path.join(self.mods_path,  name))
            self.delete_mod(path_new)
            for file in file_delete:
                try:
                    self.os.remove(file)
                except:
                    continue
            return

        def start_install(self):
            try:
                persistent.mod_updater["STATUS"] = "START"
                renpy.set_autoreload(False)
                persistent.mod_updater["DOWNLOADING_MOD"] = ''
                self.time.sleep(0.5)
                mods = persistent.mod_updater["TOGGLE_MODS"]
                for mod, value in mods.items():
                    if value:
                        persistent.mod_updater["DOWNLOADING_MOD"] = mod
                        url = "https://github.com/Vernulsi/%s/archive/refs/heads/main.zip" % mod
                        file_name = self.download_mod(url)
                        self.extract_mod(file_name, mod)
                persistent.mod_updater["DOWNLOADING_MOD"] = ''
                persistent.mod_updater["STATUS"] = "FINISH"
                return
            except:
                persistent.mod_updater["STATUS"] = "ERROR"
                return
        
        def thread(self):
            renpy.show_screen("download_screen")
            renpy.invoke_in_thread(self.start_install)

        def CheckUpdate(self):
            return CheckUpdateMods(self)

        def StartInstall(self):
            return StartInstall(self)

    md = ModDownloader()

    # def check_update():
    #     import requests
    #     import json
    #     import os
    #     if persistent.mod_updater is None:
    #         persistent.mod_updater = {}
    #     persistent.mod_updater["ERROR"] = False
    #     url = "https://raw.githubusercontent.com/Vernulsi/compatibility/main/mods_versions.json"
    #     r = requests.get(url, stream=True, verify=False).text
    #     mods = json.loads(r)
    #     with open(os.path.join(config.gamedir, "mods/compatibility/mods_versions.json"), 'w') as f:
    #         f.write(r)
    #     persistent.mod_updater["MODS"] = mods
    #     persistent.mod_updater["TOGGLE_MODS"] = {}
    #     for key, item in mods.items():
    #         persistent.mod_updater["TOGGLE_MODS"][key] = False
    #     return


    # def download_mod(url, saved_path="mods\\compatibility\\downloads"):
    #     import requests
    #     import os
    #     persistent.mod_updater["STATUS"] = "DOWNLOADING"
    #     dir_name = os.path.join(config.gamedir, saved_path)
    #     if not os.path.exists(dir_name):
    #         os.makedirs(dir_name)
    #     file_name = os.path.join(dir_name, url.split('/')[-1])
    #     file = requests.get(url, stream=True, verify=False)
    #     with open(file_name, "wb") as f:
    #         f.write(file.content)
    #     return file_name


    # def delete_mod(name):
    #     import os
    #     persistent.mod_updater["STATUS"] = "DELETING"
    #     if not os.path.exists(name):
    #         return
    #     for obj in os.listdir(name):
    #         obj = os.path.join(name, obj)
    #         if os.path.isfile(obj):
    #             os.remove(obj)
    #         if os.path.isdir(obj):
    #             delete_mod(obj)
    #     os.rmdir(name)
    #     return


    # def extract_mod(file_name, name):
    #     import os
    #     import zipfile
    #     persistent.mod_updater["STATUS"] = "EXTRACTING"
    #     file_delete = [
    #         os.path.join(config.gamedir, "mods", name, ".gitattributes"), 
    #         os.path.join(config.gamedir, "mods", name, ".gitignore"),
    #         file_name
    #     ]
    #     path = os.path.join(config.gamedir, "mods")
    #     path_new = os.path.join(path, "new")
    #     with zipfile.ZipFile(file_name) as f:
    #         f.extractall(path_new)
    #     os.rename(os.path.join(path_new, name + "-main"), os.path.join(path_new,  name))
    #     delete_mod(os.path.join(path, name))
    #     persistent.mod_updater["STATUS"] = "REPLACE"
    #     os.rename(os.path.join(path_new, name), os.path.join(path,  name))
    #     delete_mod(path_new)
    #     for file in file_delete:
    #         try:
    #             os.remove(file)
    #         except:
    #             continue
    #     return


    # def start_install():
    #     persistent.mod_updater["STATUS"] = "START"
    #     renpy.set_autoreload(False)
    #     import time
    #     persistent.mod_updater["DOWNLOADING_MOD"] = ''
    #     time.sleep(0.5)
    #     mods = persistent.mod_updater["TOGGLE_MODS"]
    #     for mod, value in mods.items():
    #         if value:
    #             persistent.mod_updater["DOWNLOADING_MOD"] = mod
    #             url = "https://github.com/Vernulsi/%s/archive/refs/heads/main.zip" % mod
    #             file_name = download_mod(url)
    #             extract_mod(file_name, mod)
    #     persistent.mod_updater["DOWNLOADING_MOD"] = ''
    #     persistent.mod_updater["STATUS"] = "FINISH"
    #     return


    def show_gametime(st, at):
        n = int(renpy.get_game_runtime())
        minutes, seconds = divmod(n, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        years, days = divmod(days, 365)
        img = Text("Проведёное в игре время: %0*d:%0*d:%0*d:%0*d:%0*d" % (2, years, 3, days, 2, hours, 2, minutes, 2, seconds))
        return img, None
init:
    image gametime = DynamicDisplayable(show_gametime)