import unittest
import frida_down


class Test_allplatforms(unittest.TestCase):
    """
    test all platforms asset binaries by calling get_latest_assets function
    """
    
    def setUp(self):
            ...
            
    def test_android(self):
            result = None
            for x in frida_down.android().get_latest_assets():
                    result = x
                    print(x)
            self.assertIsNotNone(result)
    
    def test_linux(self):
            result = None
            for x in frida_down.linux().get_latest_assets():
                    result = x
                    print(x)
            self.assertIsNotNone(result)
            
    def test_windows(self):
            result = None
            for x in frida_down.windows().get_latest_assets():
                    result = x
                    print(x)
            self.assertIsNotNone(result)
            
    def test_macos(self):
            result = None
            for x in frida_down.macos().get_latest_assets():
                    result = x
                    print(x)
            self.assertIsNotNone(result)
            
    def test_ios(self):
            result = None
            for x in frida_down.ios().get_latest_assets():
                    result = x
                    print(x)
            self.assertIsNotNone(result)
          
          

class Test_Downloading(unittest.TestCase):
    """Tests for Frida asset downloading."""

    def test_download_latest_asset(self):
        downloader = frida_down.frida()
        asset_found = None
        for  asset in downloader.get_all_assets(downloader.latest):
                asset_found = asset

        self.assertIsNotNone( asset_found,"Expected any asset but nothing was not found in the latest release.")

        path = downloader.download(downloader.latest, asset_found.name)
        self.assertIsNotNone( path,f"failed to download asset '{asset_found.name}'")
        
                
if __name__ == "__main__":
    unittest.main()