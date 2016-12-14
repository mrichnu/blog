(Don't) Do The Right Thing
##########################

:date: 2013-05-31 16:30
:tags: python, best practices, django
:slug: dont-do-the-right-thing
:author: Matthew Rich
:summary: I tend to spend way too much time doing the "right" thing that I don't get down to just coding.

In other fields they call it "analysis paralysis" but I'm not sure if it has a
name in the world of software development. What I do know is that I tend to
spend way too much time trying to do the "right" thing and I don't get down to
just coding! 

The symptoms are easy enough to recognize when I'm starting a new project:
Spending far too long just thinking about the *project layout* before I even
create a single file. Doing "documentation driven development" to a fault
(which means when combined with problem #1, I've just spent an hour fiddling
with the layout of my documentation files) [#f1]_. Worrying about what CSS
framework to use. 

I really admire developers who can simply dive in and start writing code (test
first of course!) without worrying about this stuff, whether because they have
a workflow that they're comfortable with and can use consistently or simply
because they don't worry about it. I think that when I was a younger coder I
was one of those who could just sit down and mindlessly bang out PHP code just
as fast as anybody else -- and I think the change has two main causes:
experience, and Python. The former in that I'm very much more aware of the
consequences of blindly coding away without thinking of maintainability and
readability. This dovetails with the latter and the Python community's
emphasis on readability and the One Obvious Way To Do It. What I need to find
is a happy middle ground.

So that is the inaugural theme of this blog: embrace ``import this`` but don't
worry about always doing the right thing. Break stuff! Be messy! Just don't
stop building things!


.. [#f1] Note I'm *definitely* not saying DDD is bad. Just that I can
   occasionally go a little overboard with trying to foresee and document
   every detail before even begin designing the end product.
