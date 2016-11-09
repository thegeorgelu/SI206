# Use https://www.si.umich.edu/programs/bachelor-science-
# information/bsi-admissions as a template.
# STEPS 
# Create a similar HTML file but 
# 1) Replace every occurrence of the word “student” with “AMAZING
# student.”  
# 2) Replace the main picture with a picture of yourself.
# 3) Replace any local images with the image I provided in media.  (You
# must keep the image in a separate folder than your html code.

# Deliverables
# Make sure the new page is uploaded to your GitHub account.


import requests
from bs4 import BeautifulSoup

base_url = 'http://collemc.people.si.umich.edu/data/bshw3StarterFile.html'
r = requests.get(base_url)
soup = BeautifulSoup(r.text, 'html.parser')
soup_str = str(soup)


html_text = soup.prettify() # turns it into a string too
# print(text)




for line in text:
	print("hi")


amazing_change = 


img = os.path.abspath('')
html_text = re.sub('logo2.png', img, html_text)

# could either use RegEx for this
# or the way Paco did it

# print(soup)

img_html = soup.find_all('img')
# print(img_html)

img = soup('img')
# print(img)
# picture = soup.find_all('div', {'class': 'field-item even'})

# print(img_html)

# run the replaceWith function?



fout = open("index.html", 'w')


fout.write(text)

# fout.write(soup_str) # this just writes the whole html in
# # write into the html file

# # you can use regex or not



fout.close()