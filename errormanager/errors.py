import os
from models.location import Location
from models.device import Device
from validate_email import validate_email


def validateToken(token):
	deviceModel = Device()
	device = deviceModel.getDevice({'token': token})
	if device is None:
		raise ValueError("This is an invalid token.")
	data = dict()
	data['device'] = device
	return data

def checkEmail(email):
	if not validate_email(email):
		raise ValueError("This is an invalid email")
	return email

def imageName(imagename):
	workingdir = os.getcwd()
	imagepath = os.path.join(workingdir,'images',imagename)
	if not os.path.isfile(imagepath):
		raise ValueError("Image name is not correct")
	return imagename

def descriptionValidate(description):
	if len(description) > 120:
		raise ValueError("Description is too long")
	return description

def locationValidate(lat_lng):
	lat = lat_lng.split(',')[0].strip()
	lng = lat_lng.split(',')[1].strip()
	locationModel = Location()
	inlocation = locationModel.getLocationFromPosition({'lat':lat, 'lng':lng})
	print inlocation
	# Now allowing posts from all location
	# if inlocation is None:
	# 	raise ValueError("This is an invalid location.")
	if inlocation is None:
		inlocation = dict()
		inlocation['id'] = 0
	data = dict()
	data['lat_lng'] = lat_lng
	data['data'] = inlocation
	return data