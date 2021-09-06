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
    'storageBucket': 'your.appspot.com'
})

bucket = storage.bucket()
```

The way to get the json file with your credentials is found in [this link](https://firebase.google.com/docs/admin/setup/) but in short these are the most important steps;

* In the Firebase console, open Settings > Service Accounts.
* Click Generate New Private Key, then confirm by clicking Generate Key.
* Securely store the JSON file containing the key.

#### Get all available files in the storage, access name and download to local file

```python
all_files = [b for b in bucket.list_blobs()] # careful with buckets that contain a lot of files!
for file in all_files:
    print(file.name)
    file.download_to_filename(file.name.split('/')[-1]) # requires the bucket to contain a subdirectory, adjust code otherwise
```

**note** ```bucket.list_blobs()``` will give you an iterator.

See also [this link](https://googleapis.dev/python/storage/latest/buckets.html#list_blobs)
