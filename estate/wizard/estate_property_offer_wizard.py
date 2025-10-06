from odoo import api, fields, models


class MakeOfferWizard(models.TransientModel):
    _name = 'estate.property.offer.wizard'
    _description = 'Property Offer Wizard'

    offer_price = fields.Float('Offer Price', required=True)
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')],
        string='Status'
    )
    partner_id = fields.Many2one('res.partner', 'Buyer', required=True)
    property_ids = fields.Many2many(
        'estate.property',
        string='Selected Properties',
    )

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        property_ids = self.env.context.get("active_ids", [])
        if property_ids:
            res["property_ids"] = [(6, 0, property_ids)]
        return res

    def action_make_offer(self):
        for property in self.property_ids:
            self.env['estate.property.offer'].create({
                "offer_price": self.offer_price,
                'status': self.status,
                'partner_id': self.partner_id.id,
                'property_id': property.id,
            })
        return {'type': 'ir.actions.act_window_close'}
