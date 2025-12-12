#!/bin/bash
# WeatherFlow Weather Station API Probe Commands

echo "WeatherFlow Weather Station API Probe Commands"
echo "=============================================="
echo ""

# Basic curl command for the specific station (72117) with API key
echo "1. Basic probe of WeatherFlow station 72117 (with API key):"
echo "curl -X GET 'https://swd.weatherflow.com/swd/rest/observations/station/72117?api_key=23e0cb90-8a11-4ca5-871e-133ab69c47ae'"
echo ""

# Curl with headers and verbose output
echo "2. Detailed probe with headers and verbose output:"
echo "curl -v -H 'Accept: application/json' -H 'User-Agent: Atlas-Stream-Processing-Probe/1.0' 'https://swd.weatherflow.com/swd/rest/observations/station/72117?api_key=23e0cb90-8a11-4ca5-871e-133ab69c47ae'"
echo ""

# Curl with JSON formatting (requires jq)
echo "3. Formatted JSON output (requires jq):"
echo "curl -s 'https://swd.weatherflow.com/swd/rest/observations/station/72117?api_key=23e0cb90-8a11-4ca5-871e-133ab69c47ae' | jq ."
echo ""

# Curl with timing information
echo "4. Probe with timing information:"
echo "curl -w 'Total time: %{time_total}s\\nResponse code: %{http_code}\\nSize: %{size_download} bytes\\n' -s -o /dev/null 'https://swd.weatherflow.com/swd/rest/observations/station/72117?api_key=23e0cb90-8a11-4ca5-871e-133ab69c47ae'"
echo ""

# Curl to check just headers
echo "5. Check response headers only:"
echo "curl -I 'https://swd.weatherflow.com/swd/rest/observations/station/72117?api_key=23e0cb90-8a11-4ca5-871e-133ab69c47ae'"
echo ""

# Curl with error handling
echo "6. Probe with error handling:"
echo "curl -f -s --connect-timeout 10 --max-time 30 'https://swd.weatherflow.com/swd/rest/observations/station/72117?api_key=23e0cb90-8a11-4ca5-871e-133ab69c47ae' || echo 'ERROR: Failed to connect to WeatherFlow API'"
echo ""

# Test with different station ID (base URL from config)
echo "7. Test base URL structure (will return unauthorized without api_key):"
echo "curl -s 'https://swd.weatherflow.com/swd/rest/observations/station/'"
echo ""

echo "Usage Examples:"
echo "==============="
echo ""
echo "# Quick test:"
echo "curl 'https://swd.weatherflow.com/swd/rest/observations/station/72117?api_key=23e0cb90-8a11-4ca5-871e-133ab69c47ae'"
echo ""
echo "# Save response to file:"
echo "curl 'https://swd.weatherflow.com/swd/rest/observations/station/72117?api_key=23e0cb90-8a11-4ca5-871e-133ab69c47ae' > weather_data.json"
echo ""
echo "# Test connectivity and response time:"
echo "curl -w 'Response: %{http_code}, Time: %{time_total}s\\n' -s -o /dev/null 'https://swd.weatherflow.com/swd/rest/observations/station/72117?api_key=23e0cb90-8a11-4ca5-871e-133ab69c47ae'"
echo ""

echo "API Endpoint Details:"
echo "===================="
echo "Base URL: https://swd.weatherflow.com/swd/rest/observations/station/"
echo "Station ID: 72117"
echo "Full URL: https://swd.weatherflow.com/swd/rest/observations/station/72117"
echo "API Key: 23e0cb90-8a11-4ca5-871e-133ab69c47ae (from config)"
echo ""

echo "Expected Response:"
echo "=================="
echo "The API should return JSON data with weather observations including:"
echo "- Temperature, humidity, pressure"
echo "- Wind speed and direction"  
echo "- Precipitation data"
echo "- Solar radiation"
echo "- Station metadata"
