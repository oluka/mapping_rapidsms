#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from reporting.utils import extract_weight, extract_length
from rapidsms.contrib.apps.handlers import KeywordHandler
from rwanda.models import PregnantPerson, BirthReport, ChildReport


class ChildReportHandler(KeywordHandler):
    """
    """

    keyword = "child\s+report|creport|crep"

    def must_register(self):
        self.respond("You must register before reporting.")

    def handle(self, text):

        # abort if the user hasn't identified yet
        if self.msg.reporter is None:
            self.must_register()
            return True

        resp = "Thank you for reporting"
        report = ChildReport()

        # extract and record the weight
        weight, text = extract_weight(text)
        if weight is not None:
            report.weight = weight
            resp += " at %.1f kilos" % (weight)

        # extract and record the muac
        muac, text = extract_length(text)
        if muac is not None:
            report.muac = muac
            resp += " with a MUAC of %.1f cm" % (muac)


        try:
            person = PregnantPerson.objects.get(
                code=text.strip())

        except PregnantPerson.DoesNotExist:
            self.respond("You must register the pregnancy before reporting.")
            return True


        try:
            birth_report = BirthReport.objects.get(
                person=person)

        except BirthReport.DoesNotExist:
            self.respond("You must report the birth before reporting.")
            return True


        report.person = person
        report.save()


        # save any tags extracted during
        # parse phase by the tagging app
        if hasattr(self.msg, "tags"):
            if len(self.msg.tags) > 0:
                for tag in self.msg.tags:
                    report.tags.add(tag)

                resp += " with indicators: %s" %\
                    (", ".join(map(unicode, self.msg.tags)))

        self.respond("%s." % resp)
