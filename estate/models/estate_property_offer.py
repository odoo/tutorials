from datetime import timedelta, datetime
from odoo.exceptions import UserError
from odoo import api, fields, models

class EstatePpropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'estate property offer description'
    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'A offer price must be strictly positive.')
    ]
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection(
        [
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        copy=False,
    )

    # offer Many2one relation with res.partner
    partner_id = fields.Many2one(
        'res.partner',
        required=True
    )

    # offer Many2one realtion with property
    property_id = fields.Many2one(
        'estate.property',
        required=True
    )

    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadDeadline", inverse="_inverse_deadDeadline", store=True)

    @api.depends("validity")
    def _compute_deadDeadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + timedelta(days=record.validity)
            else:
                record.date_deadline = datetime.now() + timedelta(days=record.validity)

    def _inverse_deadDeadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_offer_accepted(self):
        for record in self:
            if(record.property_id.buyer_id):
                raise UserError("This Property has already accepted an offer.")
            else:
                record.status='accepted'
                record.property_id.buyer_id=record.partner_id
                record.property_id.selling_price=record.price
        return True

    def action_offer_refused(self):
        for record in self:
            if record.status == 'accepted':
                record.property_id.buyer_id=False
                record.property_id.selling_price=False
            self.status='refused'
        return True

    def group_and_sum_prices(self):
        # Read group method to aggregate the sum of prices grouped by property_id
        result = self.env['estate.property.offer'].read_group(
            [('property_id', '!=', False)],  # Filter: property_id is not empty
            ['property_id', 'price:sum'],    # Group by property_id, sum of price
            ['property_id']                  # Group by field
        )
        
        # Output the result to the terminal for debugging purposes
        print(result)
        print('----------------------------------------------------------------')
        for group in result:
            property_id = group['property_id'][1]  # property_id name
            total_price = group['price']
            print(f"Property: {property_id}, Total Price: {total_price}")
        print('----------------------------------------------------------------')
        return result
