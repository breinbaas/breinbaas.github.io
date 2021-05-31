---
layout: post
title:  "Qt and Deta"
date:   2021-05-31 12:48:49 +0200
categories: qt cpp deta
---

### Calling Deta API from Qt

In this article I will show you some code to call an (Deta) API from Qt and handle the json response. 

#### SSL

Qt needs to be installed with the OpenSSL modules to be fully functional. If you don't have it installed run the maintenance tool (on windows usually at ```C:\Qt\MaintenanceTool.exe```) and choose the OpenSSL installation under ```Developer and Designer Tools | OpenSSL x.x.xj Toolkit``` and choose the right version for your pc (probably 64-bit). 

![qt maintenance tool](https://github.com/breinbaas/breinbaas.github.io/blob/master/img/maintenancetool.png?raw=true)


Once this has been installed you need to copy the files from ```C:\Qt\Tools\OpenSSL\Win_x64\bin``` to your release and debug paths of the application that needs to make the https requests.



### Qt code for a Deta URL call and JSON response

```cpp

// SENDING PART
// somewhere in your class where you want to call the API
// *note* that DETA_URL is a reference to a QString with the URL
// so this will translate to something like
// https://mydeta.url/leveecodes?owner=ownername

// create URL string
const QString url_string = QString("%1/leveecodes?owner=%2").arg(DETA_URL, owner)

// create request
QNetworkRequest req = QNetworkRequest(QUrl(url_string));

// send request and requesthandler to call
m_networkaccesmanager.get(req);
connect(
    &m_networkaccesmanager, 
    &QNetworkAccessManager::finished, 
    this, 
    &DetaConnection::onLeveeCodesResult
);

...

// RECEIVING PART
// somewhere in your class in a slot that gets called from the sending part

// read data
QByteArray response_data = reply->readAll();
// convert to json
QJsonDocument json_response = QJsonDocument::fromJson(response_data);
QJsonObject json_object = json_response.object();

// in this sample code we expect a JSON object like {"leveecodes":[{"code":"A123","name":"Some Levee Name"}, ...]}
// get the array
QJsonArray json_array = json_object["leveecodes"].toArray();

// iterate over all items and show the content
foreach(const QJsonValue &value, json_array){
    QJsonObject obj = value.toObject();
    qDebug() << obj["code"].toString();
    qDebug() << obj["name"].toString();
}

// free the memory
reply->deleteLater();

// optionally disconnect the slot for the finished signal
disconnect(&m_networkaccesmanager, 0,0,0);
```

and voila..

![qt maintenance tool](https://github.com/breinbaas/breinbaas.github.io/blob/master/img/jsonrequestoutput.png?raw=true)

