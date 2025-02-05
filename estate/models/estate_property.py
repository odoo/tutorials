from dateutil.relativedelta import relativedelta

from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char("Property Name", required=True, help="Property Name")
    description = fields.Char()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Datetime.today() + relativedelta(days=90))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer("Garden Area(sqm)")
    garden_orientation = fields.Selection(
        string = "Garden Orientation",
        selection = [
            ("north", "North"), 
            ("south", "South"), 
            ("east", "East"), 
            ("west", "West")
        ]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        default="new", copy=False, string="State",
        selection = [
            ("new", "New"), 
            ("offer_recieved", "Offer Recieved"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled")
        ]
    )
    property_type_id = fields.Many2one(string="Property Type", comodel_name="estate.property.type")
