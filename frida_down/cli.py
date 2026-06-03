import argparse , logging ,sys
try:
    from . import frida_down
except:
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
      
      def download(self,version , platform  , arch = frida_down.ARCH.arm, ftype=""):
            
            if platform == frida_down.PLATFORM.android:
                  down = frida_down.android()
                  for android in down.get_latest_assets(version):
                        if android["arch"] == arch and ftype in android["asset_type"] :
                              log ( "downloading..." )
                              filename = down.download( version, android["filename"] )
                              log ( f"downloaded = {filename} " )
                              return filename
      
      def parse(self):
            
            self.arg = argparse.ArgumentParser(description="frida downloader cli")
            self.arg.add_argument("-v", "--verbose", type=str, default="", help="pass any value to turn on debugging log")
            self.arg.add_argument("-i", "--install", type=str,default= "", help="enter frida version to download")
            self.arg.add_argument("-a", "--arch", type=str,  choices = [p.value for p in frida_down.ARCH], help="enter frida architecture like arm, arm64 ,x86 ,x86_64")
            self.arg.add_argument("-p", "--platform", type=str,  choices = [p.value for p in frida_down.PLATFORM], help="choose platform like Android, Linux,Windows,macos,ios")
            self.arg.add_argument("-t", "--ftype", type=str , default = "frida-server" ,
                                  help="enter frida file type like 'frida-server','frida-gadget','frida-core-devkit' or anything ")
            args = self.arg.parse_args()
            return args
      
      def run(self):
            args = self.parse()
            args_dict = vars(args)
            
            if all(value is None for value in args_dict.values()):
                  self.arg.print_help()
            else:
                  if args.install and args.arch and args.platform :
                        if args.verbose : frida_down.logger.setLevel(logging.DEBUG)
                        if not self.download( args.install, platform = args.platform  , arch = args.arch ,ftype = args.ftype):
                              log("error in donwloading ")
                              sys.exit(1)
                        else:
                              sys.exit(0)
                  else:
                        self.arg.print_help()
                        sys.exit(1)


if __name__ == "__main__":
      #sys.argv = ["test", "-i", "15.0.1","-a", "arm",  "-p", "Android","-t","server"]
      main().run()