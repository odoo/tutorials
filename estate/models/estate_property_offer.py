from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, UserError

class EstatePropertyType(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offers"
    _order = 'price DESC'

    price = fields.Float(required=True)
    status = fields.Selection(
        string="Status",
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Offer by")
    property_id = fields.Many2one("estate.property", string="Property")
    property_name = fields.Char(related='property_id.name', string="Property name")
    property_type_id = fields.Many2one("estate.property.type", related="property_id.property_type_id", store=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_date_deadline", inverse="_inverse_date_deadline")

    _sql_constraints = [
        ('positive_offer_price', 'CHECK(price > 0)', 'Offer price must be strictly positive.'),
    ]

    # date_deadline = {creation date} + {validity} days
    @api.depends("create_date", "validity")
    def _date_deadline(self):
        for record in self:
            # record.create_date is None before the record is created
            startingDate = record.create_date or fields.Date.today()

            record.date_deadline = fields.Date.add(startingDate, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.today()).days


    # actions
    def action_accept_offer(self):
        self.ensure_one()
        self.status = 'accepted'
        if self.property_id.selling_price == 0.0:
            self.property_id.buyer_id = self.partner_id
            self.property_id.selling_price = self.price
        else:
            raise UserError(_('You cannot accept multiple offers at the same time.'))
        return True

    def action_refuse_offer(self):
        self.ensure_one()
        if self.status == 'accepted': # if previously accepted, reset offer values
            self.property_id.selling_price = 0.0
            self.property_id.buyer_id = None
        self.status = 'refused'
        return True
    
    # model crud
    @api.model
    def create(self, vals):
        if vals['property_id']:
            property_record = self.env['estate.property'].browse(vals['property_id'])
            property_record.state = 'offer_received'
            if vals['price'] < property_record.best_price:
                raise ValidationError(_("Cannot create an offer where the offer price is lower than the current best price."))
        return super().create(vals)
    
'''     example 'vals'
    {'state': 'new'
     'name': 'Cat House'
     'tag_ids': []
     'property_type_id': 1
     'postcode': False
     'date_availability': '2024-12-12'
     'expected_price': 0
     'description': False
     'bedrooms': 2
      'living_area': 0
      'facades': 0
      'garage': False
      'garden': False
      'garden_area': 0
      'garden_orientation': False
      'offers_ids': []
       'salesperson_id': 2
       'buyer_id': False}
    '''
