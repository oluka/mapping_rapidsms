#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from reporting.utils import extract_date, extract_weight
from rapidsms.contrib.apps.handlers import KeywordHandler
from rwanda.models import PregnantPerson, BirthReport


class PreBirthReportHandler(KeywordHandler):
    """
    """

    keyword = "born|birth"

    def must_register(self):
        self.respond("You must register before reporting a birth.")

    def handle(self, text):

        # abort if the user hasn't identified yet
        if self.msg.reporter is None:
            self.must_register()
            return True

        resp = "Thank you for reporting a birth"
        report = BirthReport()

        # extract and record the birth weight
        weight, text = extract_weight(text)
        if weight is not None:
            report.weight = weight
            resp += " at %.1f kg" % (weight)

        # extract and record the date of birth
        date, text = extract_date(text)
        if date is not None:
            report.date = date
            resp += " on %s" %\
                format(date, "%d/%m/%Y")

        # now that the weight and date have been
        # removed, assume that the rest is the
        # mother's unique code (todo: __search__)
        try:
            person = PregnantPerson.objects.get(
                code=text.strip())

        except PregnantPerson.DoesNotExist:
            self.respond("You must register the pregnancy before reporting a birth.")
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
