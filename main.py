from fastapi import FastAPI, HTTPException
from linkedin_api import Linkedin
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import uvicorn

load_dotenv()

app = FastAPI()

# Load credentials from environment variables
LINKEDIN_USERNAME = os.getenv("LINKEDIN_USERNAME")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

if not LINKEDIN_USERNAME or not LINKEDIN_PASSWORD:
    raise ValueError("Environment variables LINKEDIN_USERNAME and LINKEDIN_PASSWORD must be set")

# Initialize LinkedIn API with credentials from environment variables
linkedin = Linkedin(LINKEDIN_USERNAME, LINKEDIN_PASSWORD, refresh_cookies=True)

class SearchRequest(BaseModel):
    search_string: str

@app.post("/search-people/")
def search_people(request: SearchRequest):
    try:
        # Using search_people with keywords
        results = linkedin.search_people(keywords=request.search_string, limit=10)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/profile/{username}")
def get_profile(username: str):
    try:
        # Retrieve full profile details
        profile = linkedin.get_profile(public_id=username)
        return profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/profile-details/{urn_id}")
def get_profile_details(urn_id: str):
    try:
        # Retrieve profile details using urn_id
        profile = linkedin.get_profile(urn_id=urn_id)
        
        # Extract displayPictureUrl and construct URLs for all image sizes
        profile_pictures = {}
        if "displayPictureUrl" in profile:
            base_url = profile["displayPictureUrl"]
            # Collect all img_xxx_yyy attributes and build their full URLs
            img_keys = [key for key in profile.keys() if key.startswith("img_")]
            for img_key in img_keys:
                profile_pictures[img_key] = base_url + profile[img_key]
        else:
            profile_pictures = None  # Handle case where profile picture is not available

        # Add the profile pictures object to the original profile
        profile["profile_pictures"] = profile_pictures

        return profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Default to 8000 if PORT is not set
    uvicorn.run(app, host="0.0.0.0", port=port)
