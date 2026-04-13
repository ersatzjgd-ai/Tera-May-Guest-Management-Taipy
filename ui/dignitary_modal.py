import taipy.gui.builder as tgb

def render_ddp_dialog():
    with tgb.dialog("{show_ddp}", title="Dignitary Details", width="50vw"):
        tgb.text("## {selected_guest.name}", mode="md")
        
        with tgb.layout("1 1"):
            # Left Column: Guest Profile
            with tgb.part():
                tgb.text("**Category:** {selected_guest.category}", mode="md")
                tgb.text("**Speaker Type:** {selected_guest.speaker_category}", mode="md")
                tgb.text("**Accompanying Persons:** {selected_guest.accompanying_persons}", mode="md")
            
            # Right Column: Logistics & Assignment
            with tgb.part():
                tgb.text("**Assigned GRE:** {selected_guest.assigned_gre}", mode="md")
                tgb.text("**Arrival Time:** {selected_guest.arrival_time}", mode="md")
                tgb.text("**Location:** {selected_guest.stay_location}", mode="md")
                tgb.text("**Admin Owner:** {selected_guest.admin_owner}", mode="md")
                
        # Action buttons
        tgb.button("Update Profile")
        tgb.button("Close", on_action=lambda state: state.assign("show_ddp", False))
