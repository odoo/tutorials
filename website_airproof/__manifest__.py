{
    "name": "Airproof Theme",
    "description": "Airproof Theme - Drones, modelling, camera",
    "category": "Website/Theme",
    # "version": "19.0.0.0",
    "author": "PSBE Designers",
    "license": "LGPL-3",
    "depends": ["website_sale", "website_sale_wishlist", "website_blog", "website_mass_mailing"],
    "data": [
        # Snippets
        "views/snippets/options.xml",
        "views/snippets/s_airproof_carousel.xml",
        # Options
        "data/presets.xml",
        "data/website.xml",
        # Menu
        "data/menu.xml",
        # Shapes
        "data/shapes.xml",
        # Pages
        "data/pages/home.xml",
        "data/pages/contact.xml",
        # Frontend
        "views/new_page_template_templates.xml",
        "views/website_templates.xml",
        "views/product_tile_templates.xml",
        "views/website_sale_templates.xml",
        "views/website_sale_wishlist_templates.xml",
        # Images
        "data/images.xml",
    ],
    "assets": {
        "web._assets_primary_variables": [
            "website_airproof/static/src/scss/primary_variables.scss",
        ],
        "web._assets_frontend_helpers": [
            ("prepend", "website_airproof/static/src/scss/bootstrap_overridden.scss"),
        ],
        "web.assets_frontend": [
            # SCSS
            "website_airproof/static/src/scss/base/font.scss",
            "website_airproof/static/src/scss/components/mouse_follower.scss",
            "website_airproof/static/src/scss/components/product_card.scss",
            "website_airproof/static/src/scss/layout/header.scss",
            "website_airproof/static/src/scss/pages/product_page.scss",
            "website_airproof/static/src/scss/pages/shop.scss",
            "website_airproof/static/src/scss/snippets/carousel.scss",
            "website_airproof/static/src/scss/snippets/newsletter.scss",
            "website_airproof/static/src/snippets/s_airproof_carousel/000.scss",
            # JS
            "website_airproof/static/src/js/mouse_follower.js",
        ],
        # Builder Option Plugins
        "website.website_builder_assets": [
            "website_airproof/static/src/website_builder/background_shapes_option_plugin.js",
            "website_airproof/static/src/website_builder/image_shapes_option_plugin.js",
            "website_airproof/static/src/website_builder/color_picker_gradient_tab.js",
            "website_airproof/static/src/website_builder/header_template_option.xml",
            "website_airproof/static/src/website_builder/footer_option_plugin.js",
            "website_airproof/static/src/website_builder/mega_menu_option.xml",
            "website_airproof/static/src/website_builder/airproof_carousel_option.xml",
            "website_airproof/static/src/website_builder/airproof_carousel_option_plugin.js",
        ],
    },
    "new_page_templates": {
        "airproof": {
            "services": ["s_parallax", "s_airproof_key_benefits_h2", "s_call_to_action", "s_airproof_carousel"]
        }
    },
}
