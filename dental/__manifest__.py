{
    "name": "Dental",
    "version": "1.1",
    "license": "LGPL-3",
    "category": "Health",
    "summary": "Track properties",
    "description": "",
    "installable": True,
    "application": True,
    "depends" : ["base_setup", "mail", "website", "account", "portal"],
    "data": [
        "security/ir.model.access.csv",
        "views/dental_patients_views.xml",
        "views/dental_medical_aids_views.xml",
        "views/dental_chronic_conditions_views.xml",
        "views/dental_medication_views.xml",
        "views/dental_allergies_views.xml",
        "views/dental_habits_views.xml",
        "views/dental_patient_history_views.xml",
        "views/dental_patient_web_templates.xml",
        "views/dental_portal_template.xml",
        "views/dental_menus.xml",
    ]
}
