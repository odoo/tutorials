{
    "name": "Dental",
    "version": "1.0",
    "license": "LGPL-3",
    "summary": "Manage properties",
    "depends": ["base", "mail"],
    "data": [
        "security/ir.model.access.csv",
        "views/pateint_views.xml",
        "views/medical_aids_views.xml",
        "views/chronic_condition.xml",
        "views/habits.xml",
        "views/allergies.xml",
        "views/medication.xml",
        "views/menuitem.xml",
        
        ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
