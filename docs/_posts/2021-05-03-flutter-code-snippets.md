---
layout: post
title:  "Flutter - Code Snippets"
date:   2021-05-02 15:53:00 +0200
categories: flutter codesnippets
---

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