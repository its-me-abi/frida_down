from github import Github
from urllib.request import urlretrieve
import logging,os

"""
                  === frida donwloader ===
                author : github.com/its_me_abi
                date   : 1/6/2026

this modules is created because currently  adding frida agent to android device is a headache for me
we have to downlaod matching binary according to the frida we use for runnning in computer,
so we must go thorugh github assetpage and read all things and download it then using adb we have to inject it,
to make this process easy i created this python module.i have plan to create a gui for this that is my ultimeate aim

"""



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
log = logger.info

class frida:
        
        token = os.getenv("GITHUB_TOKEN")
        git  = Github( token , per_page = 100 )
        latest = ""
        
        def __init__(self , filepath = "./frida_server" ):
                self.frida_repo = self.git.get_repo("frida/frida")
                self.frida_path = filepath

        def get_release(self, name ="" ):
                "returns asset object by name of release tag"
                if not isinstance(name, str):
                        raise ValueError("pleased provide string as repo name to frida github downloader ")
                
                if not name or  name == self.latest :
                        log (" no name passed as argument so fetching latest release" )
                        release = self.frida_repo.get_latest_release()
                else:
                        log ( "a custom release name specified" )
                        release = self.frida_repo.get_release(name)
                if release:
                         log( f"found release  name = {release.name } tag={release.tag_name } date={release.published_at} ")
                else:
                         log("release not found and returing empty release object")
                return release
        
        def download(self, release_name , asset_name ):
                "download asset file from release name  + assetname "
                release = self.get_release( release_name )
                for asset in  release.get_assets ():
                        if asset.name == asset_name:
                               filepath , headers = urlretrieve( asset.browser_download_url , self.frida_path , reporthook = self.progress )
                               return filepath
                raise ValueError("the provided asset name is not found in releases and assets of github repo")

        def progress(self,block_num, block_size, total_size):
                downloaded = block_num * block_size
                log(f"   downloading data = {downloaded, "/", total_size}")
                
        def get_all_assets(self,release_name=""):
                release = self.get_release(release_name)
                for asset in release.get_assets():
                        yield asset

if __name__ == "__main__":
        log("testing started")
        downloader = frida()
        for asset in downloader.get_all_assets(downloader.latest):
                log(f"   asset name  == {asset.name}")
                if asset.name == "frida-server-17.10.0-android-arm64.xz":
                        log("downloading ...")
                        path = downloader.download(downloader.latest,asset.name)
                        if path:
                                log(f"file successfully downloaded = {path}")
                        
        log("testing ended")