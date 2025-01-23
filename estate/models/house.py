from odoo import api, models, fields

class house(models.Model):
    _name = 'house'

    name = fields.Char(string='House Name', required=True, default='Unknown')
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self : self.get_availability_date())
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection=[('S', 'South'),
                                           ('N', 'North'),
                                           ('W', 'West'),
                                           ('E', 'East')])
    active = fields.Boolean(default=True)
    state = fields.Selection(string='Status', selection=[
        ('New', 'New'),
        ('Offer Received', 'Offer Received'),
        ('Offer Accepted', 'Offer Accepted'),
        ('Sold', 'Sold'),
        ('Cancelled', 'Cancelled'),
    ], default='New', required=True)
    buyer_id = fields.Many2one('res.users', string='Buyer')
    seller_id = fields.Many2one('res.users', string='Salesperson')
    house_type_id = fields.Many2one('estate.house_type', string='Property Type')
    house_tag_ids = fields.Many2many('estate.house_tag')
    offers_ids = fields.One2many('estate.house_offer', 'property_id')
    total_area = fields.Float(compute='_calculate_total_area')
    
    def get_availability_date(self):
        current_date = fields.Date.today()
        return fields.Date.add(current_date, month=3)
    
    @api.depends("living_area", "garden_area")
    def _calculate_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area