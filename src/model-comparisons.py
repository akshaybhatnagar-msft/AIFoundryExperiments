import os
import json
import time
from typing import List, Dict, Any, Optional
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage

def compare_models(client: AIProjectClient, models: List[str], prompt: str) -> None:
    """Compare responses from different models."""
    messages = [{"role": "user", "content": prompt}]
    
    print(f"Prompt: {prompt}\n")
    print("=" * 80)
    
    for model in models:
        start_time = time.time()
        
        print(f"\nModel: {model}")
        print("-" * 40)
        
        try:
            # Use the client's chat completions API            

            response = client.complete(
                messages=[
                    SystemMessage(content="You are a helpful assistant."),
                    UserMessage(content=prompt)
                ],
                max_tokens=2048,
                temperature=0.8,
                top_p=0.1,
                presence_penalty=0.0,
                frequency_penalty=0.0,
                model=model
            )
            
            if hasattr(response, 'choices') and len(response.choices) > 0:
                content = response.choices[0].message.content
                tokens = getattr(response, 'usage', {})
                
                print(f"Response:\n{content}\n")
                print(f"Completion tokens: {getattr(tokens, 'completion_tokens', 'N/A')}")
                print(f"Prompt tokens: {getattr(tokens, 'prompt_tokens', 'N/A')}")
                print(f"Total tokens: {getattr(tokens, 'total_tokens', 'N/A')}")
            else:
                print("No content in response")
            
            elapsed_time = time.time() - start_time
            print(f"Time elapsed: {elapsed_time:.2f} seconds")
            
        except Exception as e:
            print(f"Error with model {model}: {str(e)}")
        
        print("=" * 80)


def interactive_chat(client: AIProjectClient, model: str) -> None:
    """Run an interactive chat session with a specified model."""
    print(f"\nStarting interactive chat with {model}")
    print("Type 'exit' to end the conversation\n")
    
    messages = []
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            break
        
        messages.append({"role": "user", "content": user_input})
        
        print(f"\n{model}: ", end="", flush=True)
        
        # Stream the response
        try:
            stream_response = client.complete(
                messages=messages,
                max_tokens=2048,
                temperature=0.8,
                top_p=0.1,
                presence_penalty=0.0,
                frequency_penalty=0.0,
                model=model,
                stream=True
            )            
            
            for chunk in stream_response:
                if hasattr(chunk, 'choices') and len(chunk.choices) > 0:
                    content = chunk.choices[0].delta.content
                    if content:
                        print(content, end='', flush=True)
            print()  # New line after streaming is complete
            
            #Get the full response to add to message history
            full_response = client.complete(
                messages=messages,
                max_tokens=2048,
                temperature=0.8,
                top_p=0.1,
                presence_penalty=0.0,
                frequency_penalty=0.0,
                model=model,
                stream=True
            )            
            
            if hasattr(full_response, 'choices') and len(full_response.choices) > 0:
                assistant_message = full_response.choices[0].message.content
                messages.append({"role": "assistant", "content": assistant_message})
                
        except Exception as e:
            print(f"\nError: {str(e)}")


def main():
    # Define models to test
    models = [
        "Deepseek-R1",        
        "Phi-4",
        "gpt-4o",
        "gpt-4o-mini"
    ]
    
    # Create AI Project client with Azure authentication
    endpoint = "https://deephub5971927254.services.ai.azure.com/models"
    project_client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=DefaultAzureCredential(),
        credential_scopes=["https://cognitiveservices.azure.com/.default"],
    )
    
    # Examples to demonstrate
    print("\n" + "=" * 50)
    print("AI FOUNDRY LLM MODELS DEMO")
    print("=" * 50)
    
    while True:
        print("\nOptions:")
        print("1. Compare models on a sample prompt")
        print("2. Interactive chat with a specific model")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == "1":
            prompt = input("\nEnter a prompt to test across all models: ")
            compare_models(project_client, models, prompt)
        
        elif choice == "2":
            print("\nAvailable models:")
            for i, model in enumerate(models, 1):
                print(f"{i}. {model}")
            
            model_choice = input("\nSelect model (1-4): ")
            try:
                model_index = int(model_choice) - 1
                if 0 <= model_index < len(models):
                    interactive_chat(project_client, models[model_index])
                else:
                    print("Invalid model selection")
            except ValueError:
                print("Please enter a valid number")
        
        elif choice == "3":
            print("Exiting demo...")
            break
        
        else:
            print("Invalid choice. Please select 1-3.")


if __name__ == "__main__":
    main()