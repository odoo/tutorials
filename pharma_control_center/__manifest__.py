{
    'name': 'Pharma Control Center',
    'version': '1.0',
    'summary': 'Pharmacy Dashboard, Medicines, Inventory & Operations',
    'sequence': 10,
    'description': """
Pharma Control Center
=====================
Central system for pharmacy operations:
- Medicine catalog with batch, expiry, price, stock
- Dashboard showing total medicines and stock value
- Role‑based access (Patient, Doctor, Manager)
    """,
    'category': 'Healthcare/Pharmacy',
    'author': "Muhammad Qasim Shabbir AI developer.",
    'website': 'https://www.odoo.com/app/invoicing',
    'depends': [
        'base_setup',
        'product',
        'account',
        'sale',
    ],
    'data': [
        'security/groups.xml',
        'security/pharmacy_security.xml',
        'security/pharmacy_patient_security.xml',
        'security/sale_order_security.xml',
        'security/ir.model.access.csv',
        'data/demo_patients.xml',
        'data/demo_medicines.xml',
        'views/pharma_control_center_views.xml',   # root menu defined here
        'views/pharmacy_medicine_views.xml',
        'views/pharmacy_patient_views.xml',        # now includes the menuitem
        'views/pharmacy_category_views.xml',
        'views/pharmacy_order_views.xml',
        'views/pharmacy_cart_views.xml',
        'views/sales_report_views.xml',
        'views/manager_analytics_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
