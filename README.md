# timeline
Create a timeline chart from data on a table

From a csv file which looks like this
```
type,style,text,date,color
center,->,COVID-19 considered a very low health risk,2020-01-22,blue
left,->,First case in Germany (Munich),2020-01-27,blue
left,->,Masks sold out,2020-01-29,blue
...
```

create a file which looks like this
![timeline chart example](https://github.com/jccabrejas/timeline/blob/main/timeline_output.png)

There is a config file so some parameters can be changed easily.

At some point I wanted to create a timeline chart quickly, started looking into https://jakevdp.github.io/PythonDataScienceHandbook/04.09-text-and-annotation.html and eventually kept changing things, so I may want to come back to this at some point

For the example I took some data from Wikipedia and from https://ourworldindata.org/covid-vaccinations?country=ESP~DEU
