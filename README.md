# eurovision_scraper

A quick and dirty Scrapy script to obtain all voting results from the Eurovision songcontent (www.eurovision.tv) website. It was used to find voting cliques in a blog post (http://emptymind.me/eurovision-songcontests-votes-analysed/)

## The Scraper

The scraper uses [Scrapy](http://scrapy.org/).

## The converter

`parseblockvoting.py` reads the obtained data and converts it into a data format suitable for [GeoChart](https://developers.google.com/chart/interactive/docs/gallery/geochart) and [jVectorMap](http://jvectormap.com/).
