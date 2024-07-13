import face_recognition as fr
import numpy as np
from profiles.models import Profile


def is_ajax(request):
  return request.headers.get('x-requested-with') == 'XMLHttpRequest'


def get_encoded_faces():

    qs = Profile.objects.all()

    encoded = {}

    for p in qs:
        encoding = None

        face = fr.load_image_file(p.photo.path)

        face_encodings = fr.face_encodings(face)
        if len(face_encodings) > 0:
            encoding = face_encodings[0]
        else:
            print("No face found in the image")

        if encoding is not None:
            encoded[p.user.username] = encoding

    return encoded


def classify_face(img):

    faces = get_encoded_faces()
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())

    img = fr.load_image_file(img)
 
    try:
        face_locations = fr.face_locations(img)

        unknown_face_encodings = fr.face_encodings(img, face_locations)

        face_names = []
        for face_encoding in unknown_face_encodings:
            matches = fr.compare_faces(faces_encoded, face_encoding)

            face_distances = fr.face_distance(faces_encoded, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            else:
                name = "Unknown"

            face_names.append(name)

        return face_names[0]
    except:
        return False