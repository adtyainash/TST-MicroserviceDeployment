# postmedia.py

from fastapi import APIRouter, Request, File, UploadFile, Depends, HTTPException
from pydantic import BaseModel
import json
import os
from typing import Optional
from pages.hospicall import get_token
import requests

# Base model
class Options(BaseModel):
    FileName: str
    FileDesc: str = "Upload for demonstration"
    FileType: Optional[str]

# Create a new router for the postmedia module
router = APIRouter()
image_id_counter = 0
filename = "data.json"
filedata = []

try:
    with open(filename, "r") as read_file:
        filedata = json.load(read_file)
except FileNotFoundError:
    pass

@router.get('/all')
async def get_all_media():
    return filedata

# Add other GET, POST, PUT, and DELETE routes as needed

# The following functions are just placeholders and need to be updated
@router.post("/acceptdata")
async def get_data(request: Request, options: Options):
    result = await request.json()
    print(result)
    filedata.append(result)

    with open(filename, "w") as write_file:
        json.dump(filedata, write_file, indent=4)
    return result

@router.post("/uploadfile")
async def create_upload_file(data: UploadFile = File(...)):
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

    media_data.append(image_info)

    with open("media.json", "w") as write_file:
        json.dump(media_data, write_file, indent=4)

    return {"filename": filename, "image_id": image_id}

@router.post("/uploadandacceptfile")
async def upload_accept_file(options: Options = Depends(), data: UploadFile = File(...)):
    data_options = options.dict()
    result = "Uploaded Filename: {}. JSON Payload {}".format(data.filename, data_options)

@router.put('/updatedesc')
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


@router.post('/emergencycall')
async def performance_emergency(longitude: float, latitude: float):
    # longitude = 1.2
    # latitude = 1.5
    user_data = {"username": "testvincent", "password": "password"}

    access_token = get_token()
    
    if access_token:
        call_url = "https://hospicall.azurewebsites.net/emergency"  # Update the URL accordingly
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {"longitude": float(longitude), "latitude": float(latitude)}

        response = requests.post(call_url, headers=headers, params=params)

        if response.status_code == 200:
            return {"message": "Call made successfully.", "response": response.json()}
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Failed to make a call. Status code: {response.status_code}"
            )
    else:
        raise HTTPException(
            status_code=401,
            detail="Failed to obtain access token.",
            message=access_token
        )

# Inc  lude additional routes as needed

# Return the router for inclusion in the main script
# This will be included with app.include_router(postmedia.router) in the main script
# You can also create a function to return the router if needed