---
layout: post
title:  "Geolib - FastAPI"
date:   2021-05-09 13:05:11 +0200
categories: python geolib
---

### Warning

This is an 'advanced' topic. Don't complain if you end up with errors or even an invald geolib library!

### Geolib - FastAPI

If you want to use geolib in combination with FastAPI to offer downloadable files for your webservice you need to adjust a little bit of code. I am (as always) focusing on DStability for now. The current geolib code offers a DStabilityInputSerializer and a DStabilityInput**Zip**Serializer. If you then look at the serialize code in dstability_model.py you will see the the input expects a FilePath or DirectoryPath.

```python
def serialize(self, location: Union[FilePath, DirectoryPath]) -> io.BytesIO:
```

Most of the times you don't want to create physical files on the API end but you want to create them in memory. Fortunately the geolib developers have already written most of the code for this but you will have to adjust a little more. The way I did it (because in Python there are always a lot of other possibilities) was to add a new method to dstability_model.py;

```python
def serialize_buffer(self) -> io.BytesIO:
    serializer = DStabilityInputZipSerializer(ds=self.datastructure)
    return serializer.write(io.BytesIO())
```

This will give you a BytesIO object as a result which can then be returned as a downloadable file using the following FastAPI code;

```python
from fastapi.responses import Response

...

zip_buffer = dm.serialize_buffer()
resp = Response(
    zip_buffer.getvalue(),
    media_type="application/x-zip-compressed",
    headers={"Content-Disposition": f'attachment;filename="output.stix"'},
)
return resp
```

Now you are ready to create models using your own API and offer the final stix files as downloads!
