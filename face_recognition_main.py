import os

import csv
import cv2
import glob

import numpy   as np
import face_recognition

from datetime  import datetime
from playsound import playsound

face_names = []
global previous_name
previous_name = ""

class SimpleFacerec:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []

        self.frame_resizing = 0.25

    def load_encoding_images(self, images_path):
        """
        Load encoding images from path
        :param images_path:
        :return:
        """
        
        # Load Images
        images_path = glob.glob(os.path.join(images_path, "*.*"))
        print("{} encoding images found.".format(len(images_path)))

        # Store image encoding and names
        for img_path in images_path:
            img = cv2.imread(img_path)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Get the filename only from the initial file path.
            basename = os.path.basename(img_path)
            (filename, ext) = os.path.splitext(basename)
            # Get encoding
            img_encoding = face_recognition.face_encodings(rgb_img)[0]

            # Store file name and file encoding
            self.known_face_encodings.append(img_encoding)
            self.known_face_names.append(filename)
            
        print("Encoding images loaded")

    def detect_known_faces(self, frame):
        
        small_frame = cv2.resize(frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.50)
            name = "Unknown"

            # Use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
            face_names.append(name)

        # Convert to numpy array to adjust coordinates with frame resizing quickly
        face_locations = np.array(face_locations)
        face_locations = face_locations / self.frame_resizing
        return face_locations.astype(int), face_names


def facerec_main(frame):

    sfr = SimpleFacerec()
    sfr.load_encoding_images("images2/")
    
    def addData (name):
        global previous_name
        with open('attendance.csv', 'a+', newline='') as f:

            if len(previous_name) == 0:
                w = csv.writer(f)
                w.writerow([name, datetime.now()])
                f.close()
                previous_name = name
            
            elif previous_name != name:
                w = csv.writer(f)
                w.writerow([name, datetime.now()])
                f.close()
                previous_name = name

            elif previous_name == name:
                f.close()
            

    face_locations, face_names = sfr.detect_known_faces(frame)
    
    for face_loc, name in zip(face_locations, face_names):
        
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

        if name == "Unknown":
            
            #region face detect for unknown input
            print("Please try again")    
            cv2.putText(frame, "Please try again",(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0,0,255), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,0,255), 4)
            #endregion face detect for unknown input
            
        else:
            #region face detect for known input
            
            #need to update
            time_lastseen = str(datetime.now()).split(' ')[0] + "@" + str(datetime.now()).split(' ')[1].split('.')[0]
            addData(name)
            
            #cv2.putText(frame, name+str(datetime.now()),(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0,255,0), 2)
            cv2.putText(frame, name.split('-')[1]+ ". "+ name.split('-')[2].replace("_"," "),(x2+5, y1 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,0), 2)
            cv2.putText(frame, "ID No:" + name.split('-')[0]                                ,(x2+5, y1 + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,0), 2)
            
            cv2.putText(frame, "Last seen:" ,(x2+5, y1 +100), cv2.FONT_HERSHEY_SIMPLEX, 0.60, (0,255,0), 2)
            cv2.putText(frame, time_lastseen,(x2+5, y1 +140), cv2.FONT_HERSHEY_SIMPLEX, 0.60, (0,255,0), 2)
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 4)
            #endregion face detect for known input
    
    return frame