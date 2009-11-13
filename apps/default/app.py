#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


import rapidsms
from rapidsms.message import StatusCodes


class App(rapidsms.App):
    """When an incoming message is received, send a
       default response if case no other App responded."""

    def catch(self, msg):
        if not msg.responses:
            msg.respond(
                "Sorry, we didn't understand that message.",
                StatusCodes.GENERIC_ERROR)
            return True
