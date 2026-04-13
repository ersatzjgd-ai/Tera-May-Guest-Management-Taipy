event_guest_app/
├── main.py                  # Application entry point & configuration
├── requirements.txt         # Dependencies (taipy, supabase, etc.)
├── assets/
│   └── style.css            # Custom CSS for granular UI control
├── backend/
│   ├── __init__.py
│   └── db_supabase.py       # Supabase client and CRUD operations
├── ui/
│   ├── __init__.py
│   ├── dashboard.py         # Main roster, search, and layout
│   └── dignitary_modal.py   # Expandable details dialogue (DDP)
└── utils/
    ├── __init__.py
    └── data_ops.py          # .CSV processing for bulk imports/exports
