aimport subprocess
import pymongo
import gridfs
import datetime
from bson import ObjectId
import time

i = 1
def capture_image():
    global i
    try:
        # take picture
        filename = subprocess.check_output(["./camera.sh"], universal_newlines=True)
        #print(filename)  # should be camera/image.jpg
        filename = filename.rstrip('\n')

        # read in the image.

        # filename = "puppy.jpg"
        datafile = open(filename, "rb")
        thedata = datafile.read()

        # connect to database

        # connection = pymongo.Connection("localhost", 27017);
        # database = connection['example']
        URI = "mongodb://am5113:IoTFabulous!!!@cluster0-shard-00-00-faxh9.mongodb.net:27017,cluster0-shard-00-01-faxh9.mongodb.net:27017,cluster0-shard-00-02-faxh9.mongodb.net:27017/smartGardner?ssl=true&ssl_cert_reqs=CERT_NONE&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority"
        connection = pymongo.MongoClient(URI)
        database = connection.images  # this goes in the images collection

        # create a new gridfs object.
        fs = gridfs.GridFS(database)

        # store the data in the database. Returns the id of the file in gridFS
        stored = fs.put(thedata, filename=datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))  # ex. '20191209-061959'
        print("[%i]: %s" % (i, str(stored)))
        try:
            subprocess.check_output(["rm", "camera/image.jpg"], universal_newlines=True)
        except:
            pass
        i+=1

    except Exception as e:
        print(e)

while True:
    capture_image()
    time.sleep(120)