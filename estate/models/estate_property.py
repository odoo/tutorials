from odoo import fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property"

    name = fields.Char('Name', required=True, translate=True)
    description = fields.Text('Description', translate=True)
    postcode = fields.Char('Postcode', translate=True)
    date_availability = fields.Date('Availability')
    expected_price = fields.Float('Expected price', required=True)
    selling_price = fields.Float('Selling price', readonly=True)
    bedrooms = fields.Integer('Bedrooms', required=True, default=2)
    living_area = fields.Integer('Living Areas', required=True)
    facades = fields.Integer('Facades', required=True)
    garage = fields.Boolean('Has a garage')
    garden = fields.Boolean('Has a garden')
    garden_area = fields.Integer('m² of garden area')
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('east', 'East'), ('west', 'West'), ('south', 'South')],
        help="Orientation is used to tell which way the garden is, relative to the house"
    )

    # Reserved Fields
    active = fields.Boolean()
    state = fields.Selection(
        string='Status',
        selection=[('new', 'New'), ('received', 'Offer received'), ('accepted', 'Offer accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        default='new'
    )

    # Foreign keys
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)

