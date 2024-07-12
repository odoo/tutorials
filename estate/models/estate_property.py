from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"

    name = fields.Char(string="name", required=True)
    description = fields.Char()
    postcode = fields.Char()
    date_availability = fields.Date(string="last available date", copy=False, default=fields.Datetime.now() + relativedelta(months=3))
    expected_price = fields.Float(string="expected price")
    selling_price = fields.Float(string="selling price", readonly=True, copy=False)
    bedroom = fields.Integer(string="no of bedrooms", default=2)
    living_area = fields.Integer(string="living area")
    facades = fields.Integer(string="facades")
    garage = fields.Boolean(string="garage")
    garden = fields.Boolean(string="garden")
    garden_area = fields.Integer(string="garden_area")
    active = fields.Boolean(string="active on window", default=True)
    garden_orientation = fields.Selection(
        string='garden',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    state = fields.Selection(
        string='state',
        selection=[('new', 'New'), ('offer_recieved', 'Offer recieved'), ('offer_accepted', 'Offer accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')], copy=False, default='new'
    )
    property_type_id = fields.Many2one(
        comodel_name="estate.property.type",
        string="Property Type"
    )
    offer_id = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_id",
        string="Property offer"
    )
    users = fields.Char(string='buyer')
    seller_id = fields.Many2one('res.partner', string='seller')
    tag_id = fields.Many2many("estate.property.tag", string="Tags")
    total = fields.Float(compute="_compute_total", string="total")
    count = fields.Float(compute="_compute_best_price", default=0)
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'The expected price of a property can not be negative or zero.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)',
         'The selling price of a property can not be negative.')
    ]

    @api.constrains('expected_price', 'selling_price')
    def check_price(self):
        if float_compare(self.selling_price, 0.9 * self.expected_price, 2) == -1 and not float_is_zero(self.selling_price, 2):
            raise ValidationError('seeling price must greater than 90% of expected price')

    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total = record.living_area + record.garden_area

    @api.depends("offer_id.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_id:
                if record.state == "new":
                    record.state = "offer_recieved"
                record.count = max(record.offer_id.mapped('price'))
            else:
                record.count = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def action_sold_property(self):
        if self.state != "canceled":
            self.state = "sold"
        elif self.state == "canceled":
            raise UserError("This property can't be sold as it is canceled already")
        return True

    def action_cancel_property(self):
        if self.state != "sold":
            self.state = "canceled"
        elif self.state == "sold":
            raise UserError("This property can't be canceled as it is sold already")
        return True

    @api.ondelete(at_uninstall=False)
    def _unlink_property(self):
        for record in self:
            if record.state != 'new' or record.state != 'canceled':
                raise ValidationError("Only New and Canceled Properties can be Deleted.")
