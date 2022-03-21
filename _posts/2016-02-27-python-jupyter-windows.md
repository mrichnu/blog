---
title: Three Ways To Run Jupyter In Windows
tags: python jupyter windows
---
Let's look at a few different ways to run jupyter notebooks in Windows.

<!-- more -->

## The "Pure Python" Way
Make your way over to [python.org](https://www.python.org/), download and install
the latest version ([3.5.1](https://www.python.org/downloads/release/python-351/)
as of this writing) and make sure that wherever you install it, the directory 
containing `python.exe` is in your system `PATH` environment variable. I like to
install it in the root of my `C:` drive, e.g. `C:\Python35`, so my `PATH` contains
that directory.

Once that's installed, you'll want to create a [virtual environment](https://docs.python.org/3/library/venv.html),
a lightweight, disposable, isolated python installation where you can experiment
and install 3rd party libraries without affecting your "main" installation. To do
this, open up a Powershell window, and enter the following commands (where "myenv"
is the name of the virtualenv we're going to create, you can use any name you like
for this):

```
PS C:\> python -m venv myenv
PS C:\> myenv\Scripts\activate
```

Then, let's install jupyter and start up a notebook:

```
PS C:\> pip install jupyter
PS C:\> jupyter notebook
```

Incidentally, if you get a warning about upgrading pip, make sure to use the
following incantation to upgrade (to prevent an issue on windows where pip
is unable to upgrade its own executable in-place):

```
PS C:\> python -m pip install --upgrade pip
```

**Advantages**: Uses "pure" python, official tools, and no external dependencies.
Well supported, with plenty of online documentation and support communities.

**Disadvantages**:  While many popular data analysis or scientific python libraries 
can be installed by `pip` on windows (including [Pandas](http://www.scipy.org) and
[Matplotlib](http://www.scipy.org)), some (for example [SciPy](http://www.scipy.org))
require a C compiler and the presence of 3rd party C libraries on the system
which are difficult to install on Windows.

**Who is it for?** Python users comfortable with the command line and the tools
that ship with Python itself.

## The Python Distributions

Because of the difficulty mentioned above in getting packages like SciPy installed
on Windows, a few commercial entities have put together pre-packaged Python
"distributions" that contain most, if not all, of the commonly used libraries
for data analysis and/or scientific computing.

[Anaconda](http://continuum.io/downloads) is an excellent option for this. Download
their Python 3.5 installer for Windows, run it, and in your Start menu you'll have
a bunch of neat new tools, including an entry for Jupyter Notebook. Click to start
it up and it'll launch in the background and open up your browser to the notebook
console. It doesn't get any easier than that.

**Advantages**: Simplest, fastest way to get started and it comes with probably
everything you need for your scientific computing projects. And anything it 
doesn't ship with you can still instalAl via its built in `conda` package manager.

**Disadvantages**:  No virtualenv support, although the `conda` package manager
provides very similar functionality with the `conda create` command. Relies on a
commercial 3rd party for support.

**Who is it for?** People who want the quickest, easiest way to get Jupyter
notebook up and running (IE, most people).

## Docker

[Docker](https://www.docker.com/) is a platform for running software in "containers",
or self-contained, isolated processes. While it may sound similar in concept to
python virtual environments, Docker containers are an entirely different kind of 
technology offering vast flexibility and power. Don't let the flexibility and power
and confusing terminology put you off though -- Docker can be easy to get up and 
running on your PC and has some advantages of its own with respect to Python and
Jupyter.

To get started on Windows, download the [Docker Toolbox](https://www.docker.com/products/docker-toolbox),
which contains the tools you need to get up and running. Run the installer and make
sure the checkbox to install Virtualbox is checked if you don't already have 
Virtualbox or another virtualization platform (like VMWare Workstation) installed.

Once installed, you'll have a "Docker Quickstart Terminal" shortcut in your Start 
Menu. Double click that shortcut and it will create your first Docker engine for you
and set up everything you need automatically. Once you see a prompt in the terminal,
you can use the `docker run` command to run Docker "images", which you can think
of as pre-packaged bundles of software that will be automatically downloaded from
the [Docker Hub](https://hub.docker.com/) when you run them. There are many images
on Docker Hub that offer Jupyter, including the official [Jupyter Notebook](https://hub.docker.com/r/jupyter/notebook/)
image, and [Anaconda](https://hub.docker.com/r/continuumio/anaconda/) itself if you
want the full SciPy stack.

To run just the official Jupyter Notebook image in your Docker engine, type the
following into the Docker Quickstart Terminal:

```
$ docker run --rm -it -p 8888:8888 -v "$(pwd):/notebooks" jupyter/notebook
```

After all the image's "layers" are downloaded, it will start up. Make a note of the 
IP address listed in the terminal (mine is usually `192.168.99.100`), and point your
browser at that IP address, port 8888 (e.g. [http://192.168.99.100:8888](http://192.168.99.100:8888)) and you'll see the familiar Jupyter console, with both
Python 2 and Python 3 kernels available.

**Advantages**: Use the flexibility and power of Docker! Honestly one of my favorite
things about Docker is thinking of it as an open software distribution platform for
things like the SciPy stack that are hard to install.

**Disadvantages**: Grapple with the flexibility and power of Docker! There are quite
a few "gotchas" to be aware of when dealing with Docker, such as immutable
containers, data volumes, arcane commands, and rapidly developing, occasionally
buggy tooling.

**Who is it for?** Users who either already are comfortable with Docker or are
willing to dive into bleeding edge technology :)

## Conclusion

For the work I do, where Jupyter running Python 3 notebooks with Pandas and 
[SqlAlchemy](http://www.sqlalchemy.org/) is enough, I prefer to use the "pure
Python" method, because the tools are well understood and well supported, and a
tremendous amount of work has been done by the Python community to make the tools
work well on Windows. And if I ever am working on a large enough data set that my
laptop alone can't handle it, using Docker to run my notebooks on cloud providers'
platforms is wonderfully easy.

That said, if you are coming into this just looking to use Python to tackle a data
analysis or scientific computing problem and want to get started with minimal fuss,
a distribution like [Anaconda](http://continuum.io/downloads) is without a doubt the
fastest way to get started.
