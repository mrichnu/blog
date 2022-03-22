---
title: "Weeknotes: Week of January 2, 2022"
tags: weeknotes
---

AWS CLI tools, vim tips, and a new blogging setup!

<!-- more -->

## aws-sso-cli

[https://github.com/synfinatic/aws-sso-cli](https://github.com/synfinatic/aws-sso-cli).
Provides some convenience commands for working with AWS SSO roles at the command line.

Notes:
- installed deb into my WSL ubuntu environment via `dpkg`; possible to just download binary b/c it's written in Go.
- Sets itself up via wizard by running `aws-sso` with no arguments after installation.
- "Open" `UrlAction` doesn't work in WSL because no `xdg-open` command; use the "Print" action instead and paste into browser.
- Use `aws-sso cache` to force reload of list of roles. It'll have you open browser and confirm.
- `aws-sso list` to list roles available
- `eval $(aws-sso eval -A <account id> -R <role name>)` to export AWS-related env vars in bash. Really handy!

## aws-shell

Not compatible with awscli v2! Instead just upgrade to the latest awscli v2 version for a nice auto-complete
experience (see below)

## awscli autocompletion

If you have latest awscli installed, run `aws --cli-auto-prompt` to enter an autocomplete mode.
Documentation: [https://docs.aws.amazon.com/cli/latest/userguide/cli-usage-parameters-prompting.html](https://docs.aws.amazon.com/cli/latest/userguide/cli-usage-parameters-prompting.html)

Avoid having to type `--cli-auto-prompt` every time by exporting `AWS_CLI_AUTO_PROMPT=on` and then just run `aws`
(and hit enter) and you'll end up in autoprompt mode!

## Find unique records in vim

You don't have to use the shell! Vim has a built-in `:sort u` that will sort all lines in a file and remote duplicates. Run `:help :sort` for details.

## Played around with Jekyll and Netlify!

Preparing to re-launch my blog with Jekyll, I ran through the [Jekyll tutorial](https://jekyllrb.com/docs/step-by-step/01-setup/) and published the [result to Netlify](https://thirsty-austin-9f5133.netlify.app/)!
Notes along the way:

- I used Docker to run Jekyll locally rather than try to install it. Unfortunately when running `jekyll serve` in a Docker container inside WSL, the port wasn't accessible from a Windows browser. So instead I just ran the Docker container from Powershell.
- Auto-regeneration doesn't seem to work in Windows however; have to manually restart the container to see changes. And it's sloooow.
- The `sassc` gem version 2.4.0 hangs on installation. A random StackOverflow post pointed me at installing 2.1.0 instead in my `Gemfile.lock` and that solved it. But that kind of thing shouldn't be necessary.
- Netlify is in fact totally amazing. No futzing with build configuration or even GitHub Actions; just point it at your GitHub repo (can even be a private repo) and as long as the right bits are in place (namely the `Gemfile`) it immediately creates a new site and does all the Jekyll build stuff automatically. It. Just. Works.  