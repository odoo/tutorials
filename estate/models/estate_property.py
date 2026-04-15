from odoo import fields, models, api
from odoo.exceptions import ValidationError


class EstateProperty(models.Model):

    _name = 'estate.property'
    _description = "A real estate model with many fields"
    active = fields.Boolean(string="Active", default="Active")
    bedrooms = fields.Integer(string="Bedrooms", default="2")
    date_availability = fields.Datetime(
        string="Available From", copy=False, default=lambda self: fields.Date.add(fields.Date.context_today(self), months=3))
    description = fields.Text(string="Description")
    expected_price = fields.Float(string="Expected Price", required=True)
    facades = fields.Integer(string="Facades")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Float(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Direction",
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West")
        ],
        help="Type is used to specify the garden orientation"
    )
    garage = fields.Boolean(string="Garage")
    living_area = fields.Float(string="Living Area (sqm)")
    name = fields.Char(string="Title", required=True, default="Unknown")
    postcode = fields.Char(string="Postcode")
    selling_price = fields.Float(
        string="Selling Price", readonly=True, copy=False)
    state = fields.Selection([('new', "New"),
                              ('offer_received', "Offer Received"),
                              ('offer_accepted', "Offer Accepted"),
                              ('sold', "Sold"),
                              ('cancelled', "Cancelled")
                              ],
                             default='new')

    @api.constrains('expected_price')
    def _check_price(self):
        for rec in self:
            if rec.expected_price <= 0:
                raise ValidationError("Price must be positive")  # Shown in UI
