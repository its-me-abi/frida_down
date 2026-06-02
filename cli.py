import argparse , logging ,sys
import frida_down

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
log = logger.info

class main:
        
        def toString(self, argobj):
                parsed = ["> frida_down"]
                for key, value in vars(argobj).items():
                        if value is None or value is False:
                                continue
                        if value is True:
                                parsed.append(f"--{key}")
                        else:
                                parsed.append(f"--{key} {value}")
                return " ".join(parsed)
        
        def download(self,version , platform = frida_down.PLATFORM.android , arch="arm", ftype=""):
                if platform == frida_down.PLATFORM.android:
                        down = frida_down.android()
                        for android in down.get_latest_assets(version):
                                if android["arch"] == arch and ftype in android["asset_type"] :
                                        log ( "downloading..." )
                                        filename = down.download( version, android["filename"] )
                                        log ( f"downloaded = {filename} " )
                                
        def run(self):
                
                self.arg = argparse.ArgumentParser(description="frida downloader cli")
                self.arg.add_argument("-i", "--install", type=str, help="enter frida version to download")
                self.arg.add_argument("-a", "--arch", type=str, help="enter frida architecture like arm, arm64 ,x86 ,x86_64")
                self.arg.add_argument("-p", "--platform", type=str,  default = "Android" , help="choose platform like Android, Linux,Windows,macos,ios")
                self.arg.add_argument("-t", "--ftype", type=str , default = "frida-server" ,
                                      help="enter frida file type like 'frida-server','frida-gadget','frida-core-devkit' or anything ")
                args = self.arg.parse_args()
                args_dict = vars(args)

                if all(value is None for value in args_dict.values()):
                        self.arg.print_help()
                else:
                        log( self.toString(args) )
                        if args.install and args.arch and args.platform :
                                self.download( args.install, platform = args.platform  , arch = args.arch ,ftype = args.ftype)
                        else:
                                log("please provide correct options")
                                self.arg.print_help()
                        
                
if __name__ == "__main__":
        #sys.argv = ["test", "-i", "17.10.1","-a", "arm",  "-p", "Android","-t","server"]
        main().run()