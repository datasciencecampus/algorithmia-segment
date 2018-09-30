# Segmentation algo demo client

This directory contains some example code for interacting with the segmentation
algorithm service.

* `algo_io.py`: Convenience wrapper for moving data around.
* `example.py`: End to end working example.
* `visualise.py`: Visualise segmented images.


## Notes

### Random test images

Original images (c) from
[Mapillary Vistas Dataset](https://www.mapillary.com/dataset/vistas).

Get some random images:
```bash
for i in $(ls -alh |sort -R |awk '{print $9}' |head -3) ;do
  cp -v $i /home/phil/ungp/segment/client/test_images/
done
```

### Upload

Use `algo_io.py` to dump images.

```bash
export KEY=$(cat ~/.algorithmia/config |grep api_key |awk '{print $3}' \
  |sed 's/"//g')
export SERVER=$(cat ~/.algorithmia/config |grep api_server |awk '{print $3}' \
  |sed 's/"//g')
for i in $(ls test_images/) ;do
  python algo_io.py $KEY $SERVER test_images/$i data://.my/images/$i
done
```
