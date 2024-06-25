from odoo import fields, models


class RealEstateProperty(models.Model):
    _name = 'real.estate.property'
    _description = "Real Estate Property"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    image = fields.Image(string="Image")
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        string="State",
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('under_option', "Under Option"),
            ('sold', "Sold"),
        ],
        required=True,
        default='new',
    )
    type = fields.Selection(
        string="Type",
        selection=[
            ('house', "House"),
            ('apartment', "Apartment"),
            ('office', "Office Building"),
            ('retail', "Retail Space"),
            ('warehouse', "Warehouse"),
        ],
        required=True,
        default='house',
    )
    selling_price = fields.Float(
        string="Selling Price", help="The selling price excluding taxes.", required=True
    )
    availability_date = fields.Date(string="Availability Date")
    floor_area = fields.Integer(
        string="Floor Area", help="The floor area in square meters excluding the garden."
    )
    bedrooms = fields.Integer(string="Number of Bedrooms", default=2)
    has_garage = fields.Boolean(string="Garage")
    has_garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(
        string="Garden Area", help="The garden area excluding the building."
    )
