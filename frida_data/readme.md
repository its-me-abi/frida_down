### about

this folder is used as default download folder.  
if you want to change it and you want to download frida asset files to different folder then.  
use  following code on top of it,  
please note that this folder must already exist otherwise an error will be raised

```
from frida_down import frida

# Specify custom download path
downloader = frida ( download_folder_path = "/path/to/save/frida_server" )

# Download will save to the specified path
filepath = downloader.download("", "frida-server-17.10.0-android-arm64.xz")
print( "file downloaded " , filepath )

```
