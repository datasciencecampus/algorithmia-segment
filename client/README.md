# Segmentation algo demo client


## Notes

Random test images. Original images (c) from [Mapillary Vistas Dataset](https://www.mapillary.com/dataset/vistas).

```bash
for i in $(ls -alh |sort -R |awk '{print $9}' |head -100) ;do
  cp -v $i /home/phil/ungp/segment/client/test_images/
done
```
