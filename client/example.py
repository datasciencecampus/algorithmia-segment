# Segmentation algo demo

import sys
from algo_io import AlgoIO
api_key, api_endpoint, src_dir, remote_dir, result_dir = sys.argv[1:]

algo_io = AlgoIO(api_key, api_endpoint)

# upload contents of src_dir to algorithmia data:// location.
algo_io.upload_dir(src_dir+"/*", remote_dir)

