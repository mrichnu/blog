---
title: "Visual Studio Code on iPad with Tailscale and code-server"
tags: coding cloud
---

I've been learning [Elixir](https://elixir-lang.org/) recently, primarily as an excuse to
futz around and set up a development environment using my iPad Air (with "Smart
Keyboard Folio").

I can't believe this works as well as it does. 

<!-- more -->

The two technologies that are key to making this work are
[code-server](https://github.com/coder/code-server) and
[Tailscale](https://tailscale.com/). Essentially I just followed the [very
detailed instructions](https://tailscale.com/kb/1166/vscode-ipad/) provided by
the folks at Tailscale to set up `code-server` and Tailscale on an EC2 instance.
I tried to follow the [Coder
instructions](https://coder.com/docs/code-server/latest/guide#using-lets-encrypt-with-nginx)
for setting up HTTPS via Let's Encrypt + nginx, but ended up having to manually
edit my nginx config to get it to work (see below).

The truly amazing thing about doing it with Tailscale is that the EC2 instance
has no public IP and its security group has no inbound rules at all, but all I
have to do is just flip Tailscale to "On" on my iPad and I can immediately
connect to it. It feels like magic. 

Now that it's working, using VSCode on the iPad is pretty great, provided you do
the Progressive Web App installation trick of first loading it in Safari and
then adding it to your home screen.

## Tips

- To get [nginx to work with my Let's Encrypt SSL certificate](https://coder.com/docs/code-server/latest/guide#using-lets-encrypt-with-nginx), I had to manually set the path to the cert and key in my nginx config. E.g. add the below to your `/etc/nginx/sites-available/code-server`:
```
server {
  listen 443 ssl;
  server_name <Tailscale DNS hostname>;

  ssl_certificate       /var/lib/tailscale/certs/<Tailscale DNS hostname>.crt;
  ssl_certificate_key   /var/lib/tailscale/certs/<Tailscale DNS hostname>.key;

  <snip>
}
```

- The menus (File, Edit, etc.) did not work for me at all, either via touch or
  mouse, when in the default position along the top of the screen. However if I
  set the "Menu Bar Visibility" setting to "compact", then the menus are
  accessible via a "hamburger" at the top of the activity bar and work fine via
  touch and mouse.

- The software keyboard shortcut kept appearing at the bottom of the screen,
  even though I'm using a smart keyboard folio, until I turned off "Shortcuts"
  and "Predictive" in the Settings -> General -> Keyboards.