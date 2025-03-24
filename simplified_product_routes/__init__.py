from . import models


def _update_existing_products(env):
    """ This is hook is used to updates routes on all existing product templates
        after the module is installed.
    """
    product_templates = env['product.template'].search([])
    for product_template in product_templates:
        product_template._update_routes_based_on_config()
