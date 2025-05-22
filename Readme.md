# Google Agent Dev. Kit (ADK) Multi Agent App
This app uses 3 agents. 
1. The Root Agent
2. The Weather Agent. This agent uses the National Weather Service and Google Maps APIs for getting the current weather in a specified location. 

__Note:__ The NWS API only supports USA locations. 

3. The Search Agent. This agent uses Google Search to find current information and information not included in the Models training data. 

### Models
The Weather Agent uses an OpenAI GPT model. The other two Agents use Google Gemini. 

## Follow the instructions below to get it working. 

### Create a Virtual Environment
'''
python -m venv .venv
source .venv/bin/activate
'''

### Install the requirements
```
pip install -r requirements.txt
```
__Note:__ There is another requirements file `requirements-frozen-5-22-25.txt` This has all dependicies frozen as of the date in the file name. If you end up with problems over time, try this one. 

### Env Variables for Google Cloud Project
```
export GOOGLE_CLOUD_PROJECT=agent-dev-kit-dar
export GOOGLE_CLOUD_LOCATION=us-central1 
export GOOGLE_GENAI_USE_VERTEXAI=True
```

### Env Variables for APIS (OpenAI and Google Maps)
You will need to create API keys for OpenAI and Google Maps to use the Weather Agent. 
```
export OPENAI_API_KEY="your-openai-api-key-here"
export GOOGLE_MAPS_API_KEY="your-google-maps-api-key-here"
```

### Env Variables for Cloud Run Deployment
```
export AGENT_PATH="./multi_tool_agent" 
export SERVICE_NAME="multi-tool-agent"
export APP_NAME="multi-tool-agent"
```

### Run the Test Web site locally
```
adk web
```

### Run in Terminal locally
```
adk run multi_tool_agent
```

### Run the API Server locally
```
adk api_server
```

### Start a session (Local Test)
```
curl -X POST http://0.0.0.0:8000/apps/multi_tool_agent/users/u_123/sessions/s_123 \
  -H "Content-Type: application/json" \
  -d '{"state": {"key1": "value1", "key2": 42}}'
```

### Send a message using the run command (Local Test)
```
curl -X POST http://0.0.0.0:8000/run \
-H "Content-Type: application/json" \
-d '{
"app_name": "multi_tool_agent",
"user_id": "u_123",
"session_id": "s_123",
"new_message": {
    "role": "user",
    "parts": [{
    "text": "Hey whats the weather in new york today"
    }]
}
}'
```

### Send a message using the run_sse command (Local Test)
```
curl -X POST http://0.0.0.0:8000/run_sse \
-H "Content-Type: application/json" \
-d '{
"app_name": "multi_tool_agent",
"user_id": "u_123",
"session_id": "s_123",
"new_message": {
    "role": "user",
    "parts": [{
    "text": "Hey whats the weather in new york today"
    }]
}
,
"streaming": true
}'
```
## Deploy to Cloud Run with gcloud
__Note:__ I tried to deploy with the ADK CLI and it didn't work for this Agent

```
gcloud run deploy multi-tool-agent \
--source . \
--region $GOOGLE_CLOUD_LOCATION \
--project $GOOGLE_CLOUD_PROJECT \
--allow-unauthenticated \
--set-env-vars="GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT,GOOGLE_CLOUD_LOCATION=$GOOGLE_CLOUD_LOCATION,GOOGLE_GENAI_USE_VERTEXAI=$GOOGLE_GENAI_USE_VERTEXAI,OPENAI_API_KEY=$OPENAI_API_KEY,GOOGLE_MAPS_API_KEY=$GOOGLE_MAPS_API_KEY"
```

## Test the Cloud Run deployed Agent

### Set varaibles for URL and Auth Token
```
export APP_URL="https://multi-tool-agent-255503383639.us-central1.run.app"
export TOKEN=$(gcloud auth print-identity-token)
```

### See the deployed apps
```
curl -X GET -H "Authorization: Bearer $TOKEN" $APP_URL/list-apps
```

### Start a user session (run_sse command)
```
curl -X POST -H "Authorization: Bearer $TOKEN" \
    $APP_URL/apps/multi_tool_agent/users/doug/sessions/dougs-session \
    -H "Content-Type: application/json" \
    -d '{"state": {"preferred_language": "English", "visit_count": 5}}'
```
### Ask the agent a question
```
curl -X POST -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     "$APP_URL/run_sse" \
     -d @- <<EOF
{
  "app_name": "multi_tool_agent",
  "user_id": "doug",
  "session_id": "dougs-session",
  "new_message": {
    "role": "user",
    "parts": [{
      "text": "What's the weather like in Miami, FL?"
    }]
  },
  "streaming": false
}
EOF
```

### Ask the agent a question (run command)
```
curl -X POST -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     "$APP_URL/run" \
     -d @- <<EOF
{
  "app_name": "multi_tool_agent",
  "user_id": "doug",
  "session_id": "dougs-session",
  "new_message": {
    "role": "user",
    "parts": [{
      "text": "What's the weather like in New York, NY?"
    }]
  },
  "streaming": false
}
EOF
```

### Ask the agent a question (run command)
```
curl -X GET -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     "$APP_URL/hello"
```     
