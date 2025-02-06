from odoo import models, fields

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Propery Model"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string="Available From", default=(fields.Date.add(fields.Date.today() , months=3)), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    is_garage = fields.Boolean()
    is_garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection = [
            ('north', 'North'),
            ('south', 'South'),
            ('west', 'West'),
            ('east', 'East')
         ],
    )
    status = fields.Selection(
        selection=[
            ("new", "New"), 
            ("offer_received", "Offer Received"), 
            ("offer_accepted", "Offer Accepted"), 
            ("sold", "Sold"),
            ("cancelled", "Cancelled")
        ],
        default="new"
    )
    active = fields.Boolean(default=True)