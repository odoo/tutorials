from odoo import models, fields, api


class ResConfigSetting(models.TransientModel):
    _inherit = "res.config.settings"

    average_quantity = fields.Boolean(
        string="Average amount of t-shirt", default=True, config_parameter="average_quantity")
    average_time = fields.Boolean(
        string="Average time for order", default=True, config_parameter="average_time")
    nb_new_orders = fields.Boolean(
        string="Number of new orders", default=True, config_parameter="nb_new_orders")
    nb_cancelled_orders = fields.Boolean(
        string="Number of cancelled orders", default=True, config_parameter="nb_cancelled_orders")
    total_amount = fields.Boolean(
        string="Total amount of new orders", default=True, config_parameter="total_amount")
    orders_by_size = fields.Boolean(
        string="Shirts order by size", default=True, config_parameter="orders_by_size")

    @api.model
    def get_values(self):
        res = super().get_values()
        res.update(
            average_quantity=self.env['ir.config_parameter'].sudo(
            ).get_param('awesome_dashboard.average_quantity'),

            average_time=self.env['ir.config_parameter'].sudo(
            ).get_param('awesome_dashboard.average_time'),

            nb_new_orders=self.env['ir.config_parameter'].sudo(
            ).get_param('awesome_dashboard.nb_new_orders'),

            nb_cancelled_orders=self.env['ir.config_parameter'].sudo(
            ).get_param('awesome_dashboard.nb_cancelled_orders'),

            total_amount=self.env['ir.config_parameter'].sudo(
            ).get_param('awesome_dashboard.total_amount'),

            orders_by_size=self.env['ir.config_parameter'].sudo(
            ).get_param('awesome_dashboard.orders_by_size'),
        )
        return res

    @api.model
    def set_values(self):
        super().set_values()
        param = self.env['ir.config_parameter'].sudo()

        average_quantity = self.average_quantity or False
        average_time = self.average_time or False
        nb_new_orders = self.nb_new_orders or False
        nb_cancelled_orders = self.nb_cancelled_orders or False
        total_amount = self.total_amount or False
        orders_by_size = self.orders_by_size or False

        param.set_param('awesome_dashboard.average_quantity', average_quantity)
        param.set_param('awesome_dashboard.average_time', average_time)
        param.set_param('awesome_dashboard.nb_new_orders', nb_new_orders)
        param.set_param('awesome_dashboard.nb_cancelled_orders',
                        nb_cancelled_orders)
        param.set_param('awesome_dashboard.total_amount', total_amount)
        param.set_param('awesome_dashboard.orders_by_size', orders_by_size)
