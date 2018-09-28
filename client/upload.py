import Algorithmia
from glob import glob


class Uploader():

    def __init__(self, api_key=None, api_address=None):
        """Uploader convenience.
        
        Parameters
        ----------
        api_key: str, optional
            Algorithmia API key. Can get this from ~/.algorithmia/config
        api_address: str, optional
            Algorithmia endpoint. https://api.methods.officialstatistics.org
        """
        self.algo_client = Algorithmia.client(api_key, api_address)

    def upload(self, src, dst):
        """Upload a file to algorithmia hosted data:// location.
    
        Parameters
        ----------
        src: str
            Local (source) file. E.g., /tmp/lala.png
        dst: str
            Remote (destination) file. E.g., data://.my/images/lala.png

        Returns
        -------
        bool
            True if uploaded successfully, false otherwise.
        """
        # see https://docs.algorithmia.com/?python#upload-a-file
        self.algo_client.file(dst).putFile(src)


    def upload_dir(self, src_pat, dst_dir):
        """Upload collection of files to algorithma data:// location.
        
        Parameters
        ----------
        src_pat: str
            Local file(s). E.g., /tmp/*.png
        dst_dir: str
            Remote directory. Eg., data://.my/images

        Returns
        -------
        list of bool
            True if uploaded sucessfully, false otherwise.
        """
        return [self.upload(src) for src in glob(src_pat)]


if __name__ == '__main__':
    # single file.

    import sys
    api_key, api_endpoint, src, dst = sys.argv[1:]
    print("src={} dst={}".format(src, dst))
    Uploader(api_key, api_endpoint).upload(src, dst)
