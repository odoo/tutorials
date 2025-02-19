from odoo import fields, models
from datetime import timedelta


class estatepropertyofferwizard(models.TransientModel):
    _name = 'estate.property.offer.wizard'
    _description = 'Wizard to add offers to estate properties'

    price = fields.Float(required=True)
    buyer_id = fields.Many2one('res.partner', string='Buyer')
    date_deadline = fields.Date("Deadline", default=lambda self: fields.Date.today() + timedelta(days=7))
    property_ids = fields.Many2many('estate.property', string='Properties')

    def action_add_offer(self):
        properties = self.env["estate.property"].browse(self.env.context.get('active_ids', []))
        for estate_property in properties:
            self.env['estate.property.offer'].create({
                'price': self.price,
                'partner_id': self.buyer_id.id,
                'date_deadline': self.date_deadline,
                'property_id': estate_property.id,
            })
        return {'type': 'ir.actions.act_window_close'}