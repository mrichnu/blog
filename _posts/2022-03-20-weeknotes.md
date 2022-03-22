---
title: "Weeknotes: Week of March 20, 2022"
tags: weeknotes
---

Use `bc` for quick math in the terminal!

<!-- more -->

## BC

Do math in the terminal with `bc`! Just create a file that has your desired math
operations, create variables just like you expect with `<var> = <expression>`,
and output an expression by putting it on a line by itself.

Example `myfile.bc`:
```bc
total = 1 + 2 + 3
total * 2
quit
```

And now execute it:
```sh
$ bc -q myfile.bc
12
```

Or do even quicker math by piping to `bc`'s stdin:

```
$ echo "2 * 2" | bc
4
```

