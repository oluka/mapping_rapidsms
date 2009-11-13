#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from rapidsms.tests.scripted import TestScript
from rapidsms.contrib.apps.handlers.app import App as HandlerApp
from reporters.app import App as ReportersApp
from reporters.models import Reporter
from tags.app import App as TagsApp
from app import App


class TestApp (TestScript):
    fixtures = ("rwanda_test_locations", "rwanda_tags")
    apps = (HandlerApp, ReportersApp, TagsApp, App)

    testRegistration = """
        0 > JOIN
        0 < To register, send JOIN <NATIONAL-ID>


        1 > JOIN 1111
        1 < Thank you for registering.

        # broken by the AM tag
        #1 > WHO AM I?
        #1 < I think you are 1111.


        2 > JOIN 2222 rw
        2 < Thank you for registering in Kinyarwandan.

        2 > WHOAMI
        2 < I think you are 2222.


        3 > JOIN 3333 1020
        3 < Thank you for registering at Example Health Facility.

        3 > whoam i
        3 < I think you are 3333.


        4 > JOIN 4444 rw 1020
        4 < Thank you for registering in Kinyarwandan at Example Health Facility.

        4 > whoami?
        4 < I think you are 4444.


        5 > JOIN 5555 1020 rw
        5 < Thank you for registering in Kinyarwandan at Example Health Facility.
    """

#    def testRegistration(self):
#        def r(alias):
#            return Reporter.objects.get(
#                alias=alias)
#    
#        self.assertTrue(r("1111").count() == 1)
#        self.assertTrue(r("2222").language.code == "kw")
#        self.assertTrue(r("3333").location.code == "1020")
#        self.assertTrue(r("4444").language.code == "kw")
#        self.assertTrue(r("4444").location.code == "1020")

    testReportPregnancy = """
        1 > PREG 1234 01/01/2009
        1 < You must register before reporting a pregnancy.

        1 > JOIN 1111
        1 < Thank you for registering.

        1 > PREG 1234 01/01/2009
        1 < Thank you for reporting a pregnancy.

        2 > PREG
        2 < To register a pregnancy, send <PREG> <MOTHER-ID> <LAST-MENSES> <OBSERVATIONS>
    """

    testPreBirthReport = """
        1 > MREP 1234 HE
        1 < You must register before reporting.

        1 > JOIN 1111
        1 < Thank you for registering.

        1 > MREP 1234 HE
        1 < You must register the pregnancy before reporting.

        1 > PREG 1234
        1 < Thank you for reporting a pregnancy.

        1 > MREP 1234 HE
        1 > Thank you for reporting.
    """

    testBirthReport = """
        1 > BORN 1234 HE BO 5kg
        1 < You must register before reporting a birth.

        1 > JOIN 1111
        1 < Thank you for registering.

        1 > BORN 1234 HE BO 5kg
        1 < You must register the pregnancy before reporting a birth.

        1 > PREG 1234
        1 < Thank you for reporting a pregnancy.

        1 > MREP 1234 HE BO 5kg
        1 > Thank you for reporting a birth at 5 kg with indicators: Healthy, Male.
    """

    testChildReport = """
        1 > CREP 1234 HE
        1 < You must register before reporting.

        1 > JOIN 1111
        1 < Thank you for registering.

        1 > CREP 1234 HE
        1 < You must register the pregnancy before reporting.

        1 > PREG 1234
        1 < Thank you for reporting a pregnancy.

        1 > CREP 1234 HE
        1 < You must report the birth before reporting.

        1 > BORN 1234 HE RO 4kg
        1 < Thank you for reporting a birth at 4.0 kg with indicators: Healthy, Female.

        1 > CREP 1234 RH
        1 < Thank you for reporting with indicators: Neonatal child death.
    """

    testFollow = """
        1 > JOIN 1111
        1 < Thank you for registering.

        2 > JOIN 2222 1020
        2 < Thank you for registering at Example Health Facility.

        3 > JOIN 3333
        3 < Thank you for registering.

        1 > FOLLOW 2222 3333
        1 < You are now following: 2222, 3333

        2 > PREG 1234 01/01/2009
        2 < Thank you for reporting a pregnancy.
        1 < Pregnancy reported by 2222 (2) at Example Health Facility

        3 > PREG 5678 HE
        3 < Thank you for reporting a pregnancy.
        1 < Pregnancy reported by 3333 (3) with indicators: Healthy.
    """

    testDocumentation = """
        1 > JOIN 3201704 rw 1020
        1 < Thank you for registering in Kinyarwandan at Example Health Facility.

        1 > PREG 47293948 19.10.2009 ba ku
        1 < Thank you for reporting a pregnancy with indicators: Rapid breathing, Vomitting.

        1 > MREP 47293948 so in
        1 < Thank you for reporting with indicators: Coughing, Pneumonia.

        1 > BORN 47293948 20.04.2009 bo 2.4kg
        1 < Thank you for reporting a birth at 2.4 kg on 20/04/2009 with indicators: Male.

        1 > CREP 47293948 gu ku 18.2cm
        1 < Thank you for reporting with a MUAC of 18.2 cm with indicators: Diarrhea, Vomitting.
    """
