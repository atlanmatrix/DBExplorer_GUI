# About FaaS

### Introduction
> Function as a service (FaaS) is a category of cloud computing services that provides a platform allowing customers to develop, run, and manage application functionalities without the complexity of building and maintaining the infrastructure typically associated with developing and launching an app. Building an application following this model is one way of achieving a "serverless" architecture, and is typically used when building microservices applications.   

*Sourced from Wiki: [https://en.wikipedia.org/wiki/Function_as_a_service](https://en.wikipedia.org/wiki/Function_as_a_service)

### Examples
#### I. Develop a web interface
```python
import time


def interface_name():
    print('hello world!')
    return time.time()
```
And now, you can visit this interface via
```
http://{host}:{port}/faas/<faas_name>
```
