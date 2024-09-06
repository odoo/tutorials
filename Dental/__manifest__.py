{
    'name': 'dental',
    'version': '1.0',
    'summary': 'Manage patient billing and treatment notes',
    'description': """
        This module helps in managing patient billing, including treatment notes,
        consultation types, and other related information.
    """,
    'category': 'Sales',
    'author': 'odoo',
    'depends': ['base', 'website', 'mail', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/dental_medical_symptoms_allergies_view.xml',
        'views/dental_medical_symptoms_chronic_conditions_view.xml',
        'views/dental_medical_symptoms_habit_view.xml',
        'views/patients_view.xml',
        'views/templates.xml',
        'views/dental_medical_history_view.xml',
        'views/dental_medication_view.xml',
        'views/dental_medical_aids.xml',
        'views/dental_menu_view.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
