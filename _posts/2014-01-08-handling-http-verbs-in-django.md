---
title: A Pattern for Handling Multiple HTTP Verbs in Django
tags: coding django
---

An explicit, pythonic, easy-to-read way to handle multiple HTTP verbs in a single Django function-based view. No more ugly if/else blocks!

<!-- more -->

Recently I met [@odonnell004](https://twitter.com/odonnell004), a very
knowledgeable [Django developer](http://www.mavenrd.com) at the CodeMash
conference in Sandusky, Ohio, and over a beer he showed me a technique he
cooked up for dealing with multiple HTTP verbs in a single Django
function-based-view that I immediately fell in love with.

The most commonly seen way to handle either a GET or POST (or PUT or whatever)
request is to test the value of `request.method` in an if/else block, with the
logic for what to do for each case contained in the block itself. Forms are the
classic example (code below taken directly from the Django docs):

```python
def contact(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
            if form.is_valid(): # All validation rules pass
                # Process the data in form.cleaned_data
                # ...
                return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = ContactForm() # An unbound form

    return render(request, 'contact.html', {
        'form': form,
    })
```

I have been doing it this way pretty much since I started with Django three
years or so ago, and while it probably bothered me a bit at first I've long
since gotten used to this pattern and considered it the canonical way to do it.
But if you step back and look at it, it's ugly and confusing. In fact it's
bug-prone since your app could receive a PUT or other type of request and the
function above assumes that anything that isn't a POST must be a GET by
default.

What if, however, we wrote a function to handle each particular verb we want to
accept within a function-based view, and relied on a bit of clever
introspection to decide exactly which function to call?

```python        
from django.http import HttpResponse

def my_view(request):
    foo = do_something()

    def get():
        pass

    def post():
        pass

    def put():
        pass

    def delete():
        pass

    return resolve_http_method(request, [get, post, put, delete])

def resolve_http_method(request, methods):
    if isinstance(methods, types.ListType):
        methods = { func.__name__.lower() : func for func in methods }
    if request.method.lower() not in methods.keys():
        return HttpResponse(status=501)

    return methods[request.method.lower()]()
```
        
I love this. `resolve_http_method` simply gets passed the Django `HttpRequest`
instance and a list of functions whose names must be HTTP verbs. It then builds
a dict whose keys are the names of the functions and the values the functions
themselves. Then if it can't find the particular verb being handled in the
dict, it returns a 501 (Not Implemented) response. If it does find it, it
simply calls it.

But wait, what about the function's arguments you ask? Note that in the example
above, the `get`, `post`, etc. functions all have access to the variables
created in the parent `my_view` function's scope -- they are closures, and thus
have no need for extra arguments. 

I love how explicit this pattern is about what verbs can be handled, as well as
the elegant way it is implemented. And I especially love that it is a
function-based view pattern, since I find FBVs to be far more explicit,
obvious, and simple than CBVs and this is one more step in that direction.

Thanks again to Matt O'Donnell for the idea.
