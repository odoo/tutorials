def _payment_term_discount_post_init(env):
    env['account.payment.term'].search([
        ('early_discount', '=', True),
        ('early_payment_discount_ids', '=', False)
    ]).create_early_payment_discount_id()


from . import models
from . import wizard
