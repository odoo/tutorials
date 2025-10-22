from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=fields.Date.add(fields.Date.today(), months=3), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True,copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden orientation',
        selection=[('North', 'N'), ('South', 'S'),('East', 'E'),('West', 'W')],
        help="Specify the orientation of the garden to know when you're gonna enjoy the sun")
    state = fields.Selection(
        selection=[('New', 'New'), ('Offer Received', 'Offer Received'), ('Offer Accepted', 'Offer Accepted'), ('Sold', 'Sold'), ('Cancelled', 'Cancelled')],
        default='New'
    )
    active = fields.Boolean(default=True)
    salesman = fields.Many2one("res.users")
    buyer = fields.Many2one("res.partner", copy=False)
    tag_ids=fields.Many2many("estate.property.tag", string="Tags")
    offer_ids=fields.One2many("estate.property.offer","property_id")
