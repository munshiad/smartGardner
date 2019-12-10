import subprocess
import pymongo
import gridfs
import datetime

def capture_image():
    # try:

    # take picture
    filename = subprocess.check_output(["./camera.sh"], universal_newlines=True)
    print(filename)  # should be image.jpg

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

    # retrieve what was just stored.
    outputdata = fs.get(stored).read()

    # create an output file and store the image in the output file
    outfilename = "puppy2.jpg"
    output = open(outfilename, "wb")

    output.write(outputdata)
    # close the output file
    output.close()

    # except Exception as e:
    #     print(e)