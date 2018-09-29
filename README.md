# Image segmentation algo

[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](http://www.repostatus.org/badges/latest/wip.svg)](http://www.repostatus.org/#wip)

> Part of trees/ungp.



## pspnet 

Note that `src/pspnet` is a clone of [mitmul/chainer-pspnet](https://github.com/mitmul/chainer-pspnet).
Algorithmia build seems not to support git submodules (tried to update `bin/build` with no luck..).
As such, work-around is to just clone the repo as-is.


## Running

Credentials

```
export API_KEY="xxx"
export VERSION=$(git rev-parse HEAD)
```

curl

```
curl -X POST -d '{"images":["x"]}' -H 'Content-Type: text/json' \
     -H 'Authorization: Simple $API_KEY' \
  https://api.methods.officialstatistics.org/v1/algo/nocturne/segment/$VERSION

```

algo client

```
algo run nocturne/segment/$(git rev-parse HEAD) -d \
  '{"src": "data://.my/images", "dst": "data://.my/out"}'
```


## Testing

```
make test
```
