import cv2
import sys
#from VideoCapture import Device

cam = cv2.VideoCapture(0)
s, img = cam.read()
if s:    # frame captured without any errors
    cv2.namedWindow("cam-test")
    cv2.imshow("cam-test",img)
    cv2.waitKey(0)
    cv2.destroyWindow("cam-test")
    cv2.imwrite("webcam.jpg",img)
# Get user supplied values
imagePath = 'webcam.jpg'

cascPathf = "haarcascade_frontalface_default.xml"
cascPathe = "parojos.xml"
cascPathm = "Mouth.xml"
cascPathn = "Nariz_nuevo_20stages.xml"

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPathf)
eyeCascade = cv2.CascadeClassifier(cascPathe)
mouthCascade = cv2.CascadeClassifier(cascPathm)
noseCascade = cv2.CascadeClassifier(cascPathn)

# Read the image
image = cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
eyes = eyeCascade.detectMultiScale(gray)
faces = faceCascade.detectMultiScale(gray)
lips = mouthCascade.detectMultiScale(gray)
noses = noseCascade.detectMultiScale(gray)

# print "Found {0} Faces!".format(len(faces))
# print "Found {0} Eyes!".format(len(eyes))
# print "Found {0} Lips!".format(len(lips))
# print "Found {0} Noses!".format(len(noses))

# Draw a rectangle around the faces
counter=0
avg=0
first=True
proportions=[]
realnose=[]
realmouth=[]
ratios=[]
for (x, y, w, h) in faces:
	cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
	for(xe, ye, we, he) in eyes:
		if xe in xrange(x, x+w) and ye in xrange(y, y+h):
			cv2.rectangle(image, (xe, ye), (xe+we, ye+he), (0, 255, 0), 2)
			print ("Eye seperation is: "+str(we)+"px")
			for(xm, ym, wm, hm) in lips:
				if xm and xm+wm in xrange(xe, xe+we) and ym and ym+hm in xrange(ye+he, y+h) and ym>ye+he:
					realmouth.append([xm, ym, wm, hm])
			maxmouth=[0, 0, 0, 0]
			for mouth in realmouth:
				if mouth[1]>maxmouth[1]:
					maxmouth=mouth
			if not maxmouth==[0, 0, 0, 0]:
				xm, ym, wm, hm=maxmouth[0], maxmouth[1], maxmouth[2], maxmouth[3]				
				cv2.rectangle(image, (xm, ym), (xm+wm, ym+hm), (0, 0, 225), 2)	
				print ("Mouth width is: "+str(wm)+"px")
				for(xn, yn, wn, hn) in noses:
					if xn and xn+wn in xrange(xe, xe+we) and yn and yn+hn in xrange(ye+he, ym):
						realnose.append([xn, yn, wn, hn])
				maxnose=[0, 0, 0, 0]
				for nose in realnose:
					if nose[0]>maxnose[0]:
						maxnose=nose
				if not maxnose==[0, 0, 0, 0]:
					xn, yn, wn, hn=maxnose[0], maxnose[1], maxnose[2], maxnose[3]
					cv2.rectangle(image, (xn, yn), (xn+wn, yn+hn), (0, 225, 225), 2)							
					print ("Nose is at: ("+str((xn+wn)/2)+", "+str((yn+hn)/2)+")")
					proportions.append([[x, y, w, h],[xe, ye, we, he], [xm, ym, wm, hm], [xn, yn, wn, hn]])	
    
cv2.imshow("Faces found", image)
cv2.waitKey(0)
for i in xrange(len(proportions)): 
	ratios.append(proportions[i][0][3]/proportions[i][0][2])
	numer=((proportions[i][1][1]+proportions[i][1][3]/2)-proportions[i][0][1])*(proportions[i][3][1]+proportions[i][3][3]-(proportions[i][1][2]+proportions[i][1][3]/2))*((proportions[i][1][2]+proportions[i][1][3]/2)-proportions[i][0][1])
	denom=(proportions[i][3][1]+proportions[i][3][3]-(proportions[i][1][2]+proportions[i][1][3]/2))*((proportions[i][0][1]+proportions[i][0][3])-proportions[i][3][1]-proportions[i][3][3])*((proportions[i][0][1]+proportions[i][0][3])-proportions[i][3][1]-proportions[i][3][3])
	#print numer
	#print denom
	numer+=0.0
	#print numer/denom
	ratios.append(numer/denom)
	#print ratios[1]
	# print (proportions[i][3][1]+proportions[i][3][3]-(proportions[i][1][2]+proportions[i][1][3]/2))/((proportions[i][0][1]+proportions[i][0][3])-proportions[i][3][1]-proportions[i][3][3])
	# print (proportions[i][1][3]/2)/((proportions[i][0][1]+proportions[i][0][3])-proportions[i][3][1]-proportions[i][3][3])
	score=(ratios[2*i]/1.6)*ratios[2*i+1]*100
	score= 100 if score%100==0 else score%100
	print "Your score is: "+str(int(score))+"!"