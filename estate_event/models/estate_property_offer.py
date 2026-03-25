from odoo import models, api, fields
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _inherit = 'estate.property.offer'

    allowed_partner_ids = fields.Many2many(
        'res.partner',
        compute="_compute_allowed_partner_ids"
    )

    partner_id = fields.Many2one(
        "res.partner",
        domain="[('id', 'in', allowed_partner_ids)]"
    )

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            property_record = self.env['estate.property'].browse(vals.get('property_id'))

            if not property_record.event_id:
                raise UserError("No event linked to this property.")

            attendee = self.env['event.registration'].search([
                ('event_id', '=', property_record.event_id.id),
                ('state', '=', 'done')
            ], limit=1)

            if not attendee:
                raise UserError("Buyer must attend the event before making an offer.")

        return super().create(vals_list)

    def _compute_allowed_partner_ids(self):
        for record in self:
            if not record.property_id.event_id:
                record.allowed_partner_ids = False
                continue
            attended = self.env['event.registration'].search([
                ('event_id', '=', record.property_id.event_id.id),
                ('state', '=', 'done'),
            ])

            record.allowed_partner_ids = attended.mapped('partner_id')
