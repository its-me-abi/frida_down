# 🔽 frida_down 


> A lightweight Frida binaries downloader ( unofficial )

[https://github.com/frida/frida](https://github.com/frida/frida/releases)
## 📋 Prerequisites

- Python 3.x
- pip (Python package manager)
- `GITHUB_TOKEN` environment variable set (optional ,without this 60 requests per hour per ip is only allowed because of ratelimit)

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/its-me-abi/frida_down.git
cd frida_down

# Install dependencies
pip install -r requirements.txt

# Set your GitHub token
export GITHUB_TOKEN=your_github_token_here
```

## 📖 API Usage

### Download Frida Binaries

```python
from frida_down import frida

# Initialize downloader
downloader = frida()

# Get latest release
release = downloader.get_release()

# Get specific release by tag name
release = downloader.get_release("17.10.0")

# Download a specific asset
filepath = downloader.download(downloader.latest, "frida-server-17.10.0-android-arm64.xz")

# List all assets in latest release
for asset in downloader.get_all_assets():
    print(asset.name)

# List all assets in specific release
for asset in downloader.get_all_assets("17.10.0"):
    print(asset.name)
```

### Parse Asset Names

```python
from frida_down import assetname_parser

# Parse Android asset names
asset_info = assetname_parser.parse(
    "frida-server-17.10.0-android-arm64.xz",
    assetname_parser.platform.android
)
# Returns: {
#     "asset_type": "frida-server",
#     "version": "17.10.0",
#     "arch": "arm64",
#     "filename": "frida-server-17.10.0-android-arm64.xz"
# }
```

### Android-Specific Helper

```python
from frida_down import android

# Initialize Android downloader
android_dl = android()

# Get all latest Android assets (parsed)
for asset_info in android_dl.get_latest_assets():
    print(asset_info)
    # Returns parsed asset information including version, architecture, and type
```

### Custom Download Path

```python
from frida_down import frida

# Specify custom download path
downloader = frida ( download_folder_path = "/path/to/save/frida_server" )

# Download will save to the specified path
filepath = downloader.download("", "frida-server-17.10.0-android-arm64.xz")
print( "file downloaded " , filepath )
```

## 📦 LICENCE
AGPL

