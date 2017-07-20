import requests
import xml.etree.ElementTree as ET #for parsing xml
import os

def namespace_format(name, attribute, ns):
   return "{" + ns[name] + "}" + attribute
search_params = { "format":"rss", 
                  "sort":"date", 
                  "auto_make_model":"toyota",
                  "min_auto_miles":"20000",
                  "max_auto_miles":"80000",
                  "min_auto_year":"2005", 
                  "max_auto_year":"2013",
                  "min_price":"3000", 
                  "max_price":"9000",
                  "postal":"91942",
                  "search_distance":"20" 
                }
r = requests.post("http://sandiego.craigslist.org/search/sss", params=search_params)
response = r.text
root = ET.fromstring(response.encode('utf-8'))

namespace =  {"rdf":"http://www.w3.org/1999/02/22-rdf-syntax-ns#",
              "default":"http://purl.org/rss/1.0/" 
             }
result_cars = []
for item in root.findall("default:item", namespace):
  result_cars.append(item.get(namespace_format("rdf", "about", namespace)))



car_file = open("cars.txt", 'ra+')
saved_cars = car_file.readlines()
new_cars = list(set(saved_cars).symmetric_difference(set(result_cars)))

for url in new_cars:
    car_file.write(url+'\n')

if not len(new_cars) == 0: #alert new matching cars
   print "new cars"

car_file.close()



