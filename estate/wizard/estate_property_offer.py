from odoo import fields, models, exceptions

class EstatePropertyOffers(models.TransientModel):
    _name = 'estate.property.make.offer'
    _description = 'Estate Property Make Offer'

    price = fields.Float(string="price")
    partner_id = fields.Many2one('res.partner',required=True)
    validity = fields.Integer(string="Validity", default=7)

    def make_an_offer(self):
        active_property_ids = self.env.context.get('active_ids', [])

        for property in self.env['estate.property'].browse(active_property_ids):
            try:
                # Create the offer record
                self.env['estate.property.offer'].create(
                    {
                        'price': self.price,
                        'property_id': property.id,
                        'partner_id': self.partner_id.id,
                        'validity': self.validity
                    }
                )
            except Exception as e:  # Catch all exceptions and log them
                raise exceptions.ValidationError(f"Something went wrong when creating an offer for property {property.id}: {str(e)}")
