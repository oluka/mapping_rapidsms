#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from reporting.utils import extract_date
from rapidsms.contrib.apps.handlers import KeywordHandler
from rwanda.models import PregnantPerson, PreBirthReport


class PreBirthReportHandler(KeywordHandler):
    """
    """

    keyword = "mrep"

    def must_register(self):
        self.respond("You must register before reporting.")

    def handle(self, text):

        # abort if the user hasn't identified yet
        if self.msg.reporter is None:
            self.must_register()
            return True

        try:
            person = PregnantPerson.objects.get(
                code=text.strip())

        except PregnantPerson.DoesNotExist:
            self.respond("You must register the pregnancy before reporting.")
            return True

        resp = "Thank you for reporting"
        report = PreBirthReport.objects.create(
            person=person)

        # save any tags extracted during
        # parse phase by the tagging app
        if hasattr(self.msg, "tags"):
            if len(self.msg.tags) > 0:
                for tag in self.msg.tags:
                    report.tags.add(tag)

                resp += " with indicators: %s" %\
                    (", ".join(map(unicode, self.msg.tags)))

        self.respond("%s." % resp)
