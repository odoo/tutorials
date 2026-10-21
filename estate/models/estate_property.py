from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate properties"

    name = fields.Char("Title", required=True)
    description = fields.Text("Description")
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Available From", copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Has Garage")
    garden = fields.Boolean("Has Garden")
    garden_area = fields.Integer("Garden Area")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[("nord", "Nord"), ("south", "South"), ("east", "East"), ("west", "West")],
    )
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        string="State",
        selection=[("new", "New"), ("received", "Offer Received"), ("accepted", "Offer Accepted"), ("sold", "Sold"), ("cancelled", "Cancelled")],
        required=True,
        copy=False,
        default="new",
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    user_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", inverse_name="property_id", string="Test")
