# Become /healthz

There's a not yet often talked about pattern coming from google, where in ops
you want to use a node's/container's/service's status or internal checks to
monitor what you are running.

This little package aims to provide a small Python framework to get you started.

It will host on your node two endpoints:

 * `/healthz`:
   * will return `HTTP 200` with the string "ok" if everything is considered fine by its own checks
   * will raise an `HTTP` error with a corresponding one line error message, if a local check fails
   * of course there's a check implemented where it errors when the processor gets overloaded
   * if this one is broken use the node's logs and the `/statusz` endpoint to figure out what's wrong
 * `/statusz`:
   * here you output info about whatever the stuff is for
   * as example we implemented: stats for cpu load and docker process metrics
   * you can track these in a logging engine like the ELK stack
