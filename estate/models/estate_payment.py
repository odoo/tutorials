from odoo import api, fields, models


class EstatePropertyPayment(models.Model):
    _name = "estate.property.payment"
    _description = "Property Payment"

    booking_id = fields.Many2one("estate.property.booking", "Booking", required=True, readonly=True)
    amount = fields.Float("Amount", required=True)
    state = fields.Selection([('draft', 'Draft'), ('paid', 'Paid')], default='draft')

    def action_confirm(self):
        self.ensure_one()
        self.state = 'paid'
        self.booking_id.state = 'paid'
        self.booking_id.property_id.state = 'sold'
        
        property = self.booking_id.property_id
        message_body = f"Congratulations {property.buyer_id.name}! Your full payment has been received and the property {property.name} is officially yours."
        property.message_post(
            body=message_body,
            subject=f"Property {property.name} Sold!",
            partner_ids=[property.buyer_id.id]
        )
