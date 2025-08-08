{
    "name": "Library",
    "description": "Manage a library",
    "sequence": 1,
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/library_book_views.xml",
        "views/library_book_tag_views.xml",
        "views/library_book_rent_views.xml",
        "views/library_book_member_views.xml",
        "views/library_menus.xml",
    ],
    "application": True,
    "installable": True,
    "license": "LGPL-3",
}
