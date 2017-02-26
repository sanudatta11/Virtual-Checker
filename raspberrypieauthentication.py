import os
import time
from os.path import join, dirname
import json
from watson_developer_cloud import VisualRecognitionV3
import picamera
from time import sleep
import zipfile

tot_image =5



#Predefined Functions

def speak(data):
    data = '"'+data+'"'
    os.system('google_speech -l en ' + data + ' -e speed 1 overdrive 9 echo 0.5 0.8 3 0.3')

def take_image(n):
    camera = picamera.PiCamera()
    for i in range(n):
        camera.capture('pic'+str(i+1)+'.jpg')
        print('Pic'+str(i+1)+' taken')

#End of Predefined Functons


#Authorized Floor Values
p1_auth = [1,5]
p2_auth = [1,2,3,4]
p3_auth = [1,4,6,7]
p4_auth = [1,2,3,7]
#Authorized Floor Values

def isauthorized(person,floor):
    print("Person="+str(person))
    print("Floor="+str(floor))
    if(int(person) == 1):
        if(floor in p1_auth):
            return 1
        else:
            return 0
    elif(int(person) == 2 ):
        if(floor in p2_auth):
            return 1
        else:
            return 0
    elif(int(person) == 3):
        if(floor in p3_auth):
            return 1
        else:
            return 0
    elif(int(person) == 4):
        if(floor in p4_auth):
            return 1
        else:
            return 0
    else:
        return 0


#Check for the Pressure input here and take value from the transducer or android app here


pressure_point = input("Enter the number of Pressure Point=")

#save it in pressure point varaible

#Greet the People inside
data_speak = 'Welcome Sir! Am Glade ........Please wait until I verify you'
speak(data_speak)
#End of Greet


#Takes the images as input for checking number of human beings available ther
#Use Pi Camera for it
#WE ARE TAKING AT MAX 5 IMAGES

take_image(tot_image)
print("Creating Archieve with "+str(tot_image)+"images")
zf = zipfile.ZipFile('pics.zip',mode='w')
try:
    for i in range(tot_image):
        print('Adding image '+str(i))
        zf.write('pic'+str(i+1)+'.jpg')
finally:
    zf.close()

print('Made archieve successfully')

#End of Image input and zipping



#Now check the image below
visual_recog_obj = VisualRecognitionV3(VisualRecognitionV3.latest_version,api_key='e086a8b65b8e6f40aa1b49c4c5490f77ea001142')
with open('pics.zip', 'rb') as image_zip:
    faceresult = visual_recog_obj.detect_faces(images_file=image_zip)
    # print(json.dumps(faceresult,indent=2))

total_women=0
total_men=0

prevcount = -1
flag = 1

for i in range(len(faceresult['images'])):
    for j in range(len(faceresult['images'][i]['faces'])):
        if faceresult['images'][i]['faces'][j]['gender']['score'] > 0.3:          #check only if high confidence
            if faceresult['images'][i]['faces'][j]['gender']['gender'] == 'FEMALE':
                total_women=total_women+1
            elif faceresult['images'][i]['faces'][j]['gender']['gender'] == 'MALE':
                total_men=total_men+1
    counthere = len(faceresult['images'][i]['faces'])
    if(prevcount == -1 or counthere == prevcount):
        flag=1
        prevcount = counthere
        counthere = -1
    else:
        flag=0
        break

if flag==1 and prevcount!=0:
    string_to_tell = "So people are counted"
    speak(string_to_tell)
    string_to_tell="Total Humans in picture "+str(prevcount)
    speak(string_to_tell)
    string_to_tell = "Number of Pressure Points Detected = " + str(pressure_point)
    speak(string_to_tell)
    if(int(pressure_point)/2 == int(prevcount)):
      prev_floor = 0
      current_journey_stat = 0
      string_to_tell = "Moving to Phase 3 verification"
      speak(string_to_tell)
      keys = []
      justitis = prevcount
      for j in range(prevcount):
          temp_val= input("Enter the secret key for passenger " + str(j+1)+"=")
          keys.append(temp_val)
      tot_floor = input("Enter total number of floors lift will stop=")
      arr_floor = []
      print("Enter the floor number to go=")
      for j in range(int(tot_floor)):
         temp_var = input("")
         arr_floor.append(int(temp_var))
         arr_floor.sort()
      for j in range(int(tot_floor)):
          time_val = arr_floor[j] - prev_floor
          prev_floor = arr_floor[j]
          print("Moving")
          time.sleep(time_val)
          string_to_tell = "Reached at floor " + str(arr_floor[j])  
          speak(string_to_tell)
          tot_coming_down = input("Total Coming down = ")   
          
          for k in range(tot_coming_down):
              person = input("Enter person coming down=")
              justitis =justitis-1;
              assert person in keys
              if(isauthorized(int(person),arr_floor[j]) == 1):
                  speak("Good Day Person" + str(person))
              else:
                  speak("Unauthorized Floor Access")
                  #Alert Security Here and Send the Messages
              if(justitis==0):
                 string_to_tell = "No Passengers Left. Going on Halt"
                 speak(string_to_tell)
                 break
          
    else:
      string_to_tell = "Sorry Verification Error"
      speak(string_to_tell)
else:
    string_to_tell="Sorry theres a mismatch in the verification process please match with security"
    speak(string_to_tell)

#end


#Hard Coded
# 5 th Floor accessible by Person2
# 7th Floor by Person1 and Person3
#All Persons can access rest floors
