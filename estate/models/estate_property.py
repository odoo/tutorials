from odoo import fields, models
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string="Garden Orientation"
    )
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        string="Status",
        required=True,
        copy=False,
        default='new'
    )    
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    seller_id = fields.Many2one("res.users", string="Seller", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

# class EstatePropertyType(models.Model):
#     _name = "estate.property.type"
#     _description = "Property Type"

#     name = fields.Char(required=True)

# class EstatePropertyTag(models.Model):
#     _name = "estate.property.tag"
#     _description = "Real Estate Property Tags"
#     _order = "name"

#     name = fields.Char(required=True, string="Tag")
#     #color = fields.Integer(string="Color")

#     _sql_constraints = [
#         ('unique_tag_name', 'unique(name)', 'Tag name must be unique.')
#     ]
# class EstatePropertyOffer(models.Model):
#     _name = "estate.property.offer"
#     _description = "Estate Property Offer"

#     price = fields.Float(string="Offer Price", required=True)
#     status = fields.Selection([
#         ('accepted', 'Accepted'),
#         ('refused', 'Refused')
#     ], string="Status", copy=False)

#     partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
#     property_id = fields.Many2one("estate.property", string="Property", required=True)

