from odoo import _, fields, models, api
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.fields import Command


class EstateProperty(models.Model):

    _inherit = 'estate.property'

    def action_property_sold(self):
        pass

        # if not self.env['account.move'].check_access_rights('create'):
        #     try:
        #         self.check_access_rights('write')
        #         self.check_access_rule('write')
        #     except AccessError:
        #         return self.env['account.move']

        # values = []
        # for rec in self:

        #     values.append({
        #         'name': 'a invoice has been generated',
        #         'move_type': 'out_invoice',
        #         'partner_id': rec.buyer_id.id,
        #         "invoice_line_ids": [
        #             Command.create({
        #                 "product_id": rec.id,
        #                 "quantity": 1,
        #                 "price_unit": rec.selling_price,
        #             }),]
        #     })

        #     if not values:
        #         raise UserError("Nothing to invoice.")

        # moves = self.env['account.move'].sudo().create(values)
        # return super().action_property_sold
