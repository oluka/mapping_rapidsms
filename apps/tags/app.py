#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


import rapidsms
from models import *


class App(rapidsms.App):
    def parse(self, msg):
        text = msg.text
        msg.tags = []

        # check the contents of this message for EVERY SINGLE
        # TAG that we know of. TODO: cache this for a little
        # while to avoid kicking the crap out of the database
        for tag in Tag.objects.all():
            if tag.match(text):

                # log and add this tag object to the message
                self.info("Tagged message with: %r" % (tag))
                msg.tags.append(tag)

                # remove this tag from the message string,
                # so other apps don't have to deal with it.
                # this allows the tag syntax to play nice
                # with other prefix-based apps
                text = tag.crop(text)

        # if we found and stripped tags out of the
        # message, update the object and log it
        if text != msg.text:
            self.info("Message is now: %s" % (text))
            msg.text = text

        # not so important, but make a note if
        # the message didn't contain tags. just
        # in case it _should_ have, we can at
        # least see that the app is working
        else:
            self.debug("No tags were found")
