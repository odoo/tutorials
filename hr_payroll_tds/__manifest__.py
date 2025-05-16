{
    "name": "Payroll/TDS",
    "version": "1.0",
    "author": "Harsh Siddhpara siha",
    "summary": "Add Tax Declaration in contracts menu",
    "depends": ["l10n_in_hr_payroll"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "wizard/hr_tds_declaration_wizard_view.xml",
        "views/hr_tds_declaration_views.xml",
        "views/hr_payroll_menu.xml",
        "views/hr_tds_declaration_details_views.xml",
        "views/hr_tds_report.xml",
        "views/report_tds_declaration_template.xml",
        "data/hr_rule_parameters_data.xml"
    ],
    "installable": True,
    "license": "LGPL-3",
}
