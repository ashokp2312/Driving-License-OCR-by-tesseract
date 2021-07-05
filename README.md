# Driving-License-OCR-by-tesseract

In this project, the details of the Driving Licence are extracted and returned in the JSON format.
We use Tesseract OCR to convert the image to text. One must download tesseract to use this program. The logic is written in the main.py file and used in api.py for implementation.
I have created a RESTApi for the project.

## Steps to implement:
1. Install the necessary packages and Tesseract 
2. Run the api.py file it will run on the local host. 
3. The default image in the code is DL.jpg, one can change it using the input.py code. Makesure the image you want to use is in the same folder as the input.py file.
4. After running the api.py, give the input image and run the input.py file in an another prompt. The results are obtained and it will print the details on the Driving License.
