from github import Github,Auth
from github.GithubException import UnknownObjectException
from urllib.request import urlretrieve
import logging,os,re,pathlib

"""
                  === frida downloader ===
                author : github.com/its_me_abi
                date   : 1/6/2026

"""


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
log = logger.info

class filename_validator:
     filename_pattern = re.compile(r"^(?!.*\.\.))[A-Za-z0-9._-]+$")

     @staticmethod
     def is_valid_name(filename) :
             return bool(filename_validator.filename_pattern.fullmatch(filename))


class PLATFORM :
        android = "Android"
        linux   = "Linux"
        windows = "Windows"
        macos   = "macos"
        ios     = "ios"
        
class ARCH:
        x86 = "x86"
        x64 = "x86_64"
        arm = "arm"
        arm64 = "arm64"
        
class frida:
        
        token = os.getenv("GITHUB_TOKEN")
        git  = Github( auth = Auth.Token( token )  , per_page = 100 ) if token else  Github(  per_page = 100 )
        latest = ""
        platform = None  # this should be set by child classes according to regex they want
        
        def __init__(self, download_folder_path ="./frida_data"):
                self.frida_repo = self.git.get_repo("frida/frida")
                self.download_folder_path = pathlib.Path(download_folder_path).resolve()

        def get_release(self, name ="" ):
                "returns asset object by name of release tag"
                if not isinstance(name, str):
                        raise ValueError("pleased provide string as repo name to frida github downloader ")
                
                if not name or  name == self.latest :
                        log (" no name passed as argument so fetching latest release" )
                        release = self.frida_repo.get_latest_release()
                else:
                        log ( "a custom release name specified" )
                        try:
                                release = self.frida_repo.get_release(name)
                                
                        except UnknownObjectException:
                                release = None
                        
                if release:
                         log( f"found release  name = {release.name } tag={release.tag_name } date={release.published_at} ")
                else:
                         log("release not found and returing empty release object")
                return release
        
        def download(self, release_name , asset_name , raise_error = False ):
                "download asset file from release name  + assetname "
                release = self.get_release( release_name )
                if release:
                        for asset in release.get_assets():
                                if asset.name == asset_name and filename_validator.is_valid_name(asset_name):
                                        full_localpath = self.download_folder_path / asset_name
                                        filepath, headers = urlretrieve(asset.browser_download_url, full_localpath, reporthook = self.progress)
                                        return filepath
                        if raise_error:
                                log ( "the provided  asset not found in github repo releases" )
                                raise ValueError("the provided  asset not found in github repo releases")
                if raise_error:
                        raise ValueError("the provided  release not found in github repo")

        def progress(self,block_num, block_size, total_size):
                downloaded = block_num * block_size
                info = f""" { round( downloaded / 1024 ) } KB / {round( total_size / 1024 ) } KB """
                log(f"  downloading data = {info}")
                
        def get_all_assets(self,release_name=""):
                "returns asset object "
                release = self.get_release(release_name)
                if release:
                        for asset in release.get_assets():
                                yield asset
                        
        def get_latest_assets(self):
                "returns assets as json "
                for asset in self.get_all_assets():
                        parsed_name_json = assetname_parser.parse(asset.name, self.platform)
                        if parsed_name_json:
                                yield parsed_name_json
                        
class assetname_parser: # borrowed and modified
        "to parse frida release asset names"
        
        platform = PLATFORM
        
        ANDROID_ASSET_RE = re.compile(
                r"^(?P<name>frida-(?:server|gadget|core-devkit))-"
                r"(?P<version>\d+\.\d+\.\d+)-"
                r"android-(?P<arch>arm64|arm|x86_64|x86)"  # i modified order so arm64 detected otherwise it will detect arm first
        )
        
        WINDOWS_ASSET_RE = re.compile(
                r"^(?P<name>frida-(?:server|gadget|core-devkit))-"
                r"(?P<version>\d+\.\d+\.\d+)-"
                r"windows-(?P<arch>arm64|arm|x86_64|x86)"
                # i modified order so arm64 detected otherwise it will detect arm first
        )
        
        LINUX_ASSET_RE = re.compile(
                r"^(?P<name>frida-(?:server|gadget|core-devkit))-"
                r"(?P<version>\d+\.\d+\.\d+)-"
                r"linux-(?P<arch>arm64|arm|x86_64|x86)"
                # i modified order so arm64 detected otherwise it will detect arm first
        )
        
        MAC_ASSET_RE = re.compile(
                r"^(?P<name>frida-(?:server|gadget|core-devkit))-"
                r"(?P<version>\d+\.\d+\.\d+)-"
                r"macos-(?P<arch>arm64|arm|x86_64|x86)"
                # i modified order so arm64 detected otherwise it will detect arm first
        )
        IOS_ASSET_RE = re.compile(
                r"^(?P<name>frida-(?:server|gadget|core-devkit))-"
                r"(?P<version>\d+\.\d+\.\d+)-"
                r"ios-(?P<arch>arm64|arm|x86_64|x86)"
                # i modified order so arm64 detected otherwise it will detect arm first
        )
        
        @staticmethod
        def parse( fullname , platform):
                """
                :param fullname: asset name of fridas github releases
                :param platform: assetname_parser.platform.android or , assetname_parser.platform.linux or
                                 assetname_parser.platform.windows
                :return: None or json
                """
                
                match = None
                if platform == assetname_parser.platform.android:
                        match = assetname_parser.ANDROID_ASSET_RE.match(fullname)
                        
                elif platform == assetname_parser.platform.windows:
                        match = assetname_parser.WINDOWS_ASSET_RE.match(fullname)
                        
                elif platform == assetname_parser.platform.linux:
                        match = assetname_parser.LINUX_ASSET_RE.match(fullname)
                        
                elif platform == assetname_parser.platform.macos:
                        match = assetname_parser.MAC_ASSET_RE.match(fullname)
                        
                elif platform == assetname_parser.platform.ios:
                        match = assetname_parser.IOS_ASSET_RE.match(fullname)
                        
                if not match:
                        return None
                
                return {
                        "asset_type": match.group("name"),
                        "version": match.group("version"),
                        "arch": match.group("arch"),
                        "filename": fullname,
                }
        
class android(frida):
        " for handling android related assetnames "
        platform = assetname_parser.platform.android
        ...


class linux(frida):
        " for handling android related assetnames "
        platform = assetname_parser.platform.linux
        ...


class windows(frida):
        " for handling android related assetnames "
        platform = assetname_parser.platform.windows
        ...

class macos(frida):
        " for handling android related assetnames "
        platform = assetname_parser.platform.macos
        ...

class ios(frida):
        " for handling android related assetnames "
        platform = assetname_parser.platform.ios
        ...

if __name__ == "__main__":
        ...
