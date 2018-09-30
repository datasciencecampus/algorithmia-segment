# Algorithmia PSPNet image segmentation

[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](http://www.repostatus.org/badges/latest/wip.svg)](http://www.repostatus.org/#wip)

> Part of trees/ungp.

This is a street-level image segmentation algorithm hosted on the
methods.officialstatistics.org Algorithmia platform.

The implementation (currently) makes use of a
[Chainer implementation](https://github.com/datasciencecampus/chainer-pspnet) of a
[Pyramid Scene Parsing Network (PSPNet)](https://hszhao.github.io/projects/pspnet/)
which has been included as a git submodule. 


## Demo

Please see example code in `client`.



## General form

The algorithm accepts 2 arguments: `src` and `dst`.

Where:

* `src`: The (Algorithmia hosted) location of `.jpg` images you wish to segment. For example: `data://.my/input_images`
* `dst`: The (Algorithmia hosted) location to store the segmentation results. For example: `data://.algo/nocturne/segment/temp`.

Note that it is good practice to store results in
`data://.algo/:user/:algo/temp`since these files will be automatically deleted
by the algorithmia platform once per day.

After running, check the `dst` directory for resulint .bmp images.

The .bmp images describe the predicted segments for each pixel in the scene.
Each pixel value will range between `0` and `255` and map to a specific label.
The current implementation makes use of a network pre-trained on the Cityscapes
dataset, and as such, the labels are as follows:

1. road
2. sidewalk
3. building
4. wall
5. fence
6. pole
7. traffic light
8. traffic sign
9. vegetation
10. terrain
11. sky
12. person
13. rider
14. car
15. truck
16. bus
17. train
18. motorcycle
19. bicycle
20. unknown/other.

Please see the `client/visualise.py` code for a complete post-processing demo.


## Running

See `client/exmaple.py` for an end-to-end Python based demo.

Else, the webservice can be invoked as follows:


Set credentials

```
export API_KEY="xxx"
export VERSION=$(git rev-parse HEAD)
```

Using `curl`:

```
curl -X POST -d '{"images":["x"]}' -H 'Content-Type: text/json' \
     -H 'Authorization: Simple $API_KEY' \
  https://api.methods.officialstatistics.org/v1/algo/nocturne/segment/$VERSION

```

Using the Algorithmia `algo` client:

```
algo run nocturne/segment/$(git rev-parse HEAD) -d \
  '{"src": "data://.my/images", "dst": "data://.my/out"}'
```


## Testing

```
make test
```

## Maintainer

* [Phil Stubbings](https://github.com/phil8192) @[DataSciCampus](https://datasciencecampus.github.io/).
