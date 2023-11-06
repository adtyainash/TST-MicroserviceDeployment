# FASTAPI imports
from fastapi import FastAPI, Request, File, UploadFile, Depends, APIRouter
from pydantic import BaseModel
import json
import os
from typing import Optional  # Import Optional for the FileType field

# Base model
class Options(BaseModel):
    FileName: str
    FileDesc: str = "Upload for demonstration"  # Use valid string syntax
    FileType: Optional[str]

# router definition
app = FastAPI()
router = APIRouter()
image_id_counter = 0
filename = "data.json"
filedata = []
try:
    with open(filename, "r") as read_file:
        filedata = json.load(read_file)
except FileNotFoundError:
    # Handle the case where the file doesn't exist yet
    pass

#------------------------------- GET ----------------------------------
@router.get('/')
async def get_all_media():
    return filedata

@router.get('/{option_FileName}')
async def get_Media(option_FileName : str):
    media_found = False
    for media_iterate in filedata: 
        if media_iterate['FileName'] == option_FileName:
            media_found = True
            return media_iterate
    if not media_found: 
        return "Media tidak ditemukan!"


#------------------------------- POST ----------------------------------

# Using an asynchronous POST method for communication
@router.post("/acceptdata")
async def get_data(request: Request, options: Options):
    # Waits for the request and converts it into JSON
    result = await request.json()

    # Prints result in the cmd – for verification purposes
    print(result)
    filedata.append(result)

    # Write the combined data back to the JSON file
    with open(filename, "w") as write_file:
        json.dump(filedata, write_file, indent=4)
    return result

#Upload a file and return filename as response
@router.post("/uploadfile")
async def create_upload_file(data: UploadFile = File(...)):
#Prints result in cmd – verification purpose
    global image_id_counter
    image_id_counter += 1
    image_id = image_id_counter
    filename = data.filename

    image_info = {
        "image_id": image_id,
        "filename": filename,
    }
    media_data = []
    if os.path.isfile("media.json"):
        with open("media.json", "r") as read_file:
            media_data = json.load(read_file)

    # Add the new image information to the media_data list
    media_data.append(image_info)

    # Write the combined data back to "media.json"
    with open("media.json", "w") as write_file:
        json.dump(media_data, write_file, indent=4)

    # Return the filename and image_id in the response
    return {"filename": filename, "image_id": image_id}

#Accept request as data and file
@router.post("/uploadandacceptfile")
async def upload_accept_file(options: Options = Depends(),data: UploadFile = File(...)):
    data_options = options.dict()
    result = "Uploaded Filename: {}. JSON Payload {}".format(data.filename,data_options)


#-------------------------- UPDATE -----------------------------

@router.put('/update_desc')
async def update_Media_Desc(media: Options):
    media_dict = media.dict()
    media_found = False
    for media_iterate in filedata:
        if media_iterate['FileName'] == media.FileName:
            media_iterate['FileDesc'] = media.FileDesc
            media_found = True
            break

    if media_found:
        # Write the updated data back to the JSON file
        with open(filename, "w") as write_file:
            json.dump(filedata, write_file, indent=4)
        return "Berhasil mengupdate data!"
    else:
        return "Media tidak ditemukan!"


#---------------------------------- DELETE ---------------------------------
@router.delete("/{FileName}")
async def delete_media(FileName: str):
    media_found=False
    deleted_media = None

    # Find and remove the media with the specified FileName
    for media in filedata:
        if media['FileName'] == FileName:
            media_found = True
            deleted_media = media
            filedata.remove(media)
            break

    if media_found:
        # Write the updated data back to the JSON file
        with open(filename, "w") as write_file:
            json.dump(filedata, write_file, indent=4)
        return {"message": "Media deleted", "deleted_media": deleted_media}
    else:
        return {"message": "Media not found"}

app.include_router(router)