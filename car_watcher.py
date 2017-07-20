import requests
import xml.etree.ElementTree as ET #for parsing xml
import os

#Format xml elements that use a given namespace 
def namespace_format(name, attribute, ns):
   return "{" + ns[name] + "}" + attribute

#Search for cars on craiglist and email if new ones appear
def watch_cars(search_params, location):
   
   #Determine if a new item fitting the given 
   r = requests.post("http://sandiego.craigslist.org/search/sss", params=search_params)
   response = r.text
   root = ET.fromstring(response.encode('utf-8')) #turn xml into an element tree
   
   namespace =  {"rdf":"http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                 "default":"http://purl.org/rss/1.0/" 
                }
   result_cars = []
   for item in root.findall("default:item", namespace):
     result_cars.append(item.get(namespace_format("rdf", "about", namespace)))
   
   
   #Read file to determine which cars have been seen
   car_file = open("cars.txt", 'a+') #append, read, and create if not exists
   car_file.seek(0) #otherwise reading/appending starts at end of file because of append mode
   saved_cars = car_file.readlines()
   saved_cars = [ car_url[:-1] for car_url in saved_cars] #get rid of trailing '\n'
   
   #New cars are only those not already saved 
   new_cars = list(set(result_cars) - set(saved_cars))
   
   #Save new cars to file 
   for url in new_cars:
       car_file.write(url+'\n')
   
   #Alert when new matches are found
   if not len(new_cars) == 0: #alert new matching cars
      print "new cars"
      print new_cars
   
   car_file.close()


   
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
location = "sandiego"

watch_cars(search_params, location)
