init:
    
    python:
        def check_update():
            import requests
            import json
            import os
            if persistent.mod_updater is None:
                persistent.mod_updater = {}
            persistent.mod_updater["ERROR"] = False
            url = "https://raw.githubusercontent.com/Vernulsi/compatibility/main/mods_versions.json"
            r = requests.get(url, stream=True, verify=False).text
            mods = json.loads(r)
            with open(os.path.join(config.gamedir, "mods/compatibility/mods_versions.json"), 'w') as f:
                f.write(r)
            persistent.mod_updater["MODS"] = mods
            persistent.mod_updater["TOGGLE_MODS"] = {}
            for key, item in mods.items():
                persistent.mod_updater["TOGGLE_MODS"][key] = False
            return


        def download_mod(url, saved_path="mods\\compatibility\\downloads"):
            import requests
            import os
            persistent.mod_updater["STATUS"] = "DOWNLOADING"
            dir_name = os.path.join(config.gamedir, saved_path)
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            file_name = os.path.join(dir_name, url.split('/')[-1])
            file = requests.get(url, stream=True, verify=False)
            with open(file_name, "wb") as f:
                f.write(file.content)
            return file_name


        def delete_mod(name):
            import os
            persistent.mod_updater["STATUS"] = "DELETING"
            if not os.path.exists(name):
                return
            for obj in os.listdir(name):
                obj = os.path.join(name, obj)
                if os.path.isfile(obj):
                    os.remove(obj)
                if os.path.isdir(obj):
                    delete_mod(obj)
            os.rmdir(name)
            return


        def extract_mod(file_name, name):
            import os
            import zipfile
            persistent.mod_updater["STATUS"] = "EXTRACTING"
            file_delete = [
                os.path.join(config.gamedir, "mods", name, ".gitattributes"), 
                os.path.join(config.gamedir, "mods", name, ".gitignore"),
                file_name
            ]
            path = os.path.join(config.gamedir, "mods")
            path_new = os.path.join(path, "new")
            with zipfile.ZipFile(file_name) as f:
                f.extractall(path_new)
            os.rename(os.path.join(path_new, name + "-main"), os.path.join(path_new,  name))
            delete_mod(os.path.join(path, name))
            persistent.mod_updater["STATUS"] = "REPLACE"
            os.rename(os.path.join(path_new, name), os.path.join(path,  name))
            delete_mod(path_new)
            for file in file_delete:
                try:
                    os.remove(file)
                except:
                    continue
            return


        def start_install():
            persistent.mod_updater["STATUS"] = "START"
            renpy.set_autoreload(False)
            import time
            persistent.mod_updater["DOWNLOADING_MOD"] = ''
            time.sleep(0.5)
            mods = persistent.mod_updater["TOGGLE_MODS"]
            for mod, value in mods.items():
                if value:
                    persistent.mod_updater["DOWNLOADING_MOD"] = mod
                    url = "https://github.com/Vernulsi/%s/archive/refs/heads/main.zip" % mod
                    file_name = download_mod(url)
                    extract_mod(file_name, mod)
            persistent.mod_updater["DOWNLOADING_MOD"] = ''
            persistent.mod_updater["STATUS"] = "FINISH"
            return


        def show_gametime(st, at):
            n = int(renpy.get_game_runtime())
            minutes, seconds = divmod(n, 60)
            hours, minutes = divmod(minutes, 60)
            days, hours = divmod(hours, 24)
            years, days = divmod(days, 365)
            img = Text("Проведёное в игре время: %0*d:%0*d:%0*d:%0*d:%0*d" % (2, years, 3, days, 2, hours, 2, minutes, 2, seconds))
            return img, None
    image gametime = DynamicDisplayable(show_gametime)