---
layout: post
title:  "Welcome to Jekyll!"
date:   2022-02-22 08:42:34 +0000
location: 
    geojson: '{ 
        "type": "Feature",
        "properties": {"popupContent": "Banff National Park",
            "href": "/myposts/post2"},
        "geometry": {
            "type": "Point",
            "coordinates": 
                [-21.981926,64.169902]
        }
    }'
permalink: /myposts/post2
---
    
   lkjdf 
location:
    latitude: 64.169902
    longitude: -21.981926
    
include /assets/myscript.js 
You’ll find this post in your `_posts` directory. Go ahead and edit it and re-build the site to see your changes. You can rebuild the site in many different ways, but the most common way is to run `jekyll serve`, which launches a web server and auto-regenerates your site when a file is updated.

Jekyll requires blog post files to be named according to the following format:

`YEAR-MONTH-DAY-title.MARKUP`

Where `YEAR` is a four-digit number, `MONTH` and `DAY` are both two-digit numbers, and `MARKUP` is the file extension representing the format used in the file. After that, include the necessary front matter. Take a look at the source for this post to get an idea about how it works.

Jekyll also offers powerful support for code snippets:

{% highlight ruby %}
def print_hi(name)
  puts "Hi, #{name}"
end
print_hi('Tom')
#=> prints 'Hi, Tom' to STDOUT.
{% endhighlight %}
<table class="table">
  <thead>
    <tr>
      <th>Time</th>
      <th>High/Low</th>
      <th>Level (meters)</th>
    </tr>
    <tbody id="tides">

    </tbody>
  </thead>
</table>
<script src="{{ site.baseurl }}/assets/tide-predictor.js"></script>
<script src="{{ site.baseurl }}/assets/myscript.js"></script>
<script src="https://www.puck-js.com/puck.js"></script>
<button onclick="Puck.write('LED1.set();\n');">LED On!</button>
  <button onclick="Puck.write('LED1.reset();\n');">LED Off!</button>


    "providerBasemap": "Esri.WorldTopoMap" } %}
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
 "href": "/tides/{{st.site}}"},
 "geometry": {
 "type": "Point",
 "coordinates": 
 [{{st.longitude}}, {{st.latitude}}]
 }
 } %}
 {% endfor %}
 {% endleaflet_map %}

    {%- for st in site.data.tidesites %}
    
    {{ st.sitename}}
    {% endfor %}
"type": "Feature",
        "properties": {"popupContent": "Banff National Park",
            "href": "/myposts/post2"},
        "geometry": {
            "type": "Point",
            "coordinates": 
                [-21.981926,64.169902]
        }



Check out the [Jekyll docs][jekyll-docs] for more info on how to get the most out of Jekyll. File all bugs/feature requests at [Jekyll’s GitHub repo][jekyll-gh]. If you have questions, you can ask them on [Jekyll Talk][jekyll-talk].

[jekyll-docs]: https://jekyllrb.com/docs/home
[jekyll-gh]:   https://github.com/jekyll/jekyll
[jekyll-talk]: https://talk.jekyllrb.com/
