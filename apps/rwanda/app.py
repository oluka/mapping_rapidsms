#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


import re
import rapidsms
from rapidsms.parsers import Matcher
from persistance.models import *
from models import *
from locations.models import *
from tags.models import *
from people.models import *
from rwanda.models import *
from rwanda.utils import *


class App(rapidsms.App):
    pass


class Appx(object):
    MSG = {
        "en": {
            "bad-alias":   "Sorry, I don't know anyone by that name.",
            "first-login": "Nice to meet you, %(name)s. Your alias is %(alias)s.",
            "login":       "Hello, %(name)s. It has been %(days)d days since I last heard from you.",
            "reminder":    "I think you are %(name)s.",
            "dont-know":   "Please register your phone with RapidSMS.",
            "list":        "I have %(num)d %(noun)s: %(items)s",
            "empty-list":  "I don't have any %(noun)s.",
            "lang-set":    "I will now speak to you in English, where possible.",
            "denied":      "Sorry, you must identify yourself before you can do that.",
            "disabled":    "Sorry, but that functionality is disabled." },

        # worst german translations _ever_
        # just an example. all of this stuff
        # should be moved to an i18n app!
        "de": {
            "bad-alias":   "Tut mir leit, ich weiss nicht diesen Namen",
            "first-login": "%(name)s hallo! Ich habe nicht gesehen, bevor Sie",
            "login":       "%(name)s hallo! Ich habe nicht gesehen, Sie sich fur %(days)d Tag",
            "reminder":    "Sie sind %(name)s.",
            "lang-set":    "Sie sind Deutsche." }}

    HELP = [
        ("identify", "To identify yourself to RapidSMS, reply: IDENTIFY <alias>")
    ]

    datesep = r"(\.|\/|\\|\-)"
    date = r"\d\d?"
    month = r"\d\d?"
    year = r"\d{2}(\d{2})?"
    datepattern = r"^\d\d?[\.|\/|\\|\-]\d\d?[\.|\/|\\|\-]\d{2}(\d{2})?$"
     
    def __str(self, key, reporter=None, lang=None):

        # if no language was explicitly requested,
        # inherit it from the reporter, or fall
        # back to english. because everyone in the
        # world speaks english... right?
        if lang is None:
            if reporter is not None:
                lang = reporter.language

            # fall back
            if lang is None:
                lang = "en"

        # look for an exact match, in the language
        # that the reporter has chosen as preferred
        if lang is not None:
            if lang in self.MSG:
                if key in self.MSG[lang]:
                    return self.MSG[lang][key]

        # not found in localized language. try again in english
        # TODO: allow the default to be set in rapidsms.ini
        return self.__str(key, lang="en") if lang != "en" else None


    def __deny(self, msg):
        """Responds to an incoming message with a localizable
           error message to instruct the caller to identify."""
        return msg.respond(self.__str("denied", msg.reporter))


  #  def configure(self, allow_join, allow_list, **kwargs):
    #    self.allow_join = allow_join
     #   self.allow_list = allow_list


    def handle(self, msg):
        matcher = Matcher(msg)

        # TODO: this is sort of a lightweight implementation
        # of the keyworder. it wasn't supposed to be. maybe
        # replace it *with* the keyworder, or extract it
        # into a parser of its own
        map = {
            "registerChild":  ["(?:born) (whatever)"],   
            "registerMother":  ["(?:preg) (whatever)"],   
            "reporterChild":  ["(?:crep|mrep) (whatever)"],
            "reporterMother":  ["(?:crep|mrep) (whatever)"]
        }
        self.info("Entered mother")
        #the user is unidentified Dont add pregnancy of births.
        
        
        # search the map for a match, dispatch
        # the message to it, and return/stop
        for method, patterns in map.items():
            if matcher(*patterns) and hasattr(self, method):  
                getattr(self, method)(msg, *matcher.groups)
                return True

        # no matches, so this message is not
        # for us; allow processing to continue
        return False
        
    def parse_person(self,msg,text):
        allwords = text.split()
        tagsfound = []
        person = Person()
        #Find all occurances of the tags /codes and save them. or send alerts.                           
        for word in allwords:
             if len(word)==2 and Tag.objects.filter(code__iexact=word).count():
                    tagsfound = tagsfound + word
                    
        setattr(person,'tags',tagsfound)        
                           
        if len(allwords) < 1:
            msg.respond("missing national id")
            return None
                               
        # Determine if the word is a National id 
        m = re.match(r"^(\d+)$", allwords[0], re.IGNORECASE)
        if m is not None:
            MatchCode = m.group(0)
            setattr(person,'uniqueid', MatchCode)         
        else:
            msg.respond("missing or invalid national id")
            return None
            
        if len(allwords) < 2:
            msg.respond("missing national id and date")
            return None        
              
        # Determine if the word is a Date 
        m = re.match( self.datepattern, allwords[1], re.IGNORECASE)
        if m is not None:
            MatchCode = m.group(0)
            setattr(person,'date', util.get_good_date(MatchCode))
        else:
            msg.respond("missing or invalid date")
            return None 
                            
         # Determine if the word is weight 
        m = re.match(  r"(\d+(?:\.\d+))(kg|lb)$", allwords[-1], re.IGNORECASE)
        if m is not None:
            MatchCode = m.group(0)
            setattr(person,'weight', MatchCode.replace("kg","").replace("lb",""))      
            self.info(" weight %s"  % MatchCode)
        
        return person 


    def registerChild(self, msg, name):
       
        try:
            if msg.reporter is None:
                 msg.respond("you are not register")
                 return False
                 
            child = self.parse_person(msg,name)
            if child is None:
                    return False
            
            personid = child.uniqueid
            DOB =  child.date
            self.info("Dob %s"% DOB)
            weight = child.weight
            persontype ,isno = PersonType.objects.get_or_create(singular="Child" , plural="Children")
                                
            if personid is not None: 
                    child , dontcare  = Child.objects.get_or_create( code=personid,name=personid ,date_of_birth = DOB ,weight=weight, type=persontype)           
                    child.save()        
                    self.info("Success fully added/updated child")                    
                    msg.respond("Birth was added successfully")
                    
            return True
            
        except:
                msg.respond("Sorry, I couldn't add child.")
                raise    

    def registerMother(self, msg, name):
       
        try:
            if msg.reporter is None:
                 msg.respond("you are not register")
                 return False 
            person =  self.parse_person(msg,name)
            if person is None:
                 return False  
          #  getattr(person,'uniqueid')
            personid = person.uniqueid
          #  getattr(person,"date",date_of_m)
            date_of_m = person.date
            self.info("Date field %s" % date_of_m)
            persontype ,isno = PersonType.objects.get_or_create(singular="Pregnant Woman" , plural="Pregnant Women")
             
             
            self.info("Personid %s " % personid)   
            if personid is not None: 
                pregnant ,dontcare  = Pregnant.objects.get_or_create(  code=personid , name=personid, gender ="F" , 
                date_last_menses = date_of_m ,type=persontype)           
                pregnant.save()
                self.info("Successfully added or updated mother")                          
                msg.respond("pregnancy was added successfully")

            return True
            
        except:
                msg.respond("Sorry, I couldn't add pregnant woman.")
                raise    
 
    def identify(self, msg, alias):
        try:

            # give me reporter.
            # if no alias will match,
            # exception must raise
            rep = Reporter.objects.get(alias=alias)

        # no such alias, but we can be pretty sure that the message
        # was for us, since it matched a pretty specific pattern
        # TODO: levenshtein spell-checking from rapidsms/ethiopia
        except Reporter.DoesNotExist:
            msg.respond(self.__str("bad-alias"))
            return True


        # before updating the connection, take note
        # of the last time that we saw this reporter
        ls = rep.last_seen()

        # assign the reporter to this message's connection
        # (it may currently be assigned to someone else)
        msg.persistant_connection.reporter = rep
        msg.persistant_connection.save()
        msg.reporter = rep


        # send a welcome message back to the now-registered reporter,
        # depending on how long it's been since their last visit
        if ls is not None:
            msg.respond(
                self.__str("login", rep) % {
                    "name": unicode(rep),
                    "days": (datetime.now() - ls).days })

        # or a slightly different welcome message
        else:
            msg.respond(
                self.__str("first-login", rep) % {
                    "name": unicode(rep),
                    "alias": rep.alias })

        # re-call this app's prepare, so other apps can
        # get hold of the reporter's info right away
        self.parse(msg)


    def remind(self, msg):

        # if a reporter object was attached to the
        # message by self.parse, respond with a reminder
        if msg.reporter is not None:
            msg.respond(
                self.__str("reminder", msg.reporter) % {
                    "name": unicode(msg.reporter) })

        # if not, we have no idea
        # who the message was from
        else:
            msg.respond(self.__str(
                "dont-know",
                msg.reporter))


    def reporters(self, msg):

        # abort if listing reporters isn't allowed
        # (it can get rather long and expensive)
        if not self.allow_join:
            msg.respond(self.__str("disabled"))
            return True

        # not identified yet; reject, so
        # we don't allow random people to
        # query our reporters list
        if msg.reporter is None:
            msg.respond(self.__str("denied"))
            return True

        # collate all reporters, with their full name,
        # username, and current connection.
        items = [
            "%s (%s) %s" % (
                rep.full_name(),
                rep.alias,
                rep.connection().identity)
            for rep in Reporter.objects.all()
            if rep.connection()]

        # respond with the concatenated list.
        # no need to check for empty _items_. there will
        # always be at least one reporter, because only
        # identified reporters can trigger this handler
        msg.respond(
            self.__str("list", msg.reporter) % {
                "items": ", ".join(items),
                "noun":  "reporters",
                "num":    len(items) })


    def lang(self, msg, code):

        # reqiure identification to continue
        # TODO: make this check a decorator, so other apps
        #  can easily indicate that methods need a valid login
        if msg.reporter is not None:

            # if the language code was valid, save it
            # TODO: obviously, this is not cross-app
            if code in self.MSG:
                msg.reporter.language = code
                msg.reporter.save()
                resp = "lang-set"

            # invalid language code. don't do
            # anything, just send an error message
            else: resp = "bad-lang"

        # if the caller isn't logged in, send
        # an error message, and halt processing
        else: resp = "denied"

        # always send *some*
        # kind of response
        msg.respond(
            self.__str(
                resp, msg.reporter))
