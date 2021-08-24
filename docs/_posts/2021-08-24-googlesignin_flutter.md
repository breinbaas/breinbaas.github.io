---
layout: post
title:  "Flutter - Google Sign In"
date:   2021-08-24 18:48:49 +0200
categories: flutter
---

### Flutter and Google login using Firebase

Logging in with a Google account into a Flutter app is easy.. except for some very likely errors. So here is the way I found after some hours of try catch error.. Note that this is meant for a **web** application so this is no iOS or Android manual.

First of all, there is a nice package which you can find using [pub dev](https://pub.dev/), just look for google sign in and follow their instructions.

You're already almost done but be sure to watch the following checklist;

* Did you create the OAuth2 credential ID?
* Did you add the metadata line with the client ID to the index.html file?
* Did you add ```<script src="https://apis.google.com/js/platform.js" async defer></script>``` to the index.html file?

Now make absolutely sure that you copy the right information from GCP to Firebase, your Client ID for a webapplication in GCP will have a Client ID and a Client secret, your Firebase authentication page will require a Web client ID and a Web client secret so here is the data flow..

![from gcp to firebase](https://github.com/breinbaas/breinbaas.github.io/blob/master/img/03.02.png?raw=true)

Ok, almost done then (refer to the google_sigin package instructions for details) but here is a tip and a way to handle a common error.

#### Tip

The OAuth2 client ID needs to be told what the authorized javascript origins are. In my case ```http://localhost``` and ```http://localhost:43651```. Now the port 43651 was just the last port I got when I started the Flutter project using Android Studio so it could be another random number. The problem is that this will change as soon as you do a fresh start and then your login process will fail because the new port is not part of the authorized javascript origins. To fix this you need to tell Flutter to start at a specific port which can be done in Android Studio using Run | Run | main.dart and choose Edit. Simply add ```--web-port=43651``` to the Additional run args field. Now Flutter will always use the same port. Note again that you should check your port number.

![android studio option](https://github.com/breinbaas/breinbaas.github.io/blob/master/img/03.01.png?raw=true)

#### Common error

if you get the following error;

```Sign in failed with error PlatformException(idpiframe_initialization_failed, Not a valid origin for the client...)``` 

then it can very likely be solved by clearing the cache of Chrome. If you did the previous steps right and you have made sure that the port is in agreement with the one given in the authorized javascript origins then you should be fine after clearing the cache.

Hope this saves you some time in setting up the Google authentication for Flutter web applications!
