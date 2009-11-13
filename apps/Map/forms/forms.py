from django.contrib.admin import widgets
from django.utils.safestring import mark_safe
import markdown
from django import forms


class LocationWidget(forms.widgets.Widget):
    def __init__(self, *args, **kw):
        super(LocationWidget, self).__init__(*args, **kw)
        self.inner_widget = forms.widgets.HiddenInput()

    def render(self, name, value, *args, **kwargs):
        js = '''
        </script>
        <script type="text/javascript">
            //<![CDATA[
            var %(name)s_marker ;
            $(document).ready(function () {
                if (GBrowserIsCompatible()) {
                    var map = new GMap2(document.getElementById("map_%(name)s"));
                    map.setCenter(new GLatLng(4.735543142197098,-74.0822696685791), 13);
                    %(name)s_marker = new GMarker(new GLatLng(4.735543142197098,-74.0822696685791), {draggable: true});
                    map.addOverlay(%(name)s_marker);
                    map.addControl(new GLargeMapControl());
                    $('#%(name)s_id')[0].value = %(name)s_marker.getLatLng().lat() + "," + %(name)s_marker.getLatLng().lng();
                    GEvent.addListener(%(name)s_marker, "dragend", function() {
                        var point = %(name)s_marker.getLatLng();
                        $('#%(name)s_id')[0].value = point.lat() + "," + point.lng();
                    });
                }});
            $(document).unload(function () {GUnload()});
            //]]>
        </script>
        ''' % dict(name=name)
        html = self.inner_widget.render("%s" % name, None, dict(id='%s_id' % name))
        html += "<div id=\"map_%s\" style=\"width: 600px; height: 300px\"></div>" % name
        return mark_safe(js+html)

class LocationField(forms.Field):
    widget = LocationWidget
    def clean(self, value):
#        a, b = value.split(',')
#        lat, lng = float(a), float(b)
        return value