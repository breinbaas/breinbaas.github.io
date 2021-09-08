---
layout: post
title:  "Flutter - Code Snippets"
date:   2021-05-02 15:53:00 +0200
categories: flutter codesnippets
---

### Call setState in initState of a widget

Sometimes you would like to instantiate a widget with data that is not available at initialization. In this case use the following code to watch for the variable and update the widget once the information is available;

```
void initState() {
    super.initState();

    WidgetsBinding.instance!.addPostFrameCallback((_) {
        _getCPTThumbnailURL(); // this is an async function taking some time
    });
}  
```

Complete sample code for a widget that needs to create an image based on an url that is only available through an async function.

```
class CPTCard extends StatefulWidget {
  const CPTCard({Key? key, required this.cpt}) : super(key: key);
  final CPT cpt;

  @override
  _CPTCardState createState() => _CPTCardState();
}

class _CPTCardState extends State<CPTCard> {
  String _cptThumbnailURL = '';

  @override
  void initState() {
    super.initState();

    WidgetsBinding.instance!.addPostFrameCallback((_) {
      _getCPTThumbnailURL();
    });
  }

  Future<String?> _getCPTThumbnailURL() async {
    String? url = await FileStorage.getCPThumbnailURL(widget.cpt.storageName);
    if (url != null) {
      setState(() {
        _cptThumbnailURL = url;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      color: Colors.white,
      margin: EdgeInsets.symmetric(vertical: 10.0, horizontal: 10.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.end,
        children: [
          ListTile(
            title: Text(widget.cpt.name),
            subtitle: Text(widget.cpt.date),
          ),
          _cptThumbnailURL == ''
              ? Image(
                  image: AssetImage('img/placeholder.jpg'),
                )
              : Image.network(_cptThumbnailURL),
        ],
      ),
    );
  }
}
```

### Python and Flutter base64 or how to pass an image from a Python API to Flutter without too much trouble

This was an annoying problem which took a lot of time to solve so remember,

Be sure to remove the annoying endlines if you use ```base64.encodebytes``` or else get ready for a world of pain (invalid character on the client side).

```python
result = {}
try:
    fig = some matplotlibfigure
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    result['image'] = base64.encodebytes(buf.read()).decode('utf-8').replace('\n','') # note this line!
    buf.close()
```

Now you can use this on the client side without having to worry about the endline characters with code like;

```
Map map = json.decode(response.body);
Uint8List imgdata = base64.decode(map['image']);
return Image.memory(imgdata);
```

and please note that Image comes from the flutter/widgets.dart package.

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

You can now call this function in Flutter using code like;

```
Future<http.Response> cloudFunction(){
  const String URL = 'the url to your function';
  return http.get(Uri.parse(URL));
}

final response = await cloudFunction();
print(response.body);
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
