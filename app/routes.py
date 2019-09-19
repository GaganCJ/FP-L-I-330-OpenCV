from flask import render_template, redirect, url_for, request, send_from_directory
from app import app
import datetime, os, sys, csv
from werkzeug.utils import secure_filename
import faceops
from flask_uploads import UploadSet, configure_uploads, IMAGES

UPLOAD_FOLDER = os.getcwd() + r"\app\uploads"
#ALLOWED_EXTENSIONS = set(['jpg','jpeg'])
photos = UploadSet('photos',IMAGES)
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOADED_PHOTOS_DEST'] = UPLOAD_FOLDER
configure_uploads(app, photos)
DATA_FILENAME = os.getcwd() + r"\app\data.csv"
att = r"attendance" + str(datetime.date.today()) + r".csv"
ATT_FILENAME = os.getcwd() + r"\app\\" + att
OUT_PHOTO = os.getcwd() + r"app\static\output1.jpg"

@app.route('/')
def check():
	return 'server ready check 1,2,3,...'
@app.route('/main')
def index():
	return render_template("main.html")

@app.route('/upload',methods=['GET','POST'])
def upload():
	if request.method == 'POST' and 'photo' in request.files:
		print("OK1")
		filename = photos.save(request.files['photo'])
		print(filename)
		hexfs = os.getcwd() + r'\app\encodings.pickle'
		print("OK3")
		# load the known faces and embeddings
		print("[INFO] loading encodings...")
		data = pickle.loads(open(hexfs, "rb").read())

		# load the input image and convert it from BGR to RGB
		image = cv2.imread(UPLOAD_FOLDER + "\\" + filename)
		print("OK3")
		rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

		# detect the (x, y)-coordinates of the bounding boxes corresponding
		# to each face in the input image, then compute the facial embeddings
		# for each face
		print("[INFO] recognizing faces...")
		boxes = face_recognition.face_locations(rgb, model="cnn")
		encodings = face_recognition.face_encodings(rgb, boxes)

		print("OK$")

		# initialize the list of names for each face detected
		names = []

		# initialize the list of names with attendance status
		status=[]

		# loop over the facial embeddings
		for encoding in encodings:
			# attempt to match each face in the input image to our known
			# encodings
			matches = face_recognition.compare_faces(data["encodings"], encoding)
			name = "Unknown"

		# check to see if we have found a match
			if True in matches:
				print("OK5")
				# find the indexes of all matched faces then initialize a
				# dictionary to count the total number of times each face
				# was matched
				matchedIdxs = [i for (i, b) in enumerate(matches) if b]
				counts = {}

			# loop over the matched indexes and maintain a count for
			# each recognized face face
				for i in matchedIdxs:
					name = data["names"][i]
					counts[name] = counts.get(name, 0) + 1

			# determine the recognized face with the largest number of
			# votes (note: in the event of an unlikely tie Python will
			# select first entry in the dictionary)
				name = max(counts, key=counts.get)

		# update the list of names
			names.append(name)

		# # loop over the recognized faces
		# for ((top, right, bottom, left), name) in zip(boxes, names):
		#     # draw the predicted face name on the image
		#     cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
		#     y = top - 15 if top - 15 > 15 else top + 15
		#     cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

		# # show the output image
		# #cv2.imshow("Image", image)
		# #cv2.imwrite(OUT_PHOTO,image)
		# #cv2.waitKey(0)
		heady = ['Names','Status'] #[str(datetime.date.today())]
		with open(ATT_FILENAME,'w',newline='') as res, open(DATA_FILENAME,'r',newline='') as orig:
			reader = csv.reader(orig)
			duplic = list(reader)
			writer = csv.DictWriter(res,fieldnames=heady)
			writer.writeheader()
			print("OK4")
			for a in names:
				print(a)
				writer.writerow({'Names':a,'Status':'Present'})
				for b in duplic:
					print(b)
					if b[0] == a:
						duplic.remove(b)
			c = len(duplic)
			while c != 0:
				d = duplic.pop()
				print(d)
				writer.writerow({'Names':d[0],'Status':'Absent'})
				c = c - 1
			res.close()
			orig.close()

		with open(ATT_FILENAME,'r') as tell:
			say = csv.DictReader(tell)
			for row in say:
				status.append([row['Names'],row['Status']])
			tell.close()
	return render_template("main.html",name = status)

@app.route('/train')
def face_train():
	dataset = os.getcwd() + r'\app\dataset'
	hexfs = os.getcwd() + r'\app\encodings.pickle'
	# grab the paths to the input images in our dataset
	print("[INFO] quantifying faces...")
	imagePaths = list(paths.list_images(dataset))

	# initialize the list of known encodings and known names
	knownEncodings = []
	knownNames = []
	
	# loop over the image paths
	for (i, imagePath) in enumerate(imagePaths):
	# extract the person name from the image path
		print("[INFO] processing image {}/{}".format(i + 1, len(imagePaths)))
		name = imagePath.split(os.path.sep)[-2]

		# load the input image and convert it from RGB (OpenCV ordering)
		# to dlib ordering (RGB)
		image = cv2.imread(imagePath)
		rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

		# detect the (x, y)-coordinates of the bounding boxes
		# corresponding to each face in the input image
		boxes = face_recognition.face_locations(rgb, model="cnn")

		# compute the facial embedding for the face
		encodings = face_recognition.face_encodings(rgb, boxes)

		# add each encoding + name to our set of known names and encodings
		for encoding in encodings:
			knownEncodings.append(encoding)
			knownNames.append(name)
			
	# dump the facial encodings + names to disk
	print("[INFO] serializing encodings...")
	data = {"encodings": knownEncodings, "names": knownNames}
	f = open(hexfs, "wb")
	f.write(pickle.dumps(data))
	f.close()
	with open(DATA_FILENAME,'w',newline='') as orig:
		writer = csv.writer(orig)
		for row in list(set(knownNames)):
			writer.writerow([row])
		orig.close()
	return render_template("main.html")

	
@app.route('/download',methods=['GET','POST'])
def download_file():
	def back_to_main():
		return redirect(url_for('index'))
	back_to_main()
	att = r"attendance" + str(datetime.date.today()) + r".csv"
	return send_from_directory(directory = os.getcwd() + r'\app', filename=att)