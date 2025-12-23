import base64

class IconUtils:

    @staticmethod
    def get_icon(icon_name):
        # Convert your local image to base64
        with open(f'./assets/icons/{icon_name}', "rb") as f:
            icon_bytes = f.read()
        icon_b64 = base64.b64encode(icon_bytes).decode()
        icon = f'data:image/jpeg;base64,{icon_b64}'
        return icon 
    

    