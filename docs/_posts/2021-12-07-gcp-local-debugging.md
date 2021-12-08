---
layout: post
title:  "GCP Cloud Functions, local debugging"
date:   2021-12-07 12:48:49 +0200
categories: python gcp
---

### What and why?

If you are writing serverless cloud functions for Google Cloud Platform (GCP) it is a tedious task to debug the function using the GCP. You have to upload the function code, restart the function and hope for the best.. repeat until done.. 

Fortunately this task can be optimized by using the [Function Framework](https://cloud.google.com/functions/docs/functions-framework)

I will focus on the [Python version](https://github.com/GoogleCloudPlatform/functions-framework-python) but Google supports plenty other languages.

### How to debug locally

Add ```functions_framework``` to the requirements file (or install it using pip)

```
functions-framework==3.*
```

Use the ```@functions_framework.http``` decorator on the main function you want to debug (note that this is for http triggered functions, the docs deal with other type of triggers).

```python
@functions_framework.http
def main(request):
    pass
```

Run the following command to start a local server using the framework;

```functions-framework-python.exe --target main --debug```

You now have the option to debug the function locally by using ```curl``` or the nice VSCode plugin [ThunderClient](https://www.thunderclient.io/)

![the output](https://github.com/breinbaas/breinbaas.github.io/blob/master/img/05.01.png?raw=true)
