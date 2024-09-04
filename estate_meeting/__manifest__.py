{
    "name": "Real Estate Meeting",
    "version": "1.1",
    "license": "LGPL-3",
    "category": "Real Estate",
    "sequence": 15,
    "summary": "Meetings related to real estate module",
    "description": "",
    "installable": True,
    "application": True,
    "depends": ["estate"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/estate_meeting_wizard_view.xml",
        "views/estate_property_views.xml",
    ]
    
}
