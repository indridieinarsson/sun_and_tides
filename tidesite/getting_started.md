---
layout: home
---

## Create [leaflet.js](https://leafletjs.com/) maps in [Jekyll](https://jekyllrb.com/). As easy as:

{% raw %}
```liquid

 
{% leaflet_map { "center" : [64.7741, -18.65478],
    "zoom" : 6,
    "providerBasemap": "OpenTopoMap" } %}
    
   {%- for post in site.posts -%}
        {% if post.location.geojson %}
            {% leaflet_geojson {{post.location.geojson}} %}
        {% elsif post.location.latitude and post.location.longitude %}
            {% leaflet_marker { "latitude" : {{post.location.latitude}},
                                "longitude" : {{post.location.longitude}} } %}
        {% endif %}
    {% endfor %} 
{% endleaflet_map %}
```
{% endraw %}


{% leaflet_map { "center" : [64.7741, -18.65478],
    "zoom" : 6,
    "providerBasemap": "OpenTopoMap" } %}
   {%- for post in site.posts -%}
        {% if post.location.geojson %}
            {% leaflet_geojson {{post.location.geojson}} %}
        {% endif %}
    {% endfor %} 
{% endleaflet_map %}

<h2><a href="{{site.baseurl}}getting-started/">Getting Started</a></h2>


