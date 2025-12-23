#####################################################
# Only add below code in development env.
import importlib
import src.utils.icon_utils as icon_utils_module
import src.utils.ui_utils as ui_utils_module
import src.llms.information_manager as info_module

importlib.reload(icon_utils_module)
importlib.reload(ui_utils_module)
importlib.reload(info_module)
#####################################################

import gradio as gr
from dotenv import load_dotenv
from src.utils.icon_utils import IconUtils
from src.utils.ui_utils import UiUtils
from src.llms.information_manager import InformationManager

# Load environment variables from .env file.
# `override=True` ensures existing environment variables
# are overwritten with values from the .env file if present.
load_dotenv(override=True)

# Create an instance of InformationManager.
# This class handles AI logic, knowledge loading, and agent execution.
infoManager = InformationManager()

# Initialize and configure the AI agent.
# This must be called before the chatbot is used.
infoManager.create_agents()

# Load profile image icon and convert it into HTML.
# This HTML is later reused in the top bar and floating chat UI.
profile_icon = IconUtils.get_icon("Amol.jpg")
profile_img_html = (
    f'<img src="{profile_icon}" '
    f'style="width:45px;height:45px;border-radius:50%;margin-right:10px;">'
)

# Load social media icons.
# These icons are displayed in the left vertical social toolbar.
linkedin_icon = IconUtils.get_icon("linkedin.png")
twitter_icon = IconUtils.get_icon("twitter.png")
youtube_icon = IconUtils.get_icon("youtube.png")
github_icon = IconUtils.get_icon("github.png")
huggingface_icon = IconUtils.get_icon("huggingface.png")

# Create the main Gradio UI container for the application.
# `gr.Blocks` is used to build a custom layout using rows, columns,
# buttons, chat components, and other UI elements.
# The `title` sets the browser tab title for the app.
with gr.Blocks(title="Amol Salunke") as demo:

    # Load and apply custom CSS styles to the Gradio application.
    UiUtils.load_css()
    
    # Display the left vertical social media toolbar.
    # Each icon links to a corresponding social profile.
    UiUtils.show_social_toolbar([
        linkedin_icon,
        twitter_icon,
        youtube_icon,
        github_icon,
        huggingface_icon
    ])

    # Create the top navigation bar with profile image and menu buttons.
    # Returns button references for attaching click events.
    home_btn, about_btn, proj_btn, contact_btn = UiUtils.show_top_topbar(profile_img_html)

    # State variable to track whether the floating chatbot is visible.
    # True = open, False = hidden.
    chat_open_state = gr.State(True)

    # Create the floating chatbot UI.
    # Returns:
    # - floating_chat: chatbot container
    # - chatbot: chat history component
    # - msg: user input textbox
    floating_chat, chatbot, msg = UiUtils.show_floating_chat(profile_img_html, infoManager)

    # Load and display the default Home page content.
    # HTML content is loaded dynamically from file.
    content = gr.HTML(UiUtils.load_page("assets/html/home.html"))

    # Bind top navigation buttons to dynamically load page content.
    home_btn.click(lambda: UiUtils.load_page("assets/html/home.html"), outputs=content)
    about_btn.click(lambda: UiUtils.load_page("assets/html/about.html"), outputs=content)
    proj_btn.click(lambda: UiUtils.load_page("assets/html/projects.html"), outputs=content)
    contact_btn.click(lambda: UiUtils.load_page("assets/html/contact.html"), outputs=content)

    # Create a floating launcher button to open or close the chatbot.
    # The icon changes based on chatbot visibility.
    launcher_btn = gr.Button(value="👋", elem_id="floating-launcher", interactive=True)

    # Bind launcher button click to toggle chatbot visibility.
    # Updates:
    # - chat open/close state
    # - chatbot container visibility
    # - launcher button icon
    launcher_btn.click(UiUtils.toggle_chat, inputs=[chat_open_state], outputs=[chat_open_state, floating_chat, launcher_btn])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0",server_port=7860)

