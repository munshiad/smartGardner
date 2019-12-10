import pymongo
import gridfs

if __name__ == '__main__' :
    # read in the image.
    filename = "puppy.jpg"
    datafile = open(filename, "rb");
    thedata = datafile.read()

    # connect to database

    #connection = pymongo.Connection("localhost", 27017);
    #database = connection['example']
    URI = "mongodb://am5113:IoTFabulous!!!@cluster0-shard-00-00-faxh9.mongodb.net:27017,cluster0-shard-00-01-faxh9.mongodb.net:27017,cluster0-shard-00-02-faxh9.mongodb.net:27017/test?ssl=true&ssl_cert_reqs=CERT_NONE&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority"
    connection = pymongo.MongoClient(URI)
    database = connection.test

    # create a new gridfs object.
    fs = gridfs.GridFS(database)

    # store the data in the database. Returns the id of the file in gridFS
    stored = fs.put(thedata, filename="testimage")

    # retrieve what was just stored.
    outputdata = fs.get(stored).read()

    # create an output file and store the image in the output file
    outfilename = "puppy2.jpg"
    output = open(outfilename, "wb")

    output.write(outputdata)
    # close the output file
    output.close()

    # for experimental code restore to known state and close connection
    # fs.delete(stored)
    # connection.drop_database('example');
    # #    print(connection.database_names())
    # connection.close()