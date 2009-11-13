#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from django.views.decorators.http import require_GET, require_http_methods
from django.shortcuts import get_object_or_404
from django.db import transaction

from rapidsms.djangoproject import settings
from rapidsms.djangoproject.utils import *
from follow.models import *
from follow.utils import *
from reporters.utils import *
from follow.models import *
from locations.models import Location
from reporters.models import *


# likewise, is the logger app running? we'll
# add a mini message log just for this reporter
use_logger = ("logger" in settings.RAPIDSMS_APPS)
if use_logger:
    from logger.models import *

#>>> for model in followable_models():
#...     model.__follow_model__

@require_GET
def index(req):
    reporter =[]
    location=[]
    group=[]
    for model in followable_models():
  #      if type(model.__follow_model__) == type(ReporterGroup) :
  #           group = group + list(model.__follow_model__.objects.all())      
   #     if type(model.__follow_model__) == type(Reporter)  :
          objType =  model.__follow_model__.__name__ 
          reporter = reporter + list(model.__follow_model__.objects.all()) 
  #      if type(model.__follow_model__) == type(Location) :
   #          location = location + list(model.__follow_model__.objects.all())

    return render_to_response(req,
        "follow/index.html", {
        "followReporter": paginated(req,reporter)
    #    "followLocation": paginated(req,location),
     #   "followGroup": paginated(req,group)
       })

@require_http_methods(["GET", "POST"])
def add_follow(req):
    def get(req):
        
        # maybe pre-populate the "connections" field
        # with a connection object to convert into a
        # follow, if provided in the query string
        connections = []
        if "connection" in req.GET:
            connections.append(
                get_object_or_404(
                    PersistantConnection,
                    pk=req.GET["connection"]))

       # context = {
            # display paginated follow in the left panel
             #  "follow": None }
            
          
        # populate the "location" field if
        # we're running the locations app
        """if use_locations:
            context["locations_label"] = LocationType.label(only_linkable=True).singular
            context["all_locations"]   = Location.objects.filter(type__is_linkable=1)"""

        return render_to_response(req,
            "follow/follow.html"
            )

    @transaction.commit_manually
    def post(req):
        
        # check the form for errors
        errors = check_follow_form(req)
        
        # if any fields were missing, abort. this is
        # the only server-side check we're doing, for
        # now, since we're not using django forms here
        if errors["missing"]:
            transaction.rollback()
            return message(req,
                "Missing Field(s): %s" %
                    ", ".join(missing),
                link="/follow/add")
        
        try:
            # create the follow object from the form
            rep = insert_via_querydict(follow, req.POST)
            rep.save()
            
            # every was created, so really
            # save the changes to the db
            update_follow(req, rep)
            transaction.commit()
            
            # full-page notification
            return message(req,
                "follow %d added" % (rep.pk),
                link="/follow")
        
        except Exception, err:
            transaction.rollback()
            raise
    
    # invoke the correct function...
    # this should be abstracted away
    if   req.method == "GET":  return get(req)
    elif req.method == "POST": return post(req)
    
@require_http_methods(["GET", "POST"])  
def edit_follow(req, pk):
    follow = get_object_or_404(follow, pk=pk)
    
    def get(req):
        context = {
            # display paginated follow in the left panel
            #"follow": paginated(req, follow.objects.all())}
            "follow":follow}
            
      #  if use_logger:
       #     context["message_log"] = paginated(req, combined_message_log(follow), prefix="msg", wrapper=combined_message_log_row)

        return render_to_response(req,
            "follow/follow.html",
            context)
    
    @transaction.commit_manually
    def post(req):
        
        # if DELETE was clicked... delete
        # the object, then and redirect
        if req.POST.get("delete", ""):
            pk = follow.pk
            follow.delete()
            
            transaction.commit()
            return message(req,
                "follow %d deleted" % (pk),
                link="/follow")
                
        else:
            # check the form for errors (just
            # missing fields, for the time being)
            errors = check_follow_form(req)
            
            # if any fields were missing, abort. this is
            # the only server-side check we're doing, for
            # now, since we're not using django forms here
            if errors["missing"]:
                transaction.rollback()
                return message(req,
                    "Missing Field(s): %s" %
                        ", ".join(errors["missing"]),
                    link="/follow/%s" % (follow.pk))
            
            try:
                # automagically update the fields of the
                # follow object, from the form
                update_via_querydict(follow, req.POST).save()
                update_follow(req, follow)
                
                # no exceptions, so no problems
                # commit everything to the db
                transaction.commit()
                
                # full-page notification
                return message(req,
                    "follow %d updated" % (follow.pk),
                    link="/follow")
            
            except Exception, err:
                transaction.rollback()
                raise
        
    # invoke the correct function...
    # this should be abstracted away
    if   req.method == "GET":  return get(req)
    elif req.method == "POST": return post(req)
    
def check_follow_form(req):
    
    # verify that all non-blank
    # fields were provided
    missing = [
        field.verbose_name
        for field in follow._meta.fields
        if req.POST.get(field.name, "") == ""
           and field.blank == False]
    
    # TODO: add other validation checks,
    # or integrate proper django forms
    return {
        "missing": missing }
        
def update_follow(req, follow):   
        follow.save()

def message(req, msg, link=None):
    return render_to_response(req,
        "message.html", {
            "message": msg,
            "link": link
    })

        




