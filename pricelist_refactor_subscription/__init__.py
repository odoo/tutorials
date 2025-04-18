from . import models


def _pre_init_pricelist_refactor_sale_subscription(env):
    env['res.config.settings'].create({
        'group_product_pricelist': True,
    }).execute()
