import taipy.gui.builder as tgb
import pandas as pd
from ui.dignitary_modal import render_ddp_dialog
from backend.db_supabase import fetch_all_guests

# ---------------------------------------------------------
# 1. INITIALIZATION & STATE VARIABLES
# ---------------------------------------------------------

# Fetch the raw data once on load
base_guest_dataframe = fetch_all_guests()

# Fallback in case the database is empty or connection fails
if base_guest_dataframe.empty:
    base_guest_dataframe = pd.DataFrame(columns=[
        "id", "name", "category", "speaker_category", "poc", 
        "assigned_gre", "housing", "arrival_time", "airport_pickup_sent"
    ])

# The dataframe bound to the UI table (this one changes when filtered)
guest_dataframe = base_guest_dataframe.copy()

# Filter State Variables
search_name = ""
selected_pocs = []
selected_categories = []
selected_alerts = []

# Dropdown Options (Extracted dynamically from the database)
# We drop NA values and convert to a list for the Taipy selector
poc_options = base_guest_dataframe["poc"].dropna().unique().tolist()
category_options = base_guest_dataframe["category"].dropna().unique().tolist()
alert_options = ["Needs GRE", "Needs Housing", "Needs Airport Pickup"]

# KPI State Variables
kpi_total = len(guest_dataframe)
kpi_unassigned_gre = 0
kpi_speakers = 0
kpi_category_breakdown = "No data"

# ---------------------------------------------------------
# 2. FILTERING LOGIC (CALLBACKS)
# ---------------------------------------------------------

def apply_filters(state):
    """Slices the in-memory dataframe based on user selections and updates KPIs."""
    df = state.base_guest_dataframe.copy()
    
    # 1. Name Search Filter
    if state.search_name:
        df = df[df["name"].str.contains(state.search_name, case=False, na=False)]
        
    # 2. POC Filter (Multi-select)
    if state.selected_pocs:
        df = df[df["poc"].isin(state.selected_pocs)]
        
    # 3. Category Filter (Multi-select)
    if state.selected_categories:
        df = df[df["category"].isin(state.selected_categories)]
        
    # 4. Alerts Filter (Multi-select)
    if state.selected_alerts:
        if "Needs GRE" in state.selected_alerts:
            df = df[df["assigned_gre"].isna() | (df["assigned_gre"] == "")]
        if "Needs Housing" in state.selected_alerts:
            df = df[df["housing"].str.lower() == "tbd"]
        if "Needs Airport Pickup" in state.selected_alerts:
            # Assuming arrival_time is populated but pickup is 0
            df = df[(df["arrival_time"].notna()) & (df["airport_pickup_sent"] == 0)]
            
    # Update the UI table
    state.guest_dataframe = df
    
    # Update KPIs dynamically based on the newly filtered dataframe
    state.kpi_total = len(df)
    state.kpi_unassigned_gre = len(df[df["assigned_gre"].isna() | (df["assigned_gre"] == "")])
    
    # Handle safe string checking for speakers
    speaker_mask = df["speaker_category"].astype(str).str.lower().str.contains("speaker", na=False)
    state.kpi_speakers = len(df[speaker_mask])
    
    # Generate dynamic category breakdown string (e.g., "Bollywood: 3 | VIP: 5")
    counts = df["category"].value_counts()
    if not counts.empty:
        state.kpi_category_breakdown = " | ".join([f"{k}: {v}" for k, v in counts.items()])
    else:
        state.kpi_category_breakdown = "None"

def reset_filters(state):
    """Clears all search fields and restores the full dataset."""
    state.search_name = ""
    state.selected_pocs = []
    state.selected_categories = []
    state.selected_alerts = []
    apply_filters(state)

# Trigger apply_filters whenever any filter state variable changes
def on_change(state, var_name, var_value):
    if var_name in ["search_name", "selected_pocs", "selected_categories", "selected_alerts"]:
        apply_filters(state)

# ---------------------------------------------------------
# 3. UI LAYOUT
# ---------------------------------------------------------

with tgb.Page() as dashboard_page:
    
    # --- KPI QUICK STATS ROW ---
    with tgb.layout("1 1 1 3", class_name="kpi-container"):
        with tgb.part(class_name="kpi-card"):
            tgb.text("Total in View", class_name="kpi-title")
            tgb.text("{kpi_total}", class_name="kpi-value")
            
        with tgb.part(class_name="kpi-card"):
            tgb.text("Unassigned GREs", class_name="kpi-title")
            tgb.text("{kpi_unassigned_gre}", class_name="kpi-value error-text")
            
        with tgb.part(class_name="kpi-card"):
            tgb.text("Speakers", class_name="kpi-title")
            tgb.text("{kpi_speakers}", class_name="kpi-value")
            
        with tgb.part(class_name="kpi-card"):
            tgb.text("Category Breakdown", class_name="kpi-title")
            tgb.text("{kpi_category_breakdown}", class_name="kpi-value-small")
            
    tgb.html("hr") # Visual separator

    # --- MAIN DASHBOARD LAYOUT ---
    with tgb.layout("1 4"): 
        
        # Left Sidebar: Batch Actions
        with tgb.part(class_name="action-sidebar"):
            tgb.text("### Actions", mode="md")
            tgb.button("Import .CSV Roster", class_name="fullwidth plain")
            tgb.button("Export .CSV", class_name="fullwidth plain")
            tgb.button("Assign GRE to Selected", class_name="fullwidth")
            
        # Main Visual Space: Search, Filters, and Roster
        with tgb.part():
            # Filter Control Bar
            with tgb.layout("2 2 2 2 1"):
                tgb.input("{search_name}", label="Search Name...", class_name="fullwidth")
                tgb.selector("{selected_pocs}", lov="{poc_options}", multiple=True, dropdown=True, label="Filter by POC")
                tgb.selector("{selected_categories}", lov="{category_options}", multiple=True, dropdown=True, label="Filter by Category")
                tgb.selector("{selected_alerts}", lov="{alert_options}", multiple=True, dropdown=True, label="Operational Alerts")
                tgb.button("Clear All", on_action=reset_filters, class_name="plain fullwidth")
            
            # The Data Table
            tgb.table("{guest_dataframe}", 
                      columns=["name", "category", "poc", "assigned_gre", "housing"],
                      filter=False, # We disable Taipy's built-in column filters since we built custom global ones
                      class_name="grid-table", 
                      on_action="open_guest_details")
            
    # Mount the DDP dialogue
    render_ddp_dialog()
