from fastapi import FastAPI, HTTPException, Path
from linkedin_api import Linkedin
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from dotenv import load_dotenv
import os
import uvicorn

load_dotenv()

app = FastAPI()

# Load LinkedIn credentials from environment variables
LINKEDIN_USERNAME = os.getenv("LINKEDIN_USERNAME")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

if not LINKEDIN_USERNAME or not LINKEDIN_PASSWORD:
    raise ValueError("Environment variables LINKEDIN_USERNAME and LINKEDIN_PASSWORD must be set")

# Initialize LinkedIn API
linkedin = Linkedin(LINKEDIN_USERNAME, LINKEDIN_PASSWORD, refresh_cookies=True)

### **Pydantic Models** ###

# Model for search request
class SearchRequest(BaseModel):
    search_string: str = Field(..., description="Search query for LinkedIn profiles")

# Response models
class SearchResult(BaseModel):
    urn_id: str = Field(..., description="URN ID of the LinkedIn user")
    distance: str = Field(..., description="Connection distance (e.g., DISTANCE_1, DISTANCE_2)")
    jobtitle: str = Field(..., description="Current job title of the user")
    location: str = Field(..., description="Location of the user")
    name: str = Field(..., description="Full name of the user")


class SearchResponse(BaseModel):
    results: List[SearchResult] = Field(..., description="List of search results")

# Model for profile picture URLs
class ProfilePictureUrls(BaseModel):
    img_100_100: Optional[str] = Field(None, description="URL for 100x100 profile picture")
    img_200_200: Optional[str] = Field(None, description="URL for 200x200 profile picture")
    img_378_378: Optional[str] = Field(None, description="URL for 378x378 profile picture")
    img_800_800: Optional[str] = Field(None, description="URL for 800x800 profile picture")

class Experience(BaseModel):
    companyName: Optional[str] = Field(None, description="Name of the company")
    title: Optional[str] = Field(None, description="Job title at the company")
    locationName: Optional[str] = Field(None, description="Job location")
    timePeriod: Optional[Dict] = Field(None, description="Time period of the job")
    description: Optional[str] = Field(None, description="Job description, if available")
    geoUrn: Optional[str] = Field(None, description="Geographical URN for the job")
    companyLogoUrl: Optional[str] = Field(None, description="URL for the company logo")

class Education(BaseModel):
    schoolName: Optional[str] = Field(None, description="Name of the school")
    degreeName: Optional[str] = Field(None, description="Name of the degree")
    fieldOfStudy: Optional[str] = Field(None, description="Field of study")
    timePeriod: Optional[Dict] = Field(None, description="Time period of education")
    schoolLogoUrl: Optional[str] = Field(None, description="URL for the school logo")

class ProfileDetailsResponse(BaseModel):
    urn_id: str = Field(..., description="URN ID of the LinkedIn user")
    firstName: str = Field(..., description="First name of the user")
    lastName: str = Field(..., description="Last name of the user")
    headline: Optional[str] = Field(None, description="Professional headline")
    locationName: Optional[str] = Field(None, description="Location of the user")
    summary: Optional[str] = Field(None, description="Profile summary")
    industryName: Optional[str] = Field(None, description="Industry name")
    experience: Optional[List[Experience]] = Field(None, description="List of work experiences")  # Now optional
    education: Optional[List[Education]] = Field(None, description="List of educational qualifications")  # Now optional
    profile_pictures: Optional[ProfilePictureUrls] = Field(None, description="URLs for profile pictures")

class ContactInfo(BaseModel):
    email_address: Optional[str] = Field(None, description="Email address of the user")
    phone_numbers: Optional[List[Dict[str, str]]] = Field(None, description="List of phone numbers")
    twitter_handles: Optional[List[str]] = Field(None, description="List of Twitter handles")
    websites: Optional[List[Dict[str, str]]] = Field(None, description="List of websites")
    address: Optional[str] = Field(None, description="Address of the user")

### **API Endpoints** ###

@app.post("/search-people/", response_model=SearchResponse, summary="Search LinkedIn Profiles", description="Search for LinkedIn profiles using a search string.")
def search_people(request: SearchRequest):
    """Search for people using the LinkedIn search API."""
    try:
        # Perform the LinkedIn search
        search_results = linkedin.search_people(keywords=request.search_string, limit=10)
        
        # Map LinkedIn results to SearchResult objects
        results = [
            SearchResult(
                urn_id=result.get("urn_id", ""),
                distance=result.get("distance", ""),
                jobtitle=result.get("jobtitle", ""),
                location=result.get("location", ""),
                name=result.get("name", "")
            )
            for result in search_results
        ]
        
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/profile-details/{urn_id}", response_model=ProfileDetailsResponse, summary="Get LinkedIn Profile Details", description="Retrieve the full profile details of a LinkedIn user using their URN ID.")
def get_profile_details(urn_id: str):
    """Get full profile details for a specific URN ID."""
    try:
        profile = linkedin.get_profile(urn_id=urn_id)
        
        # Build profile pictures dictionary
        profile_pictures = {
            key: profile['displayPictureUrl'] + profile[key] 
            for key in profile if key.startswith("img_")
        }

        return {
            "urn_id": urn_id,
            "firstName": profile.get("firstName", ""),
            "lastName": profile.get("lastName", ""),
            "headline": profile.get("headline"),
            "locationName": profile.get("locationName"),
            "summary": profile.get("summary"),
            "industryName": profile.get("industryName"),
            "experience": profile.get("experience"),
            "education": profile.get("education"),
            "profile_pictures": profile_pictures or None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/profile-contact-info/{urn_id}", response_model=ContactInfo, summary="Get LinkedIn Profile Contact Info", description="Retrieve the contact information of a LinkedIn user using their URN ID.")
def get_profile_contact_info(urn_id: str):
    """Retrieve the contact information for a LinkedIn profile by URN ID."""
    try:
        contact_info = linkedin.get_profile_contact_info(urn_id=urn_id)
        
        return {
            "email_address": contact_info.get("emailAddress"),
            "phone_numbers": contact_info.get("phoneNumbers", []),
            "twitter_handles": contact_info.get("twitterHandles", []),
            "websites": contact_info.get("websites", []),
            "address": contact_info.get("address"),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Default to 8000 if PORT is not set
    uvicorn.run(app, host="0.0.0.0", port=port)
