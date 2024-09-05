{
    'name': 'Dental',
    'version': '1.0',
    'summary': 'Manage dental history and appointments',
    'description': 'Module to manage medical history and appointments',
    'author': 'Akya',
    'sequence': '15',
    'depends': ['base', 'mail', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/dental_patient_view.xml',
        'views/dental_medication_view.xml',
        'views/dental_chronic_diseases_view.xml',
        'views/dental_allergies_view.xml',
        'views/dental_habits_view.xml',
        'views/dental_medical_aid_view.xml',
        'views/dental_history_view.xml',
        'views/dental_menus.xml',
        'report/dental_patient_report.xml',
        'report/dental_patient_report_template.xml'
        ],
    'installable': True,
    'application': True,
    'license': 'AGPL-3'
}
