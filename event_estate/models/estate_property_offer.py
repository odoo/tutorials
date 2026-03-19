from odoo import models, fields, api
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):
    _inherit = 'estate.property.offer'

    allowed_partner_ids = fields.Many2many(
        'res.partner',
        compute="_compute_allowed_partners"
    )
    partner_id = fields.Many2one(
        domain="[('id', 'in', allowed_partner_ids)]"
    )

    def _compute_allowed_partners(self):
        for rec in self:
            registrations = self.env['event.registration']
            if rec.property_id and rec.property_id.event_id:
                registrations = self.env['event.registration'].search([
                    ('event_id', '=', rec.property_id.event_id.id),
                    ('state', '=', 'done')
                ])
            rec.allowed_partner_ids = registrations.mapped('partner_id')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get('property_id')
            partner_id = vals.get('partner_id')
            if property_id and partner_id:
                property_rec = self.env['estate.property'].browse(property_id)
                event = property_rec.event_id
                if not event:
                    raise ValidationError("No open house event found for this property.")
                registration = self.env['event.registration'].search([
                    ('event_id', '=', event.id),
                    ('partner_id', '=', partner_id),
                    ('state', '=', 'done')
                ], limit=1)
                if not registration:
                    raise ValidationError(
                        "Customer must attend the open house event before making an offer."
                    )
        return super().create(vals_list)
