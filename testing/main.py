# 1. Routing Agent

routing_system_prompt = """You are a Routing Agent. Your role is to assess the user's query and route it to the relevant department. The departments available are:
- Google Maps Scraping Department: Handles tasks related to scraping data from Google Maps.
- Business Idea Generation Department: Generates ideas for businesses based on given contexts or requirements.

Use the route_query tool to forward the user's query to the relevant department. Also, use the speak_to_user tool to get more information from the user if needed."""

routing_tools = [
    {
        "type": "function",
        "function": {
            "name": "route_query",
            "description": "Routes the user query to the relevant department.",
            "parameters": {
                "type": "object",
                "properties": {
                    "department": {
                        "type": "string",
                        "enum": ["Google Maps Scraping", "Business Idea Generation"],
                        "description": "The department to route the query to."
                    },
                    "query": {
                        "type": "string",
                        "description": "The user query to send."
                    }
                },
                "required": ["department", "query"]
            }
        },
        "strict": True
    },
    {
        "type": "function",
        "function": {
            "name": "speak_to_user",
            "description": "Asks the user for more information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "The message to send to the user."
                    }
                },
                "required": ["message"]
            }
        },
        "strict": True
    }
]

# 2. Google Maps Scraping Department

scraping_system_prompt = """You are part of the Google Maps Scraping Department. Your role is to handle tasks related to scraping data from Google Maps. Use the scrape_google_maps tool to perform scraping tasks."""

scraping_tools = [
    {
        "type": "function",
        "function": {
            "name": "scrape_google_maps",
            "description": "Scrapes data from Google Maps based on given parameters.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The location to search in Google Maps."
                    },
                    "business_type": {
                        "type": "string",
                        "description": "The type of business to search for."
                    },
                    "radius": {
                        "type": "integer",
                        "description": "The radius (in meters) to search within."
                    }
                },
                "required": ["location", "business_type", "radius"]
            }
        },
        "strict": True
    }
]

# 3. Business Idea Generation Department

idea_generation_system_prompt = """You are part of the Business Idea Generation Department. Your role is to generate innovative business ideas based on given contexts or requirements. Use the generate_business_idea tool to create ideas, and the query_business_knowledge tool to access relevant information from the RAG system."""

idea_generation_tools = [
    {
        "type": "function",
        "function": {
            "name": "generate_business_idea",
            "description": "Generates a business idea based on given parameters.",
            "parameters": {
                "type": "object",
                "properties": {
                    "industry": {
                        "type": "string",
                        "description": "The industry or sector for the business idea."
                    },
                    "target_audience": {
                        "type": "string",
                        "description": "The target audience or customer base for the business."
                    },
                    "budget": {
                        "type": "string",
                        "description": "The approximate budget range for starting the business."
                    }
                },
                "required": ["industry", "target_audience", "budget"]
            }
        },
        "strict": True
    },
    {
        "type": "function",
        "function": {
            "name": "query_business_knowledge",
            "description": "Queries the RAG system for relevant business information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query to send to the RAG system."
                    }
                },
                "required": ["query"]
            }
        },
        "strict": True
    }
]

# Main execution function

def handle_user_query(user_query):
    # Initialize conversation
    conversation = [{"role": "system", "content": routing_system_prompt}]
    conversation.append({"role": "user", "content": user_query})

    while True:
        response = client.chat.completions.create(
            model="gpt-4-0613",  # Replace with your preferred model
            messages=conversation,
            tools=routing_tools,
            tool_choice="auto"
        )

        assistant_message = response.choices[0].message
        conversation.append(assistant_message)

        if assistant_message.tool_calls:
            for tool_call in assistant_message.tool_calls:
                if tool_call.function.name == "route_query":
                    args = json.loads(tool_call.function.arguments)
                    department = args["department"]
                    query = args["query"]

                    if department == "Google Maps Scraping":
                        result = handle_scraping_department(query)
                    elif department == "Business Idea Generation":
                        result = handle_idea_generation_department(query)
                    
                    conversation.append({"role": "function", "name": tool_call.function.name, "content": result})
                
                elif tool_call.function.name == "speak_to_user":
                    args = json.loads(tool_call.function.arguments)
                    user_response = input(args["message"] + " ")
                    conversation.append({"role": "user", "content": user_response})
        else:
            # If no tool calls, assume the assistant has a final response
            return assistant_message.content

def handle_scraping_department(query):
    # Implement the logic for the Google Maps Scraping Department
    # This would involve using the scrape_google_maps tool and processing the results
    pass

def handle_idea_generation_department(query):
    # Implement the logic for the Business Idea Generation Department
    # This would involve using the generate_business_idea and query_business_knowledge tools
    pass

# Example usage
user_query = "I need ideas for a tech startup in the education sector"
result = handle_user_query(user_query)
print(result)