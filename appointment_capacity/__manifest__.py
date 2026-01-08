{
    'name': "Appointment Capacity",
    'summary': "change the capacity of the appointment based on the user and resource",
    'description':"capacity of the appointment is change base on the type of the appointment",
    'author':"sujal asodariya",
    'version':"1.0",
    'depends':[
        "appointment",
        "website",
        "calendar",
        "account_auto_transfer",
    ],
    'data':[
        'views/appointment_template_views.xml',
        'views/appointment_type_views.xml',
    ],
    'installable':True,
    'application':True,
    'license':"LGPL-3",
}
