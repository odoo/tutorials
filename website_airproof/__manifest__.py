{
    'name': 'Airproof Theme',
    'description': 'Airproof Theme - Drones, modelling, camera',
    'category': 'Website/Theme',
    # 'version': '18.0.1.0',
    'author': 'PSBE Designers',
    'license': 'LGPL-3',
    'depends': ['website_sale', 'website_sale_wishlist', 'website_blog', 'website_mass_mailing'],
    'data': [
        # Options
        'data/presets.xml',
        # Menu
        'data/menu.xml',
        # Shapes
        'data/shapes.xml',
        # Pages
        'data/pages/home.xml',
        'data/pages/contact.xml',
        # Frontend
        'views/website_templates.xml',
        'views/website_sale_templates.xml',
        'views/website_sale_wishlist_templates.xml',
        # Snippets
        'views/snippets/options.xml',
        'views/snippets/s_airproof_carousel.xml',
        # Images
        'data/images.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            'website_airproof/static/src/scss/primary_variables.scss',
        ],
        'web._assets_frontend_helpers': [
            ('prepend', 'website_airproof/static/src/scss/bootstrap_overridden.scss'),
        ],
        'web.assets_frontend': [
            # SCSS
            'website_airproof/static/src/scss/components/mouse_follower.scss',
            'website_airproof/static/src/scss/layout/header.scss',
            'website_airproof/static/src/scss/pages/product_page.scss',
            'website_airproof/static/src/scss/pages/shop.scss',
            'website_airproof/static/src/scss/snippets/caroussel.scss',
            'website_airproof/static/src/scss/snippets/newsletter.scss',
            'website_airproof/static/src/snippets/s_airproof_carousel/000.scss',
            # JS
            'website_airproof/static/src/js/mouse_follower.js',
        ],
    },
}
