{
    "name": "Estate Manager",
    "version": "1.0",
    "depends": ["base"],
    "application": True,
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_actions.xml",  # moved up to render action button for offers of a prop type
        "views/offer_list_view.xml",
        "views/offer_form_view.xml",
        "views/property_tags_list_view.xml",
        "views/estate_property_type_list_view.xml",
        "views/estate_property_type_form_view.xml",
        "views/estate_property_list_view.xml",
        "views/estate_property_form_view.xml",
        "views/estate_property_search_view.xml",
        "views/estate_menus.xml",
        "views/res_users_views.xml",
        "views/estate_property_kanban_view.xml",
    ],
}
