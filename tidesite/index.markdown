---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: home
---

{% leaflet_map { "center" : [64.7741, -18.65478],
    "zoom" : 6,
    "providerBasemap": "OpenTopoMap" } %}
    {%- for st in site.data.tidesites %}
    {% leaflet_marker {"latitude" : {{st.latitude}},
                       "longitude" : {{st.longitude}},
                       "popupContent": "{{st.sitename}}"} %} 

 {% leaflet_geojson {
 "type": "Feature",
 "properties": {"popupContent": "{{st.sitename}}",
 "href": "/tides/{{st.datafile}}.html"},
 "geometry": {
 "type": "Point",
 "coordinates": 
 [{{st.longitude}}, {{st.latitude}}]
 }
 } %}
 {% endfor %}
 {% endleaflet_map %}
