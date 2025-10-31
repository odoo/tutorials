from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = "res.users"

    average_quantity = fields.Boolean(default=True)
    average_time = fields.Boolean(default=True)
    nb_new_orders = fields.Boolean(default=True)
    nb_cancelled_orders = fields.Boolean(default=True)
    total_amount = fields.Boolean(default=True)
    orders_by_size = fields.Boolean(default=True)

    @api.model
    def get_dashboard_config(self):
        user = self.env.user
        return {
            'average_quantity': user.average_quantity,
            'average_time': user.average_time,
            'nb_new_orders': user.nb_new_orders,
            'nb_cancelled_orders': user.nb_cancelled_orders,
            'total_amount': user.total_amount,
            'orders_by_size': user.orders_by_size,
        }

    @api.model
    def set_dashboard_config(self, config):
        user = self.env.user
        user.write(config)
        return True
