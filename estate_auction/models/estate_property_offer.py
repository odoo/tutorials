from odoo import api,fields, models, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class EstatePropertyOfferAuction(models.Model):
    _inherit = 'estate.property.offer'

    property_sale_type = fields.Selection(related="property_id.sale_type")

    @api.model_create_multi
    def create(self, vals_list):
        for record in vals_list:
            property_obj = self.env['estate.property'].browse(record['property_id'])
            if property_obj.sale_type == 'regular':
                return super().create(vals_list)
            if float_compare(record['price'], property_obj.expected_price, precision_digits=6) < 0:
                raise UserError(_("offer price is lower than expected price"))
            property_obj.state = 'offer_received'
        return models.Model.create(self, vals_list)
