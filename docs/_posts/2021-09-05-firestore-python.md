---
layout: post
title:  "Using Python and Firestore"
date:   2021-09-06 18:48:49 +0200
categories: python firestore
---

### Using Python and Firestore

At the moment of writing it can be quite a pain to find nice information about the usage of Python and Firebase storage so in this post I will write down code snippets to connect to the Firestore using Python.

#### Connecting to the storage location

```python
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

cred = credentials.Certificate('./gcpcredentials.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'leveelogic-1ce15.appspot.com'
})

bucket = storage.bucket()
```

The way to get the json file with your credentials is found in [this link](https://firebase.google.com/docs/admin/setup/) but in short these are the most important steps;

* In the Firebase console, open Settings > Service Accounts.
* Click Generate New Private Key, then confirm by clicking Generate Key.
* Securely store the JSON file containing the key.

#### Get all available files in the storage

```python
all_files = [b for b in bucket.list_blobs()]
```

which will give you information like;

```
[<Blob: your.appspot.com, cpts/00942275-5183-4ed5-8ecd-e987c0d06fc0.cpt, 1630327229077364>, <Blob: your.appspot.com, cpts/443f4bcb-1b6d-4308-b39d-1a54ec354257.cpt, 1630327200232994>, <Blob: your.appspot.com, cpts/fbeccb6a-9074-489d-a7f3-5ba1f54f2dbc.cpt, 1630069205354434>]
```

**note** ```bucket.list_blobs()``` will give you an iterator.

See also [this link](https://googleapis.dev/python/storage/latest/buckets.html#list_blobs)

