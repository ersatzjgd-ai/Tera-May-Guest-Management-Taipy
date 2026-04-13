import taipy.gui.builder as tgb
from ui.dignitary_modal import render_ddp_dialog
from backend.db_supabase import fetch_all_guests

# Fetch live data
guest_dataframe = fetch_all_guests() 

with tgb.Page() as dashboard_page:
    with tgb.layout("1 3"): 
        
        # Left Sidebar: Batch Actions
        with tgb.part(class_name="action-sidebar"):
            tgb.text("### Batch Actions", mode="md")
            tgb.button("Import .CSV Roster", class_name="fullwidth plain")
            tgb.button("Export .CSV", class_name="fullwidth plain")
            tgb.button("Assign GRE to Selected", class_name="fullwidth")
            
        # Main Visual Space: Search and Roster
        with tgb.part():
            tgb.text("### Guest Roster", mode="md")
            tgb.input("{search_query}", label="Search Guests by Name, ID, or Category...")
            
            # Table optimized for readability using exact schema columns
            tgb.table("{guest_dataframe}", 
                      columns=["name", "category", "assigned_gre", "housing"],
                      filter=True, 
                      class_name="grid-table", 
                      on_action="open_guest_details")
            
    # Mount the DDP dialogue
    render_ddp_dialog()
