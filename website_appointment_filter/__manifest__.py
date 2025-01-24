{
    "name": "Website Appointments Filter",
    "description": """
    "category": "Services/Appointment/Appointment Filter",
        Allow clients to Filter Appointments on basis of mode of appointment, payment step status and basis of schedule
        """,
    "depends": ["website_appointment", "appointment_account_payment"],
    "data": [
      'views/appointment_filter_templates.xml'
    ],
    "license": "OEEL-1",
    "auto_install": True,
}
