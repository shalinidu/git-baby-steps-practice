#!/usr/bin/env pwsh
# DIAL connectivity smoke test.
#
# NOTE: this calls gpt-4o directly with no Jira/project context attached —
# it is not connected to our real Jira data in any way. The model has no
# tool access or retrieval, so its answer to the prompt below will be a
# generic/hallucinated example, not real issues from this project.

if (-not $env:DIAL_API_KEY) {
    Write-Error "DIAL_API_KEY environment variable is not set. Run: `$env:DIAL_API_KEY = 'dial-...'"
    exit 1
}

$headers = @{
    "api-key" = $env:DIAL_API_KEY
}

$body = @{
    messages    = @(
        @{
            role    = "user"
            content = "Give me the list of issues with issue id and title"
        }
    )
    temperature = 0.2
    max_tokens  = 500
} | ConvertTo-Json -Depth 5

$response = Invoke-RestMethod `
    -Uri "https://ai-proxy.lab.epam.com/openai/deployments/gpt-4o/chat/completions" `
    -Method Post `
    -ContentType "application/json" `
    -Headers $headers `
    -Body $body

$response.choices[0].message.content
