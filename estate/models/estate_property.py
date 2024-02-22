from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property Management"
    _order = "id desc"
    _sql_constraints = [
        ('selling_price_stricly_positive', 'CHECK (selling_price>0)', 'The selling price must be strictly positive.'),
        (
            'expected_price_stricly_positive', 'CHECK (expected_price>0)',
            'The expected price must be strictly positive.'),
    ]

    name = fields.Char(required=True, string="Title")
    user_id = fields.Many2one('res.users', string="Salesperson", index=True, default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    description = fields.Text()
    active = fields.Boolean(default=True)
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.add(fields.Date.today(), months=3),
                                    string="Available from")
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    total_area = fields.Integer(compute='_compute_total_area', string="Total Area (sqm)")
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden orientation",
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ]
    )
    state = fields.Selection(
        string="State",
        selection=[
            ('new', 'New'),
            ('offer', 'Offer Received'),
            ('accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ],
        default='new'
    )
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    tag_ids = fields.Many2many('estate.property.tag', string="Property Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    best_price = fields.Float(compute='_compute_best_price', readonly=True, copy=False, string="Best Offer")



    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for property in self:
            property.best_price = max(property.offer_ids.mapped('price'), default=0.0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for property in self:
            if float_compare(property.selling_price, 0.9 * property.expected_price, precision_digits=2) == -1:
                raise ValidationError("The selling price cannot be lower than 90% of the expected price.")

    @api.ondelete(at_uninstall=False)
    def _unlink_if_not_new_or_canceled(self):
        for property in self:
            if property.state not in ['new', 'canceled']:
                raise UserError("You cannot delete a property that is not new or canceled.")

    def action_set_to_sold(self):
        for property in self:
            if property.state == 'canceled':
                raise UserError("A canceled property cannot be set as sold.")
            property.state = 'sold'
        return True

    def action_set_to_canceled(self):
        for property in self:
            if property.state == 'sold':
                raise UserError("A sold property cannot be canceled.")
            property.state = 'canceled'
        return True
