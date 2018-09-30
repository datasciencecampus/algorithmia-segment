# Segmentation algo demo
# ======================
# python3 example.py $KEY $SERVER test_images "data://.my/test_images" "data://.algo/nocturne/segment/temp" result

import Algorithmia
import sys
from algo_io import AlgoIO
api_key, api_endpoint, local_src_dir, remote_src_dir, remote_dst_dir, local_dst_dir = sys.argv[1:]

algo_io = AlgoIO(api_key, api_endpoint)
algo_client = Algorithmia.client(api_key, api_endpoint)

# upload contents of local_src_dir to algorithmia data:// location.
print("uploading images...")
algo_io.upload_dir(local_src_dir+"/*", remote_src_dir)

# invoke algo.
print("start image segmentation...")
algo = algo_client.algo('nocturne/segment/22d097cfdd0f837f081f83ce03a3ab79dd889612').set_options(timeout=600, stdout=True)
result = algo.pipe(dict(src=remote_src_dir, dst=remote_dst_dir))

print(result.result)
print(result.metadata)

# stash results locally.
print("downloading results...")
algo_io.download_dir(remote_dst_dir, local_dst_dir)

print("done.")
