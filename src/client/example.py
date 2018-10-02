################################################################################
# Segmentation algo. demo                                                      #
# ============================================================================ #
# export KEY=$(cat ~/.algorithmia/config \                                     #
#              |grep api_key |awk '{print $3}' |sed 's/"//g')                  #
# export SERVER=$(cat ~/.algorithmia/config \                                  #
#                 |grep api_server |awk '{print $3}' |sed 's/"//g')            #
# python3 example.py $KEY $SERVER test_images "data://.my/test_images" \       #
#   "data://.algo/nocturne/segment/temp" result                                #
#                                                                              #
# Phil Stubbings, ONS Data Science Campus.                                     #
################################################################################

ALGO="nocturne/segment/1397637817d54197cbe1d35a4eeb3c7fddc0f34a"

import Algorithmia
import sys
from algo_io import AlgoIO
api_key, api_endpoint, local_src_dir, remote_src_dir, remote_dst_dir, \
        local_dst_dir = sys.argv[1:]

algo_io = AlgoIO(api_key, api_endpoint)
algo_client = Algorithmia.client(api_key, api_endpoint)

# 1. upload contents of local_src_dir to algorithmia data:// location.
print("uploading images...")
algo_io.upload_dir(local_src_dir+"/*", remote_src_dir)

# 2. invoke algo.
print("start image segmentation...")
algo = algo_client.algo(ALGO).set_options(timeout=600, stdout=True)
result = algo.pipe(dict(src=remote_src_dir, dst=remote_dst_dir))

print(result.result)
print(result.metadata)

# 3. stash results locally.
print("downloading results...")
algo_io.download_dir(remote_dst_dir, local_dst_dir)

print("done.")
