Title: Python Documentation and Vim
Date: 2014-01-08 17:24
Tags: python, documentation, vim
Slug: python-documentation-and-vim
Author: Matthew Rich
Summary: Getting Python help directly in vim.

Today at a [CodeMash](http://codemash.org) session I did a bit of pair
programming, which honestly I hadn't done in over 10 years and was a great
experience, and we were given to work on two programming exercises: the
canonical "FizzBuzz" game and then a more difficult [String Calculator
Kata](http://osherove.com/tdd-kata-1/). Because my partner did not have a
language environment he felt comfortable taking the lead with -- his primary
languages, oddly enough, were Bash, PowerShell, and a proprietary ERP language
-- I ended up controlling the keyboard and we finished the exercise using
Python. You can read our
[implementation](http://technivore.org/extra/string-calculator/StringCalculatorKata.py)
and [tests](http://technivore.org/extra/string-calculator/string_calculator_tests.py).

The String Calculator exercise is very straightforward until you get to the 7th
step and beyond, which involve handling a variable number of variable length
delimiters within a string. Obviously, this problem calls for regular
expressions and while I had intended to avoid that route since my partner was
not familiar with them, I decided it was much easier than the alternative
approach of multiple character-by-character passes through the input string.

Now, anyone who has used the Python standard library can tell you that the `re`
module is one of its oldest and cruftiest corners. The module clearly dates
back to the very early days of the language and, to my amateur eye at least,
there seem to be hidden and dangerous C-based things happening under the hood
that make the module relatively difficult to work with, or at least difficult
to remember the proper incantation to work with it effectively.

While working with my partner I referred to the Python documentation numerous
times, including to browse a list of methods on the built-in `str` type and the
interface for the `re.MatchObject` (because, Quick, how do you get a list of
all matched groups from a `MatchObject`?)

You can get (most of) this information directly from the `pydoc` command and
there is a [vim plugin](https://github.com/fs111/pydoc.vim) that integrates it
nicely. Save that plugin in `~/.vim/bundle` (You are using
[Pathogen](https://github.com/tpope/vim-pathogen), right?) and you now have the
`:Pydoc` and `:PydocSearch` commands to search the Python documentation
directly in vim. The first command allows you to read the docs for a
module/class/method/function if you know its name already (e.g. `:Pydoc
re.search`) while the latter searches through the documentation for matching
strings in module doc synopsis lines (that is, it's the same thing as `pydoc -k
<searchstring>`). 

The pydoc plugin also helpfully maps `<leader>pw` to do a Pydoc search on the
word under the curser and `<leader>pk` to do a Pydoc -k search. And, special
bonues due to the magic of how the `pydoc` command works, since all the plugin
does is call the actual `pydoc` command on your path, you can actually search
the documentation of your own modules since `pydoc` simply imports modules to
get their docs. And presumably, any code you are working on is importable, so
pydoc can search your own code as easily as it can the standard library.

As a final aside, one bit of documentation that actually *cannot* be displayed
by `pydoc` is for the `re.MatchObject` class, which was one of the things I
most wanted to look up. It turns out that that class is not importable, as it
is actually dynamically constructed at runtime by some bit of C black magic
when `re.match` is run. Therefore you still need to keep an offline copy of the
Python documentation handy to refer to outside of vim.
