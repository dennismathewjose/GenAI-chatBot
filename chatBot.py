import json
import asyncio
import aiohttp

# Load the JSON data
with open("./resume.json", "r") as file:
    resume_data = json.load(file)

conversation_history = []
# Function to construct the prompt based on user query and JSON data
def construct_prompt(user_query, resume_data):
    # Extract relevant sections from the JSON based on the user query
    context = ""
    if "education" in user_query.lower():
        context += "Education:\n"
        for edu in resume_data["education"]:
            context += f"- {edu['degree']} from {edu['institution']}, Graduation: {edu['graduation_date']}\n"
            context += f"  Relevant Courses: {', '.join(edu['relevant_courses'])}\n"
    
    if "experience" or "work" in user_query.lower():
        print("code is in experience section")
        context += "Professional Experience:\n"
        for exp in resume_data["professional_experience"]:
            context += f"- {exp['position']} at {exp['company']}, {exp['duration']}\n"
            context += f"  Responsibilities: {', '.join(exp['responsibilities'])}\n"
    
    if "skills" in user_query.lower():
        context += "Technical Skills:\n"
        for category, skills in resume_data["technical_skills"].items():
            context += f"- {category}: {', '.join(skills)}\n"
    
    if "projects" or "project" in user_query.lower():
        context += "Academic Projects:\n"
        for project in resume_data["academic_projects"]:
            context += f"- {project['title']} at {project['institution']}, {project['duration']}\n"
            context += f"  Description: {', '.join(project['description'])}\n"

    # Add conversation history
    if conversation_history:
        context += "\nConversation History:\n"
        for i, (query, response) in enumerate(conversation_history, 1):
            context += f"{i}. User: {query}\n   Bot: {response}\n"
    
    # Combine the context with the user query
    prompt = f"Based on the following information:\n{context}\nProvide a concise and accurate response for: {user_query} as first peson's view"
    return prompt

# Function to interact with the LLaMA model
async def ask_llama(user_query):
    # Construct the prompt
    prompt = construct_prompt(user_query, resume_data)
    
    # Send the prompt to the LLaMA model
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": "llama3.2:3b",
                "prompt": prompt,
                "stream": False
            }
        ) as response:
            result = await response.json()
            return result["response"]

# Example usage
async def chat():
    print("welcome to my personal chatBot. \nIf you don't want to go through the entire portfolio, \nASK ME!! Type 'exit' to quit")
    while True:
        user_query = input("\nYou: ")
        if user_query.lower() == 'exit':
            print("See you later. The bot is exiting\n")
            break
        else:
            bot_response = await ask_llama(user_query)
            print(f"Dennis : {bot_response}")
        
        conversation_history.append((user_query,bot_response))

# Run the async function
asyncio.run(chat())