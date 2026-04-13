from taipy.gui import Gui
from ui.dashboard import dashboard_page

# Global state variables needed across the app
search_query = ""
show_ddp = False
selected_guest = {}

# Routing
pages = {
    "/": "<|toggle|theme|>\n<center>\n# Guest Management Portal\n</center>",
    "dashboard": dashboard_page
}

if __name__ == "__main__":
    gui = Gui(pages=pages)
    
    # Applying the core brand identity
    stylekit = {
        "color_primary": "rgb(247, 97, 10)",
        "border_radius": "8px"
    }
    
    # Load custom CSS and run
    gui.run(title="Event Guest Database", 
            margin="2em", 
            stylekit=stylekit, 
            css_file="assets/style.css")
