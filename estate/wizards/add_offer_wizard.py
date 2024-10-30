from odoo import fields, models


class AddOfferWizard(models.TransientModel):
    _name = 'add.offer.wizard'
    _description = 'Add Offer Wizard'

    price = fields.Float(string="Offer Price", required=True)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], string="Offer Status", default='pending', required=True)
    partner_id = fields.Many2one('res.partner', string="Buyer", required=True)

    def action_make_offer(self):
        property_active_ids = self.env.context['active_ids']
        properties = self.env['estate.property'].browse(property_active_ids)
        for property in properties:
            self.env['estate.property.offer'].create({
                'property_id': property.id,
                'price': self.price,
                'status': self.status,
                'partner_id': self.partner_id.id,
            })
            property.state = 'offer_received'
        return {'type': 'ir.actions.act_window_close'}
