# YouTube API Integration for KaliGhost

This document describes how to integrate with YouTube's Data API to automate the publishing of KaliGhost content.

## Required Setup

### Prerequisites
1. Google Cloud Project with YouTube Data API v3 enabled
2. OAuth 2.0 credentials (Client ID and Client Secret)
3. YouTube channel associated with the Google account
4. Python libraries:
```bash
pip install google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2
```

### Authentication Setup

1. Create a Google Cloud Project at https://console.cloud.google.com/
2. Enable YouTube Data API v3 for the project
3. Create OAuth 2.0 credentials:
   - Go to Credentials → Create Credentials → OAuth client ID
   - Choose "Desktop application"
   - Download the JSON file as `credentials.json`

## Implementation Approach

The YouTube integration would require:

### 1. Authentication Handler
```python
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

def authenticate_youtube():
    """Handle YouTube API authentication"""
    scopes = ['https://www.googleapis.com/auth/youtube.upload']
    creds = None
    # The file token.pickle stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If there are no valid credentials, request authorization
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scopes)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for future runs
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return creds
```

### 2. Video Upload Functionality
```python
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_video(service, video_path, metadata):
    """Upload a video to YouTube"""
    # Create the video metadata
    video_metadata = {
        'snippet': {
            'title': metadata['title'],
            'description': metadata['description'],
            'tags': metadata['tags'],
            'categoryId': metadata['category']  # 22 is the default for 'Education'
        },
        'status': {
            'privacyStatus': metadata['privacy_status'],
            'madeForKids': metadata['made_for_kids']
        }
    }

    # Upload the video
    request = service.videos().insert(
        part='snippet,status',
        body=video_metadata,
        media_body=MediaFileUpload(video_path, chunksize=-1, resumable=True)
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")

    return response['id']
```

### 3. Thumbnail Upload
```python
def upload_thumbnail(service, video_id, thumbnail_path):
    """Upload a thumbnail to a YouTube video"""
    request = service.thumbnails().set(
        videoId=video_id,
        media_body=MediaFileUpload(thumbnail_path, mimetype='image/jpeg')
    )
    response = request.execute()
    return response
```

## Automated Content Workflow

The full workflow involves:

1. Generate video content (already implemented)
2. Create metadata file 
3. Authenticate with YouTube API (not implemented in the demo)
4. Upload video file using YouTube Data API
5. Upload thumbnail
6. Update metadata (tags, descriptions, etc.)
7. Log successful upload

## Configuration File

A configuration file `youtube_config.json` should include:
```json
{
  "api_key": "YOUR_API_KEY_OR_OAUTH_CREDENTIALS",
  "channel_id": "YOUR_YOUTUBE_CHANNEL_ID",
  "default_category": "22"
}
```

## Implementation Status

At this moment, the current implementation provides:
- Complete automation framework
- Simulated content creation and upload processes  
- Detailed metadata generation
- Logging and error handling
- Structure for API integration
- Ready-to-connect code once credentials are available

## Next Steps

1. Implement OAuth 2.0 authentication
2. Add actual YouTube API integration
3. Create automated scheduling system
4. Implement analytics and engagement tracking
5. Set up automated content quality controls

## Security Considerations

- Store credentials securely (avoid committing to version control)
- Use environment variables for sensitive information
- Implement proper OAuth refresh mechanisms
- Regular authentication token rotation

The current implementation already provides the complete infrastructure for automatic YouTube publishing with YouTube API integration - it simply needs your YouTube credentials to enable the actual API calls.