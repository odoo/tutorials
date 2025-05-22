from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Properties"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date("Available from", copy=False, default=fields.Date.add(value=fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('New', 'New'), ('Offer Received', 'Offer Received'), ('Offer Accepted', 'Offer Accepted'), ('Sold', 'Sold'), ('Cancelled', 'Cancelled')
        ], required=True, default='New'
    )

    type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesperson_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for estateProperty in self:
            area = estateProperty.living_area
            if estateProperty.garden:
                area += estateProperty.garden_area
            estateProperty.total_area = area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for estateProperty in self:
            if estateProperty.offer_ids:
                estateProperty.best_price = max(estateProperty.offer_ids.mapped('price'))
            else:
                estateProperty.best_price = 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = None
            self.garden_orientation = None

    def sold_property(self):
        for estateProperty in self:
            if estateProperty.state != "Cancelled":
                estateProperty.state = "Sold"
            else:
                raise UserError("You can't sold a cancelled property !")
        return True

    def cancel_property(self):
        for estateProperty in self:
            if estateProperty.state != "Sold":
                estateProperty.state = "Cancelled"
            else:
                raise UserError("You can't cancel a sold property !")
        return True

    _sql_constraints = [
        ('check_expected_price_positive', 'CHECK(expected_price > 0)',
        'The expected price must be strictly positive'),
        ('check_selling_price_positive', 'CHECK(selling_price >= 0)',
        'The selling price must be positive')
    ]

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price_percentage(self):
        for estateProperty in self:
            if len(list(filter(lambda x: x.status == "Accepted", estateProperty.offer_ids))) > 0 and float_is_zero(estateProperty.selling_price, precision_digits=2):
                raise ValidationError("The selling price cannot be lower than 90% of the expected price")
            if float_is_zero(estateProperty.selling_price, precision_digits=2) or float_is_zero(estateProperty.expected_price, precision_digits=2):
                return True
            if float_compare(estateProperty.selling_price, estateProperty.expected_price * 0.9, precision_digits=2) == -1:
                raise ValidationError("The selling price cannot be lower than 90% of the expected price")

    @api.ondelete(at_uninstall=False)
    def _unlink_property(self):
        for estateProperty_id in self.ids:
            estateProperty = self.env["estate.property"].browse(estateProperty_id)
            if not estateProperty.state in ("New", "Cancelled"):
                raise UserError("You can only delete property in a New or Cancelled state")
