#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

import time, datetime, os
import threading
import traceback

import component
import log

from utils.modules import try_import, get_class
import rapidsms


class Router (component.Receiver):
    incoming_phases = ('filter', 'parse', 'handle', 'catch', 'cleanup')
    outgoing_phases = ('outgoing',)

    def __init__(self):
        component.Receiver.__init__(self)
        self.backends = []
        self.apps = []
        self.running = False
        self.logger = None

    def __str__(self):
        return "Router"

    def log(self, level, msg, *args):
        self.logger.write(self, level, msg, *args)

    def set_logger(self, level, file):
        self.logger = log.Logger(level, file)

    def build_component (self, class_template, conf):
        """Imports and instantiates an module, given a dict with 
           the config key/value pairs to pass along."""
        # break the class name off the end of the module template
        # i.e. "%s.app.App" -> ("%s.app", "App")
        module_template, class_name = class_template.rsplit(".",1)
       
        # make a copy of the conf dict so we can delete from it
        conf = conf.copy()

        # resolve the component name into a real class
        module_name = module_template % (conf.pop("type"))
        module = __import__(module_name, {}, {}, [''])
        component_class = getattr(module, class_name)
        
        # create the component with an instance of this router
        # and keep hold of it here, so we can communicate both ways
        component = component_class(self)
        try:
            component._configure(**conf)
        except TypeError, e:
            # "__init__() got an unexpected keyword argument '...'"
            if "unexpected keyword" in e.message:
                missing_keyword = e.message.split("'")[1]
                raise Exception("Component '%s' does not support a '%s' option."
                        % (title, missing_keyword))
            else:
                raise
        return component

    def add_backend (self, conf):
        try:
            backend = self.build_component("rapidsms.backends.%s.Backend", conf)
            self.info("Added backend: %r" % conf)
            self.backends.append(backend)
            
        except:
            self.log_last_exception("Failed to add backend: %r" % conf)
            

    def get_backend (self, slug):
        '''gets a backend by slug, if it exists'''
        for backend in self.backends:
            print backend.slug
            print slug
            if backend.slug == slug:
                return backend
        return None


    def add_app (self, conf):

        # try to import the .app module from this app. it's okay if the
        # module doesn't exist, but all other exceptions will propagate
        app_module = try_import("%s.app" % conf["type"])

        if app_module is None:
            return None

        # find the app class (regardless of its name). it should be
        # the only subclass of rapidsms.App defined the app module
        app_class = get_class(app_module, rapidsms.App)

        # instantiate and configure the app instance.
        # TODO: app.configure must die, because the webui (in a separate
        # process) can't access the app instances, only the flat modules
        app = app_class(self)
        app._configure(**dict(conf))
        self.apps.append(app)


    def start_backend (self, backend):
        while self.running:
            try:
                backend.start()

                # if backend execution completed
                # normally (and did not raise),
                # allow the thread to terminate
                break

            except Exception, e:
                
                # an exception was raised in backend.start()
                # sleep for 5 seconds, then loop and restart it
                self.log_last_exception("Error in the %s backend" % backend.slug)

                # don't bother restarting the backend
                # if the router isn't running any more
                if not self.running:
                    break
               
                # TODO: where did the 5.0 constant come from?
                # we should probably be doing something more intelligent
                # here, rather than just hoping five seconds is enough
                time.sleep(5.0)
                self.info("Restarting the %s backend" % backend.slug)


    def start_all_apps (self):
        """Calls the _start_ method of each app registed via
           Router.add_app, logging any exceptions raised, but
           not allowing them to propagate. Returns True if all
           of the apps started without raising."""

        raised = False
        for app in self.apps:
            try:
                app.start()

            except Exception:
                self.log_last_exception("The %s app failed to start" % app.slug)
                raised = True

        # if any of the apps raised, we'll return
        # False, to warn that _something_ is wrong
        return not raised


    def start_all_backends (self):
        """Starts all backends registed via Router.add_backend,
           by calling self.start_backend in a new thread for each."""

        for backend in self.backends:
            worker = threading.Thread(
                target=self.start_backend,
                args=(backend,))

            worker.start()

            # attach the worker thread to the backend,
            # so we can check that it's still running
            backend.thread = worker


    def stop_all_backends (self):
        """Notifies all backends registered via Router.add_backend
           that they should stop. This method cannot guarantee that
           backends *will* stop in a timely manner."""

        for backend in self.backends:
            try:
                backend.stop()
                timeout = 5
                step = 0.1

                # wait up to five seconds for the backend's
                # worker thread to terminate, or log failure
                while(backend.thread.is_alive()):
                    if timeout <= 0:
                        raise RuntimeError, "The %s backend's worker thread did not terminate" % backend.slug

                    else:
                        time.sleep(step)
                        timeout -= step

            except Exception:
                self.log_last_exception("The %s backend failed to stop" % backend.slug)


    def start (self):
        self.running = True

        # dump some debug info for now
        #self.info("BACKENDS: %r" % (self.backends))
        #self.info("APPS: %r" % (self.apps))
        self.info("SERVING FOREVER...")
        
        self.start_all_backends()
        self.start_all_apps()
        
        # wait until we're asked to stop
        while self.running:
            try:
                self.run()
                
            except KeyboardInterrupt:
                self.warning("Caught KeyboardInterrupt")
                break
                
            except SystemExit:
                self.warning("Caught SystemExit")
                break
        
        self.info("Stopping all backends...")
        self.stop_all_backends()
        self.running = False

    def stop (self):
        self.running = False
        
    def run(self):
        msg = self.next_message(timeout=1.0)
        if msg is not None:
            self.incoming(msg)
    
    def __sorted_apps(self):
        return sorted(self.apps, key=lambda a: a.priority())
    
    def incoming(self, message):   
        self.info("Incoming message via %s: %s ->'%s'" %\
            (message.connection.backend, message.connection.identity, message.text))
        
        # loop through all of the apps and notify them of
        # the incoming message so that they all get a
        # chance to do what they will with it
        try:
            for phase in self.incoming_phases:
                for app in self.__sorted_apps():
                    self.debug("IN %s phase %s" % (phase, app))
                    responses = len(message.responses)
                    handled = False
                    try:
                        handled = getattr(app, phase)(message)
                    except Exception, e:
                        self.error("%s failed on %s: %r\n%s", app, phase, e, traceback.print_exc())

                    # during the "filter" phase, apps can return True
                    # to abort ALL further processing of this message
                    if phase == 'filter':
                        if handled is True:
                            self.warning('Message filtered by "%s" app', app.slug)
                            raise(StopIteration)

                    elif phase == 'handle' or phase == 'catch':
                        if handled is True:
                            self.debug("%s short-circuited %s phase" % (app, phase))
                            break

                    elif responses < len(message.responses):
                        self.warning("App '%s' shouldn't send responses in %s()!", 
                            app.config["type"], phase)

        # maybe raised within the loop, when
        # it's aborted during the filter phase
        except StopIteration:
            pass

        # now send the message's responses
        message.flush_responses()

        # we are no longer interested in
        # this message... but some crazy
        # synchronous backends might be!
        message.processed = True


    def outgoing(self, message):
        self.info("Outgoing message via %s: %s <- '%s'" %\
            (message.connection.backend, message.connection.identity, message.text))
        
        # first notify all of the apps that want to know
        # about outgoing messages so that they can do what
        # they will before the message is actually sent
        for phase in self.outgoing_phases:
            continue_sending = True
            
			# call outgoing phases in the opposite order of the
			# incoming phases so that, for example, the first app
			# called with an incoming message is the last app called
			# with an outgoing message
            for app in reversed(self.__sorted_apps()):
                self.debug("OUT %s phase %s" % (phase, app))
                
                try:
                    continue_sending = getattr(app, phase)(message)
                except Exception, e:
                    self.error("%s failed on %s: %r\n%s", app, phase, e, traceback.print_exc())
                if continue_sending is False:
                    self.info("App '%s' cancelled outgoing message", app)
                    return False

        # now send the message out
        message.connection.backend.send(message)
        self.debug("SENT message '%s' to %s via %s" % (message.text,\
			message.connection.identity, message.connection.backend.slug))
        return True
