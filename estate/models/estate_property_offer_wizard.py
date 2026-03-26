from odoo import _, fields, models
from odoo.exceptions import UserError


class PropertyOfferWizard(models.TransientModel):
    _name = 'estate.property.offer.wizard'
    _description = 'Property Offer Wizard'

    partner_id = fields.Many2one('res.partner', required=True)
    price = fields.Float(required=True)

    def action_apply_offer(self):
        active_ids = self.env.context.get('active_ids', [])
        if not active_ids:
            raise UserError(_("Please select at least one property"))

        properties = self.env['estate.property'].browse(active_ids)

        valid_properties = properties.filtered(
            lambda p: p.state in ['new', 'offer_received'],
        )

        if not valid_properties:
            raise UserError(_("No valid properties (New / Offer Received) selected"))

        for prop in valid_properties:
            self.env['estate.property.offer'].create({
                'property_id': prop.id,
                'partner_id': self.partner_id.id,
                'price': self.price,
            })

            if prop.state == 'new':
                prop.state = 'offer_received'

        return {'type': 'ir.actions.act_window_close'}
