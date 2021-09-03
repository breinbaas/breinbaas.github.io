---
layout: post
title:  "Flutter - Code Snippets"
date:   2021-05-02 15:53:00 +0200
categories: flutter codesnippets
---

### GCP pyhton functions and Flutter

To avoid CORS problems with GCP function and Flutter be sure to check [this link](https://cloud.google.com/functions/docs/writing/http#handling_cors_requests) and simply add the following code (well at least the interesting header part) to your GCP function;

```
def cors_enabled_function(request):
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)

    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    return ('Hello World!', 200, headers)
```

You can now call this function in Flutter using;

```
const String URL = 'the url to your function';
return http.get(Uri.parse(URL));
```

### Upload / load and read textfile 

Uses [file_picker](https://pub.dev/packages/file_picker) 

```
FilePickerResult? result = await FilePicker.platform.pickFiles();
if(result != null){
    PlatformFile file = result.files.first;
    _cpt = CPT.fromPlatformFile(file);
}

...


String fileContent = utf8.decode(List.from(file.bytes!));
List<String> lines = fileContent.split('\n');
for (var i=0; i<lines.length; i++) {
    print(lines[i]);
}
```
### 'list comprehension'

A fast way to convert a list of types to other types (bit like list comprehension);

```
var fargs = [for(var j = 0; j < args.length; j++) double.parse(args[j])];
```

### iterate over dictionary

```
bool hasColumnVoid = false;
columnVoids.forEach((key, value) {
    hasColumnVoid |= fargs[key] == value;
});
```
