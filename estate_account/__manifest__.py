{
    "name": "Real_estate_account",
    "summary": "Track and Generate the invoices for properties.",
    "depends": ["estate", "account"],
    "data": ["security/ir.model.access.csv",
        "estate_account/report/estate_property_templets.xml"
    ],
    "installable": True,
    "application": True,
    "auto_install": True,
    "license": "LGPL-3",
}
