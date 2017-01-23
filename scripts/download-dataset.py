
import os
import sys
import urlparse as url
import requests
import csv
import random
import django

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VAL_RAT = 0.25

if len(sys.argv)>=4:
    CSV_PATH = sys.argv[1]
    VAL_CSV_PATH = sys.argv[2]
    DOWNLOAD_PATH = sys.argv[3]
else:
    CSV_PATH = os.path.join(BASE_PATH, 'train.csv')
    DOWNLOAD_PATH = 'D:/descargas_png/'

print("WORKIN ON " + BASE_PATH)
sys.path.append(BASE_PATH)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "peppers.settings")

django.setup()

from django.conf import settings
from rest.models import CorreccionDiagnostico, SugerenciaDiagnostico, Imagen


def get_correccion_object(imagen):
    try:
        im = CorreccionDiagnostico.objects.filter(imagen=imagen)
    except CorreccionDiagnostico.DoesNotExist:
        im = None
    return im


def get_sugerencia_object(imagen):
    try:
        im = SugerenciaDiagnostico.objects.get(imagen=imagen)
    except SugerenciaDiagnostico.DoesNotExist:
        im = None
    return im


def generate_download_url(studyuid, seriesuid, objectuid):
    rel_path = settings.DICOM_PNG_URL_PATTERN%{'studyuid': studyuid,
                                              'seriesuid': seriesuid,
                                              'objectuid': objectuid }
    dcm_path = url.urljoin(settings.DCM4CHEE_HOSTDIR, rel_path)
    return dcm_path


def download_img(url, name):
    r = requests.get(url, stream=True)
    f_path = os.path.join(DOWNLOAD_PATH, name+ '.png')
    if r.status_code == 200:
        with open(f_path, 'wb') as f:
            for chunk in r.iter_content(256):
                f.write(chunk)
        return name+ '.png'
    return None


def create_row(imagen):
    # obtener sugerencia de imagen
    im = get_correccion_object(imagen)
    if im is None:
        im = get_sugerencia_object(imagen)
    else:
        im.clasificacion = im.clasificacion_correcta
    if im is None:
        return None
    # descargar imagen
    studyuid = im.imagen.studyUID()
    seriesuid = im.imagen.seriesUID()
    objectuid = im.imagen.objectUID
    durl = generate_download_url(studyuid, seriesuid, objectuid)
    f_path = download_img(durl, objectuid)
    if f_path is None:
        return None
    return [f_path, im.clasificacion.id]

imagenes = Imagen.objects.all()
rows = []
val_rows = []
row = None
for imagen in imagenes:
    row = create_row(imagen)
    if row is not None:
        if random.uniform(0,1)>VAL_RAT:
            rows.append(row)
        else:
            val_rows.append(row)

with open(CSV_PATH, 'wb') as csvf:
    csvw = csv.writer(csvf)
    csvw.writerows(rows)

with open(VAL_CSV_PATH, 'wb') as csvf:
    csvw = csv.writer(csvf)
    csvw.writerows(val_rows)