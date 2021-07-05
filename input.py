#importing libraries
import requests
#base line
BASE = "http://127.0.0.1:5000/driving"

#sending image
my_img = {'image': open('DL.jpg', 'rb')}
r = requests.post(BASE, files=my_img)

#printing the result
result = r.json()
for key, value in result.items():
    print(key,":", value)

print(" If the details are wrong, Please adjust the threshold value or Retake the picture")