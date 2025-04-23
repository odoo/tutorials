from odoo import fields, models


class EstatePropertyOfferWizard(models.TransientModel):
    _name = 'estate.property.offer.wizard'
    _description = 'Wizard to add offers to multiple properties'

    price = fields.Float(string="Price")
    status = fields.Selection(
        [
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        string="Offer Status"
    )
    partner_id = fields.Many2one(
        'res.partner',
        string="Buyer",
        required=True,
    )

    def action_make_offer(self):
        """Create offers for selected properties"""
        property_ids = self.env.context.get('active_ids')
        properties = self.env['estate.property'].browse(property_ids)

        for property in properties:
            offer = self.env['estate.property.offer']
            offer.create({
                'price': self.price,
                'partner_id': self.partner_id.id,
                'property_id': property.id,
                'status': self.status
            })
