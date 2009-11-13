#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

"""
This app provides a generic way for Reporters and PersistantConnections
to "follow" events triggered by other models. The linking is performed
by dynamically-generated models; This maintains foreign key consistancy
and integrates with the Django admin nicely.

To make a Model followable, just add a "followable=True" attribute. The
apps.follow.models module will notice, and create an intermediate model
to link your model with Reporter and/or PersistantConnection.
For example:

    class MyFollowableModel(models.Model):
        something = models.CharField(max_length=20)
        followable = True

Later that day, in the shell...

    >>> x = MyFollowableModel(something="Alpha")
    >>> adam = Reporter.objects.get(alias="adammck")
    >>> x.followers.add(reporter=adam)

That's magic! It's not very Python-ish, since it's not explicit and all
that, but allows models to easily become "followable" without requiring
this app to be present. If it's not running, nothing explodes.

For a model to be followable over SMS, it also needs to be searchable.
Luckily, this is also easy. See the rapidsms.search module for docs, or
apps.reporters.models.Reporter.__search__ for an example. Once your model
is searchable, it can be followed by anyone over SMS with some fairly
simple syntax:

    ~~> I AM adammck
    <~~ Hello, Adam Mckaig!

    ~~> FOLLOW ewheeler
    <~~ You are now following Evan Wheeler.

    ~~> FOLLOW @3 czue nyc
    <~~ You are now following Mark Johnston, Cory Zue, and New York City.

Back in the shell...

    >>> adam = Reporter.objects.get(alias="adammck")

    >>> adam.following_reporter_set.all()
    [<Reporter #2: Evan Wheeler (ewheeler)>,
     <Reporter #3: Mark Johnston (mej)>,
     <Reporter #4: Cory Zue (czue)>]

    >>> adam.following_location_set.all()
    [<Location #1: New York City>]
"""
