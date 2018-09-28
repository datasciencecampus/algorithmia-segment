# Segmentation algo demo client


## Notes

### Random test images

Original images (c) from [Mapillary Vistas Dataset](https://www.mapillary.com/dataset/vistas).

```bash
for i in $(ls -alh |sort -R |awk '{print $9}' |head -100) ;do
  cp -v $i /home/phil/ungp/segment/client/test_images/
done
```

### Upload

Use `upload.py` to dump images.

```bash
export KEY=$(cat ~/.algorithmia/config |grep api_key |awk '{print $3}')
export SERVER=$(cat ~/.algorithmia/config |grep api_server |awk '{print $3}')

for i in $(ls test_images/) ;do
  python upload.py $KEY $SERVER test_images/$i data://.my/images/$i
done
```
