from odoo import fields, models


class EstatePropertyOffer(models.TransientModel):
    _name = 'estate.property.offer.wizard'
    _inherit = 'estate.property.offer'
    _description = 'Wizard for estate property offers'

    property_id = fields.Many2one('estate.property', string="Property", required=False)

    def action_create_offer(self):
        active_ids = self.env.context.get('active_ids')
        properties = self.env['estate.property'].search([
            ('id', 'in', active_ids)
        ])
        for property in properties:
            self.env['estate.property.offer'].create({
                'price': self.price,
                'property_id': property.id,
                'partner_id': self.partner_id.id
            })
            if property.state == 'new':
                property.state = 'offer_received'
        return True
