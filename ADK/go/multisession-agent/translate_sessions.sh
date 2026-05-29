#!/bin/bash

# Configuration
BASE_URL="http://localhost:8080"
COOKIE="__next_hmr_refresh_hash__=15; argocd.token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcmdvY2QiLCJzdWIiOiJhZG1pbjpsb2dpbiIsImV4cCI6MTc3ODIwNDA1NSwibmJmIjoxNzc4MTE3NjU1LCJpYXQiOjE3NzgxMTc2NTUsImp0aSI6IjNhYjBkZGJhLTQwMmQtNGQ4ZS05MTkxLWE3ZWRjYjUxOTJkNyJ9.DaW3xyvsANQd4JW62JXC3RhfEXYBSVMSK4JZCrDiSVA"
MOCK_TEXT="Robert Frost is one of the most famous poets from the 1900s. He never earned a formal college degree, but he did receive honorary degrees from more than 40 colleges and universities. This famous poem shows that everything in life is cyclical and that the beauty in nature only lasts for a short period of time. Even though life ends, there is new life waiting to come forth."

# 10 different languages - one for each session
LANGUAGES=("Spanish" "French" "German" "Italian" "Portuguese" "Russian" "Japanese" "Chinese" "Arabic" "Hindi")

# Common headers
COMMON_HEADERS=(
  "-H" "Accept: application/json, text/plain, */*"
  "-H" "Cookie: $COOKIE"
  "-H" "Referer: http://localhost:8080/ui/?app=orchestrator_agent"
  "-H" "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36 Edg/148.0.0.0"
)

echo "Creating 10 sessions, each translating to a different language..."

# Array to store session IDs
SESSION_IDS=()

# Create 10 sessions, each with one translation request
for i in {0..9}; do  # 0-indexed for array access
  SESSION_NUM=$((i + 1))
  LANGUAGE=${LANGUAGES[$i]}
  
  echo "Creating session $SESSION_NUM/10 for $LANGUAGE translation..."
  
  # Create session
  SESSION_RESPONSE=$(curl -s -X POST "${BASE_URL}/api/apps/orchestrator_agent/users/user/sessions" \
    "${COMMON_HEADERS[@]}" \
    "-H" "Content-Type: application/json" \
    "-H" "Origin: http://localhost:8080" \
    "-H" "Sec-Fetch-Dest: empty" \
    "-H" "Sec-Fetch-Mode: cors" \
    "-H" "Sec-Fetch-Site: same-origin" \
    "-H" "sec-ch-ua: \"Chromium\";v=\"148\", \"Microsoft Edge\";v=\"148\", \"Not/A)Brand\";v=\"99\"" \
    "-H" "sec-ch-ua-mobile: ?0" \
    "-H" "sec-ch-ua-platform: \"macOS\"" \
    --data-raw '{"appName":"orchestrator_agent","userId":"user"}')
  
  # Extract session ID from response
  SESSION_ID=$(echo "$SESSION_RESPONSE" | grep -o '"id":"[^"]*' | cut -d'"' -f4)
  
  if [ -n "$SESSION_ID" ]; then
    SESSION_IDS+=("$SESSION_ID")
    echo "  Created session: $SESSION_ID"
    
    # Send ONE translation request in the assigned language
    echo "  Sending translation request to $LANGUAGE..."
    
    curl -s -X POST "${BASE_URL}/api/run_sse" \
      "${COMMON_HEADERS[@]}" \
      "-H" "Content-Type: application/json" \
      "-H" "Accept: text/event-stream" \
      "-H" "Origin: http://localhost:8080" \
      "-H" "Referer: http://localhost:8080/ui/?app=orchestrator_agent&session=${SESSION_ID}&userId=user" \
      "--data-raw" "{\"appName\":\"orchestrator_agent\",\"userId\":\"user\",\"sessionId\":\"${SESSION_ID}\",\"newMessage\":{\"role\":\"user\",\"parts\":[{\"text\":\"SHOW ONLY THE TRANSLATION Please translate the following text to ${LANGUAGE}: \\\"${MOCK_TEXT}\\\"\"}]},\"streaming\":false,\"stateDelta\":null}"
    
    echo "  Completed translation request for session $SESSION_ID ($LANGUAGE)"
  else
    echo "  Failed to create session $SESSION_NUM"
    echo "  Response: $SESSION_RESPONSE"
  fi
  
  # Delay between session creations
  sleep 2
done

echo ""
echo "Summary:"
echo "Created ${#SESSION_IDS[@]} sessions:"
for i in "${!SESSION_IDS[@]}"; do
  echo "  - ${SESSION_IDS[$i]} -> ${LANGUAGES[$i]}"
done