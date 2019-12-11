import subprocess
import pymongo
import gridfs
import datetime
from bson import ObjectId
def get_picture(stored):
    stored = ObjectId(stored)
    URI = "mongodb://am5113:IoTFabulous!!!@cluster0-shard-00-00-faxh9.mongodb.net:27017,cluster0-shard-00-01-faxh9.mongodb.net:27017,cluster0-shard-00-02-faxh9.mongodb.net:27017/smartGardner?ssl=true&ssl_cert_reqs=CERT_NONE&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority"
    connection = pymongo.MongoClient(URI)
    database = connection.images  # this goes in the images collection

    # create a new gridfs object.
    fs = gridfs.GridFS(database)

    # retrieve what was just stored.
    outputdata = fs.get(stored).read()

    # create an output file and store the image in the output file
    outfilename = "camera/test2.jpg"
    output = open(outfilename, "wb")

    output.write(outputdata)
    # close the output file
    output.close()

    # except Exception as e:
    #     print(e)
#get_picture('5df0182efd10e576b8b5ba19')
#get_picture('5df019d76c33443dbe72aeb2')
get_picture('5df067b0f7dee01bf6ff9dbf')