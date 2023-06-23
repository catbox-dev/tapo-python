# Description: This script is used to test the tapo-rest API and the OpenAI API.
#              It uses the tapo-rest API to set the color of a smart bulb and
#              the OpenAI API to generate a response to a prompt, based on the
#              GPT-3 model. The prompt is a text that describes an alert scenario
#              and asks the user to assign a color to the alert based on the
#              impact on the system or network. The response is a JSON object
#              that contains the alert, the color assigned, and a short feedback
#              of the alert's impact and the color choice. The response is then
#              parsed and the color is set to the smart bulb using the tapo-rest
#              API. The alert is also read out loud using the macOS text-to-speech
#              engine. The script is meant to be used as a proof-of-concept for
#              the research paper "Using GPT-3 to Automate Cybersecurity Tasks".

# Import libraries
import subprocess
import json
import random
import openai

# JSON file containing the configuration data
with open("config.json") as f:
    data = json.load(f)

# Get the device name, model, port, and OpenAI API key from the config file
device_name = data["devices"][0]["name"]
model = data["devices"][0]["device_type"].lower()
port = data["devices"][0]["port"]
openai.api_key = data["account"]["openai_token"]

# Get the session ID from the tapo-rest API
response = subprocess.run(
    ["curl", "-i", "-X", "POST", "-H", "Content-Type: application/json", "--data", '{ "password": "potatoes" }',
     "http://localhost:" + port + "/login"], capture_output=True, text=True)
session_id = response.stdout.splitlines()[-1]


# Function to generate a random alert
def random_alerts():
    alerts = [
        "Critical security breach detected. Immediate action required!",
        "System overload detected. Performance degradation may occur.",
        "Unauthorized access attempt detected. Please investigate.",
        "Potential data corruption detected. Verify data integrity.",
        "Error: Database connection lost. Data may be unavailable.",
        "Warning: High CPU usage detected. Optimize system resources.",
        "Attention: Insufficient disk space remaining. Clean up storage.",
        "Network connectivity issue detected. Check network configuration.",
        "Error: Application crashed unexpectedly. Restart required.",
        "Possible intrusion attempt detected. Enhance security measures.",
        "All system components are functioning properly. No issues to report.",
        "System is running smoothly. No abnormalities detected.",
        "Currently experiencing a minor network slowdown. No impact on system performance.",
        "Testing new feature. System functionality unaffected.",
        "System maintenance in progress. No service disruptions expected."
    ]

    return random.choice(alerts)


# List of colors
colorsList = ["CoolWhite", "Daylight", "Ivory", "WarmWhite", "Incandescent", "Candlelight", "Snow", "GhostWhite",
              "AliceBlue", "LightGoldenrod", "LemonChiffon", "AntiqueWhite", "Gold", "Peru", "Chocolate", "SandyBrown",
              "Coral", "Pumpkin", "Tomato", "Vermilion", "OrangeRed", "Pink", "Crimson", "DarkRed", "HotPink",
              "Smitten", "MediumPurple", "BlueViolet", "Indigo", "LightSkyBlue", "CornflowerBlue", "Ultramarine",
              "DeepSkyBlue", "Azure", "NavyBlue", "LightTurquoise", "Aquamarine", "Turquoise", "LightGreen", "Lime",
              "ForestGreen"]

# Prompt to be sent to the OpenAI API
prompt = (f"Please assess the potential impact of each alert on the system or network and assign a color from the "
          f"following list representing the impact on a scale from red to green: {colorsList}. "
          "Consider the severity, magnitude, and consequences of each alert when assigning the color. A red color "
          "indicates high impact and potential critical issues, while a green color suggests low impact or no "
          "significant disruptions. In the response you have to add the following but with your responses and all "
          "have to be inside quotes:\n\n\n"
          f'("Alert": "{random_alerts()}",  "Color": [Choose the appropriate color], "Feedback": [Provide a short '
          'feedback of the alert\'s impact and a short feedback of your color choice])')

# Send the prompt to the OpenAI API and get the response
openaiResponse = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0.7,
    max_tokens=100,
    top_p=1.0,
    frequency_penalty=0.5,
    presence_penalty=0.0
)

# Parse the response and get the alert, color, and feedback
openaiAnswer = eval("{" + openaiResponse['choices'][0]['text'][2:][1:-1] + "}")
alert = openaiAnswer["Alert"]
color = openaiAnswer["Color"]
feedback = openaiAnswer["Feedback"]

# Set the color of the smart bulb using the tapo-rest API
subprocess.run(["curl", "-i", "-X", "GET", "-H", f"Authorization: Bearer {session_id}",
                "http://localhost:" + port + "/actions/" + model + "/set-color?color=" + color + "&device=" + device_name])

# Print the alert, color, and feedback
print("\nAlert: " + alert + "\nFeedback: " + feedback + "\nColor set to: " + color + ".\n")

# Uncomment the following line to enable text-to-speech (macOS only)
# subprocess.run(["say", "-v", "Samantha",
#                "Alert: " + alert + ". " + feedback + ". Color set to: " + color + "."])
