from odoo import models, fields


class Estate(models.Model):
    _name = "estate_property"
    _description = "real estate management"
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_available = fields.Date(
        string="Date available",
        copy=False,
        default=fields.Datetime.add(fields.Date.today(), months=3),
    )
    expected_price = fields.Float(string="Expected price", required=True)
    selling_price = fields.Float(string="Selling price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    active = fields.Boolean(string="State", default=True)
    state = fields.Selection(
        string="State",
        selection=[
            ("new", "New"),
            ("offerRecieved", "OfferRecieved"),
            ("offerAccepted", "OfferAccepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        copy=False,
        required=True,
    )
    property_type_id = fields.Many2one(
        comodel_name="estate.property_type", string="Property Type"
    )
    buyer_id = fields.Many2one(comodel_name="res.partner", string="Buyer", copy=False)
    salesman_id = fields.Many2one(
        comodel_name="res.users", string="Salesman", default=lambda self: self.env.user
    )
    property_tag_ids = fields.Many2many(
        comodel_name="estate.property_tag", string="Property Tags"
    )
    offer_ids = fields.One2many(
        comodel_name="estate.property_offer",
        inverse_name="property_id",
        string="Offers",
    )
