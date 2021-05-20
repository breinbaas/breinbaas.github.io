---
layout: post
title:  "Flutter - Code Snippets"
date:   2021-05-20 12:24:00 +0200
categories: flutter codesnippets
---

### Using routes in flutter

If you want Flutter web applications to respond to arguments that are passed in the URL you can use the excellent [VRouter package](https://vrouter.dev/).

Using this package is easy, first setup the routes;

```
void main() {
  runApp(
      VRouter(
        routes: [
          VWidget(path:'/cpt/:cptId', widget:MyHomePage()),
          VWidget(path:'/', widget:MyHomePage()),          
        ]
      )
  );
}
```

Both paths are linked to the same widget.

Then use the VRouter object to retrieve the URL parameters;

```
class _MyHomePageState extends State<MyHomePage> {
  var _cptId;

  ...

  @override
  Widget build(BuildContext context) {
    _cptId = context.vRouter.pathParameters['cptId'];
    ...
  }
 ```

So now you can call the webapp like;
* http://yoururl/ will lead to the same widget but _cptId having the value null
* http://yoururl/cpt/1 to get _cptId with value '1'
 
