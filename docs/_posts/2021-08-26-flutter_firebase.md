---
layout: post
title:  "Flutter - Firebase"
date:   2021-08-26 18:48:49 +0200
categories: flutter
---

### Flutter and Firebase

#### Where the heck is this error coming from!

So there is one very annoying thing that is easily overlooked if you use Flutter and Firebase for web applications.. please note that if you add a package like 'firebase_storage' using for example ```firebase_storage: ^10.0.2``` remember to also add the required Javascript line in your index.html!

So add;

```<script src="https://www.gstatic.com/firebasejs/8.9.1/firebase-storage.js"></script>```

and now it is very likely that your error will be handled. Can take you hours if you don't remember this step!

Here is an example if you forget the js file with firebase_storage just as a reminder of how unhelpful the error message will be;

```
TypeError: appImpl.storage is not a function
    at Object.getStorageInstance (http://localhost:43651/packages/firebase_storage_web/src/interop/storage.dart.lib.js:739:65)
    at new firebase_storage_web.FirebaseStorageWeb.new (http://localhost:43651/packages/firebase_storage_web/src/reference_web.dart.lib.js:248:33)
    at firebase_storage_web.FirebaseStorageWeb._nullInstance.delegateFor (http://localhost:43651/packages/firebase_storage_web/src/reference_web.dart.lib.js:203:14)
    ...
```

Happy coding!

