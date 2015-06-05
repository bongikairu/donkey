from ctypes import *
from math import *
import StringIO


libhl = cdll.LoadLibrary("/root/donkey/HLLib/libhl.so.2.3.0");

#print libhl

libhl.hlInitialize()

#filename = "/root/donkey/dota2/dota/pak01_dir.vpk"
filename = "/root/donkey/s2d2contents/pak01_dir.vpk"
filemode = 1 + 8 + 32	# read flag + volatile flag

ePackageType = libhl.hlGetPackageTypeFromName(filename);

# 9 = VPK
#print "Package File type"
#print ePackageType

vpk = c_int()

libhl.hlCreatePackage(ePackageType, byref(vpk))

libhl.hlBindPackage(vpk);

openSuccess = libhl.hlPackageOpenFile(filename, filemode)

#print "File open result"
#print openSuccess

if openSuccess==0:
	libhl.hlGetString.restype = c_char_p
	print libhl.hlGetString(3)
	exit()

libhl.hlPackageGetRoot.restype = c_void_p
libhl.hlFolderGetItemByPath.restype = c_void_p

HL_FIND_ALL = 1	# 1 = file only

#print subdata.getvalue()

def app(environ, start_response):
	
	subname = environ["PATH_INFO"][1:]
	
	'''
	data = subname + " not found"
	print "- 404 NOT FOUND"
	start_response("404 NOT FOUND", [
		("Content-Type", "text/plain"),
		("Content-Length", str(len(data)))
	])
	return iter([data])
	'''
	
	#print environ
	
	print environ["REMOTE_ADDR"] + " request " + subname
	
	#print libhl
	
	pItem = libhl.hlFolderGetItemByPath(libhl.hlPackageGetRoot(), subname, HL_FIND_ALL);
	
	#print pItem
	
	if pItem==None:
		#print "item not found"
		data = subname + " not found"
		print "- 404 NOT FOUND"
		start_response("404 NOT FOUND", [
			("Content-Type", "text/plain"),
			("Content-Length", str(len(data)))
#			("Access-Control-Allow-Origin", "http://104.236.208.106")
		])
		return iter([data])
	
	def content():
		
		chunksize = 2048
		csf = float(chunksize)
		
		sSize = c_int()
		libhl.hlItemGetSize(pItem, byref(sSize))
		
		subsize = sSize.value
		
		print "- SIZE: " + str(int(ceil(sSize.value/1024.0))) + " KB"
		
		sent = 0
		chunk = int(ceil(subsize/csf))
		
		#hlBool hlItemGetSize(const HLDirectoryItem *pItem, hlUInt *pSize);
		#hlVoid* hlItemGetData(const HLDirectoryItem *pItem);
		
		#libhl.hlItemGetData.restype = c_void_p
		#sCdata = libhl.hlItemGetData(pItem);
		#subdata = cast(sCdata, POINTER(c_char * subsize))
		
		#for i in range(0,100):
		#	print subdata[i].value
		
		#libhl.hlItemExtract(pItem, "/root/donkey/")
		
		#HLLIB_API hlBool hlFileCreateStream(HLDirectoryItem *pItem, HLStream **pStream);
		#HLLIB_API hlVoid hlFileReleaseStream(HLDirectoryItem *pItem, HLStream *pStream);
		
		stream = c_void_p()
		
		libhl.hlFileCreateStream.argtypes = [c_void_p, POINTER(c_void_p)]
		libhl.hlFileCreateStream(pItem, byref(stream))
		
		libhl.hlStreamOpen(stream, 1)
		
		libhl.hlStreamGetStreamSize(stream);
		
		#output.write('First line.\n')
		
		sCdata = (c_char * chunksize)()
	
		#c = c_char()
		#libhl.hlStreamReadChar(stream, byref(c));
		
		
		
		#print c
		
		tosend = chunksize
		if sent + tosend > subsize:
			tosend = subsize - sent
			
		sent = sent + tosend
		
		for c in range(chunk):
			libhl.hlStreamRead(stream, byref(sCdata), tosend);
			subdata = StringIO.StringIO()
			for i in range(tosend):
				#print sCdata[i]
				subdata.write(sCdata[i])
			yield subdata.getvalue()
		
		print "- DATA SENT"
		
		libhl.hlStreamClose(stream)
	
		libhl.hlFileReleaseStream(pItem, stream);
	
	print "- 200 OK"
	#data = "Hello, World!\n"
	start_response("200 OK", [
		("Content-Type", "application/octet-stream")
		#("Content-Length", str(subsize)),
#		("Access-Control-Allow-Origin", "http://104.236.208.106")
	])
	return content()

#libhl.shutdown()