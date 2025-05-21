{
    "name": "Real Estate",
    "summary": "Test Module",
    "version": "18.0.0.0.0",
    "license": "OEEL-1",
    "depends": ["base"],
    "data": [
        # Security
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        # Views
        "views/estate_property_views.xml",
        "views/estate_menus.xml",
    ],
    "demo": [
        "demo/demo.xml",
    ],
}
