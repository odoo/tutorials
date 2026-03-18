from odoo import models, api
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _inherit = 'estate.property.offer'

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            property_record = self.env['estate.property'].browse(vals.get('property_id'))

            if not property_record.event_id:
                raise UserError("No event linked to this property.")

            if not property_record.buyer_id:
                raise UserError("No buyer set on the property.")

            attendee = self.env['event.registration'].search([
                ('event_id', '=', property_record.event_id.id),
                ('partner_id', '=', property_record.buyer_id.id),
                ('state', '=', 'done')
            ], limit=1)

            if not attendee:
                raise UserError("Buyer must attend the event before making an offer.")

        return super().create(vals_list)