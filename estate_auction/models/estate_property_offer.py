from odoo import api, fields, models
from odoo.tools import float_compare
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _inherit = "estate.property.offer"

    property_sale_type = fields.Selection(related="property_id.sale_type")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("property_id") and vals.get("price"):
                property = self.env["estate.property"].browse(vals["property_id"])
                if property.sale_type == 'regular':
                    return super().create(vals_list)
                expected_price = property.expected_price
                if float_compare(vals["price"], expected_price, precision_rounding=0.01) < 0:
                    raise UserError("The offer price cannot be less than the expected price of %.2f" % expected_price)
                property.state = 'offer_received'
        return models.Model.create(self, vals_list)
