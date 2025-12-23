import os
import gradio as gr
import sendgrid
from typing import Dict
from sendgrid.helpers.mail import Mail, Email, To, Content

class UiUtils:

    @staticmethod
    def load_page(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    
    @staticmethod
    def load_css():
        base_dir = os.path.dirname(os.path.abspath(__file__))
        css_path = os.path.join(base_dir, "..", "..", "assets", "css", "style.css")
        css_path = os.path.normpath(css_path)
        with open(css_path, "r") as f:
            css = f"<style>{f.read()}</style>"
        return gr.HTML(css)

    @staticmethod
    def show_social_toolbar(icons):
        linkedin_icon, twitter_icon, youtube_icon, github_icon, huggingface_icon = icons
        html = f"""
        <div class="left-vertical-toolbar">
            <a href="https://www.linkedin.com/in/amol-salunke/" target="_blank">
                <img src="{linkedin_icon}" class="left-icon">
            </a>

            <a href="https://x.com/salunkecoep" target="_blank">
                <img src="{twitter_icon}" class="left-icon">
            </a>

            <a href="https://www.youtube.com/@amol-salunke-official" target="_blank">
                <img src="{youtube_icon}" class="left-icon">
            </a>

            <a href="https://github.com/amol-salunke" target="_blank">
                <img src="{github_icon}" class="left-icon">
            </a>

            <a href="https://huggingface.co/amolsalunke" target="_blank">
                <img src="{huggingface_icon}" class="left-icon">
            </a>
        </div>
        """

        return gr.HTML(html)  

    @staticmethod
    def show_top_topbar(profile_img_html):
        with gr.Row(elem_classes="topbar", elem_id="fixed-topbar"):

            # Top Left side - profile block
            gr.HTML(f"""
            <div class="topbar-left">
                {profile_img_html}
                AMOL SALUNKE
            </div>
            """)

            with gr.Row(elem_classes="nav-buttons"):
                home_btn = gr.Button("HOME")
                about_btn = gr.Button("ABOUT")
                proj_btn = gr.Button("PROJECTS")
                contact_btn = gr.Button("CONTACT")

        return home_btn, about_btn, proj_btn, contact_btn
    
    @staticmethod
    def show_floating_chat(profile_img_html, infoManager):
        with gr.Row(elem_id="floating-chat") as floating_chat:
            with gr.Column(elem_id="floating-chat-container"):
                
                gr.HTML(f"""
                <div id='floating-chat-header' class="chatbot-top">
                    {profile_img_html} Ask Me
                </div>
                """)
                
                chatbot = gr.Chatbot(elem_id="floating-chat-body",type="messages")
                
                with gr.Row(elem_id="chat-input-row"):
                    msg = gr.Textbox(
                        placeholder="Type a message...",
                        show_label=False,
                        elem_id="custom-chat-input",
                        scale=10
                    )

                    send_btn = gr.Button(
                        "➤",
                        elem_id="custom-send-btn",
                        scale=1
                    )            

                # Send message to LLM on pressing of Enter Key
                msg.submit(infoManager.chat, inputs=[msg, chatbot], outputs=[msg, chatbot])
                
                # Send message to LLM on click on Send Button
                send_btn.click(infoManager.chat, inputs=[msg, chatbot], outputs=[msg, chatbot])        
   
        return floating_chat, chatbot, msg
    
    @staticmethod    
    def toggle_chat(is_open: bool):
        new_state = not bool(is_open)
            
        # Make chat visible when new_state True, otherwise hide
        chat_visibility = gr.update(visible=new_state)
            
        # Update launcher icon
        icon = "👋" if new_state else "💬"
        launcher_update = gr.update(value=icon)
        return new_state, chat_visibility, launcher_update
    
    @staticmethod
    def send_email(to_email:str, subject: str, html_body: str) -> Dict[str, str]:
        """
        Sends an HTML email using the SendGrid service.

        This method retrieves the SendGrid API key from environment variables,
        constructs an email with the given subject and HTML body, and sends it
        to the specified recipient.

        Args:
            to_email (str): Recipient email address.
            subject (str): Subject line of the email.
            html_body (str): HTML content of the email body.

        Returns:
            Dict[str, str]: Status response indicating success.
        """
        # Fetch SendGrid API key from environment variables
        my_api_key = os.getenv("SENDGRID_API_KEY")
        
        # Initialize SendGrid client with the API key
        sg = sendgrid.SendGridAPIClient(api_key=my_api_key)

        # Define sender email address
        from_email = Email("salunkecoep@gmail.com") 

        # Define recipient email address
        to_email = To(to_email)

         # Create HTML content for the email
        content = Content("text/html", html_body)

        # Construct the email payload
        mail = Mail(from_email, to_email, subject, content).get()

        # Send the email via SendGrid API
        sg.client.mail.send.post(request_body=mail)

        # Return success status
        return {"status": "success"}
    
    