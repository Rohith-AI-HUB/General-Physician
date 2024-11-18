import speech_recognition as sr
from difflib import get_close_matches

# Dictionary of predefined queries and their solutions
responses = {
    "what is a fever": "A fever is a temporary increase in your body temperature, often due to an illness. You can treat it by resting, staying hydrated, and using medications like paracetamol to reduce the temperature.",
    "what is a headache": "A headache is pain or discomfort in the head or face area. Rest, hydration, and over-the-counter pain relievers like ibuprofen can help.",
    "how to treat a cold": "For a cold, drink plenty of fluids, get sufficient rest, and consider using nasal sprays or steam inhalation for congestion relief.",
    "what are the symptoms of covid": "Common symptoms of COVID-19 include fever, cough, fatigue, and loss of taste or smell. If you suspect an infection, isolate and consult a doctor immediately."
}

def recognize_speech():
    """Recognize speech using the microphone."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... Please speak into the microphone.")
        try:
            # Adjust for ambient noise and listen
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("Recognizing...")
            # Convert speech to text
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()  # Convert to lowercase for easier matching
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

def process_query(query):
    """Analyze the query and return the most relevant solution."""
    if not query:
        return "Sorry, I didn't catch that. Please try again."

    # Find the closest match in the responses dictionary
    closest_matches = get_close_matches(query, responses.keys(), n=1, cutoff=0.4)  # Adjust cutoff for sensitivity
    if closest_matches:
        # If a close match is found, return its corresponding response
        matched_query = closest_matches[0]
        return responses[matched_query]
    else:
        # Default response if no close match is found
        return "I'm sorry, I couldn't find a relevant answer. Please consult a professional."

if __name__ == "__main__":
    print("Welcome to your General Physician AI Assistant!")
    user_query = recognize_speech()
    if user_query:
        response = process_query(user_query)
        print(f"Response: {response}")
    else:
        print("Please try speaking again.")
