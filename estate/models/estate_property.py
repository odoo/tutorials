from odoo import fields,models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Properties of an estate"
    

    name = fields.Char('Title',required=True, translate=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Date Available', copy=False, default=lambda self:self._get_current_day())
    expected_price = fields.Float('Expected Price',required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms',default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(string='Orientation Type', selection=[('north', 'North'), ('south', 'South'),('west', 'West'), ('east', 'East')])
    active = fields.Boolean(default=True)
    state = fields.Selection(required=True, copy=False, default='New', selection=[('new', 'New'), ('offer_received', 'Offer Received'),('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')])

    property_type_id = fields.Many2one("estate.property.type",string="Property Type")
    salesman_id = fields.Many2one("res.partner", string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.users",string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    def _get_current_day(self):
        return fields.Date.add(fields.Date.today(),months=3)
