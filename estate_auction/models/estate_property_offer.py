from odoo import fields, models, api
from odoo.exceptions import UserError
from odoo.addons.estate.models.estate_property_offer import estate_Property_Offer


class estate_property_offer(models.Model):
    _inherit = "estate.property.offer"

    from_auction = fields.Boolean(compute="_compute_from_auction", readonly=True)

    def _compute_from_auction(self):
        for record in self:
            if record.property_id.selling_type == "auction":
                record.from_auction = True
            else:
                record.from_auction = False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = self.env['estate.property'].browse(vals['property_id'])
            if property_id.selling_type == 'auction':
                if property_id.auction_state == 'blocked':
                    property_id.status = "offer_received"
                    return super(estate_Property_Offer, self.with_context(skip_intermediate_create=True)).create(vals_list)
                else:
                    raise UserError("The auction is not started yet.")
            else:
                return super().create(vals_list)
