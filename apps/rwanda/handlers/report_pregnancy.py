#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from reporters.models import Reporter
from reporting.utils import extract_date
from rapidsms.contrib.apps.handlers import KeywordHandler
from rwanda.models import PregnantPerson, PregnancyReport


class ReportPregnancyHandler(KeywordHandler):
    """
    """

    keyword = r"pregnancy|pregnant|preg"

    def help(self):
        self.respond("To register a pregnancy, send <PREG> <MOTHER-ID> <LAST-MENSES> <OBSERVATIONS>")

    def must_register(self):
        self.respond("You must register before reporting a pregnancy.")

    def handle(self, text):

        # abort if the user hasn't identified yet
        if self.msg.reporter is None:
            self.must_register()
            return True

        # create a new person linked back to the reporter
        # and their 
        person = PregnantPerson.objects.create()
        report = PregnancyReport.objects.create(
            person=person)

        person.reporters.add(self.msg.reporter)

        resp = "Thank you for reporting a pregnancy"
        follow_resp = "Pregnancy reported by %s (%s)" %\
            (self.msg.reporter, self.msg.reporter.connection.identity)

        # explicitly link the reporter's location,
        # in case they move during the pregnancy
        loc = self.msg.reporter.location
        if loc is not None:
            person.locations.add(loc)
            follow_resp += " at %s" % (loc)

        # extract the last menses date, if possible
        last_menses, text = extract_date(text)
        if last_menses is not None:
            person.last_menses = last_menses
            person.save()

        # save any tags extracted during
        # parse phase by the tagging app
        if hasattr(self.msg, "tags"):
            if len(self.msg.tags) > 0:
                for tag in self.msg.tags:
                    report.tags.add(tag)

                suffix = " with indicators: %s" %\
                    (", ".join(map(unicode, self.msg.tags)))

                resp += suffix
                follow_resp += suffix

        # assume that the remainder of the text is the
        # woman's national id (rwanda-specific; sorry)
        person.code = text.strip()
        person.save()

        self.respond("%s." % resp)
        
        follower = self.msg.reporter.followers.all()
