############
# Only add below code in development env.
import importlib
import src.utils.icon_utils as icon_utils_module
import src.utils.ui_utils as ui_utils_module
import src.prompts.prompts as prompts_module

importlib.reload(icon_utils_module)
importlib.reload(ui_utils_module)
importlib.reload(prompts_module)
############

from agents import Agent, Runner, trace, function_tool
from pypdf import PdfReader
from src.prompts.prompts import Prompts
from src.utils.ui_utils import UiUtils

class InformationManager:

    def __init__(self):
        self.name = "Amol Salunke"

        # Read Profile.
        reader = PdfReader("knowledge/Amol_Salunke_Profile.pdf")
        self.profile = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.profile += text

        # Read Summary.
        self.summary = ""
        with open("knowledge/Amol_Salunke_Summary.txt", "r", encoding="utf-8") as f:
            self.summary = f.read()

    @function_tool
    def send_email_tool(to_email_id: str, subject: str, message: str):
        """
        Send out an email to given email id with the given subject and message.
        """

        try:
            UiUtils.send_email(to_email_id, subject, message)
            return {"status": "success", "message": "Email Sent Successfully!!!"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def create_agents(self):
        # Create and configure the AI agent used for chat interactions.
        # The agent is initialized with:
        # - Custom system instructions (prompt)
        # - Optional tools the agent can call (e.g., send email)
        # - Selected LLM model        
        tools = [InformationManager.send_email_tool]

        instructions = Prompts.chat_bot_prompt(self.name, self.summary, self.profile)
        self.chat_bot_agent = Agent(
            name="Ask Amol",
            instructions=instructions,
            tools=tools,
            model="gpt-4o-mini")

    async def chat(self, message, history):
         # Process the user message only if it is not empty
        if message.strip():

            # Convert Gradio chatbot history into OpenAI-style messages
            # Gradio stores content as structured blocks, so we extract
            # plain text from each message before sending it to the agent.
            agent_messages = []
            for msg in history:
                role = msg.get("role")
                content = msg.get("content", "")
                agent_messages.append({"role": role,"content": content})

            # Append the current user message to the conversation
            agent_messages.append({"role": "user","content": message})
            
            # Run the AI agent with the full conversation context
            with trace("Aks Me!"):
                response = await Runner.run(self.chat_bot_agent, agent_messages)

            # Update Gradio chat history with the new user message
            history.append({"role": "user", "content": message})

            # Update Gradio chat history with the assistant response
            history.append({"role": "assistant", "content": response.final_output})

         # Clear input box and return updated chat history
        return "", history
