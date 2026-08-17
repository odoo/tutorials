{
    "name": "Realest Estate",
    "version": "1.0",
    "summary": "Manage housing properties",
    "category": "Marketing",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        # currently directly loaded in the db <no demo data>
        # "demo/estate_property_demo.xml",
        "demo/estate.property.csv",
        "views/estate_property_view.xml",
        # root
        "views/estate_property_root.xml",
    ],
    "demo": [],
    "application": True,
    "installable": True,
    "license": "LGPL-3",
    "author": "Smit Patel",
}
