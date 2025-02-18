from odoo import fields, models

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"

    price = fields.Float('Price')
    partner_id = fields.Many2one('res.partner', string='Buyer', copy=False, required=True)
    property_id = fields.Many2one('estate.property', string='Property', copy=False, required=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False,
        default='new',
    )

    def action_set_accepted(self):
        self.write({'state': 'accepted'})

    def action_set_refused(self):
        self.write({'state': 'refused'})
