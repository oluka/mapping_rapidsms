#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from django.views.decorators.http import require_GET, require_http_methods
from django.shortcuts import get_object_or_404
from django.db import transaction

from rapidsms.djangoproject import settings
from rapidsms.djangoproject.utils import *
from tags.models import *
from reporters.utils import *



# likewise, is the logger app running? we'll
# add a mini message log just for this reporter
use_logger = ("logger" in settings.RAPIDSMS_APPS)
if use_logger:
    from logger.models import *



@require_GET
def index(req):
    return render_to_response(req,
        "tags/index.html", {
        "tags": paginated(req, Tag.objects.all(), prefix="tag")
       })




@require_http_methods(["GET", "POST"])
def add_tag(req):
    def get(req):
        
        # maybe pre-populate the "connections" field
        # with a connection object to convert into a
        # tag, if provided in the query string
        connections = []
        if "connection" in req.GET:
            connections.append(
                get_object_or_404(
                    PersistantConnection,
                    pk=req.GET["connection"]))

       # context = {
            # display paginated tags in the left panel
             #  "tag": None }
            
          
        # populate the "location" field if
        # we're running the locations app
        """if use_locations:
            context["locations_label"] = LocationType.label(only_linkable=True).singular
            context["all_locations"]   = Location.objects.filter(type__is_linkable=1)"""

        return render_to_response(req,
            "tags/tag.html"
            )

    @transaction.commit_manually
    def post(req):
        
        # check the form for errors
        errors = check_tag_form(req)
        
        # if any fields were missing, abort. this is
        # the only server-side check we're doing, for
        # now, since we're not using django forms here
        if errors["missing"]:
            transaction.rollback()
            return message(req,
                "Missing Field(s): %s" %
                    ", ".join(missing),
                link="/tags/add")
        
        try:
            # create the tag object from the form
            rep = insert_via_querydict(Tag, req.POST)
            rep.save()
            
            # every was created, so really
            # save the changes to the db
            update_tag(req, rep)
            transaction.commit()
            
            # full-page notification
            return message(req,
                "Tag %d added" % (rep.pk),
                link="/tags")
        
        except Exception, err:
            transaction.rollback()
            raise
    
    # invoke the correct function...
    # this should be abstracted away
    if   req.method == "GET":  return get(req)
    elif req.method == "POST": return post(req)
    
@require_http_methods(["GET", "POST"])  
def edit_tag(req, pk):
    tag = get_object_or_404(Tag, pk=pk)
    
    def get(req):
        context = {
            # display paginated tags in the left panel
            #"tag": paginated(req, tag.objects.all())}
            "tag":tag}
            
      #  if use_logger:
       #     context["message_log"] = paginated(req, combined_message_log(tag), prefix="msg", wrapper=combined_message_log_row)

        return render_to_response(req,
            "tags/tag.html",
            context)
    
    @transaction.commit_manually
    def post(req):
        
        # if DELETE was clicked... delete
        # the object, then and redirect
        if req.POST.get("delete", ""):
            pk = tag.pk
            tag.delete()
            
            transaction.commit()
            return message(req,
                "tag %d deleted" % (pk),
                link="/tags")
                
        else:
            # check the form for errors (just
            # missing fields, for the time being)
            errors = check_tag_form(req)
            
            # if any fields were missing, abort. this is
            # the only server-side check we're doing, for
            # now, since we're not using django forms here
            if errors["missing"]:
                transaction.rollback()
                return message(req,
                    "Missing Field(s): %s" %
                        ", ".join(errors["missing"]),
                    link="/tags/%s" % (tag.pk))
            
            try:
                # automagically update the fields of the
                # tag object, from the form
                update_via_querydict(tag, req.POST).save()
                update_tag(req, tag)
                
                # no exceptions, so no problems
                # commit everything to the db
                transaction.commit()
                
                # full-page notification
                return message(req,
                    "tag %d updated" % (tag.pk),
                    link="/tags")
            
            except Exception, err:
                transaction.rollback()
                raise
        
    # invoke the correct function...
    # this should be abstracted away
    if   req.method == "GET":  return get(req)
    elif req.method == "POST": return post(req)
    
def check_tag_form(req):
    
    # verify that all non-blank
    # fields were provided
    missing = [
        field.verbose_name
        for field in Tag._meta.fields
        if req.POST.get(field.name, "") == ""
           and field.blank == False]
    
    # TODO: add other validation checks,
    # or integrate proper django forms
    return {
        "missing": missing }
        
def update_tag(req, tag):   
        tag.save()

def message(req, msg, link=None):
    return render_to_response(req,
        "message.html", {
            "message": msg,
            "link": link
    })

        




