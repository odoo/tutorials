from datetime import timedelta
from odoo import api,exceptions,fields, models,_
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _inherit = ['mail.thread']
    _description = "Estate Property"
    _order = "id desc"

    name = fields.Char(required = True, tracking=True)
    image_1920 = fields.Image(store=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy = False,string="Available Form",default = lambda self: fields.Datetime.today() + timedelta(days=90))
    expected_price = fields.Float(required = True)
    selling_price = fields.Float(readonly = True,copy = False, default = 7000000)
    bedrooms = fields.Integer(default = 2)
    living_area = fields.Integer(string="Living area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden area(sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    status = fields.Selection(
        string="Status",
        default = "new",
        copy = False,
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ])
    active = fields.Boolean(default = True)
    property_type_id = fields.Many2one("estate.property.type",string="Property Type", ondelete="restrict")
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', index=True, default=lambda self:self.env.user, copy=False)
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    tags_ids = fields.Many2many("estate.property.tag", string="Tags")
    total_area = fields.Integer(string="Total area (sqm)" ,compute="_compute_total_area", store= True)
    best_price = fields.Float("Best Offer", compute="_compute_best_price", store=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, required=True)
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_cancel(self):
        if self.status == "sold":
            raise UserError("A sold property cannot be cancelled.")
        else:
            self.status = "cancelled"

    def action_sold(self):
        if self.status == "cancelled":
            raise UserError("A cancelled property cannot be sold.")
        if self.status not in ["offer_accepted"]:
            raise exceptions.UserError(("You cannot sell a property that is not in 'Offer Accepted' state"))
        self.status = "sold"

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = (record.living_area or 0) + (record.garden_area or 0)

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0.0)

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0 )','The Expected price must be strictly positive'),
        ('check_selling_price', 'CHECK(selling_price > 0 )','The Selling price must be strictly positive'),
        ]

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_rounding=0.01):
                continue
            min_valid_price = record.expected_price * 0.9
            if float_compare(record.selling_price, min_valid_price, precision_rounding=0.01) == -1:
                  raise ValidationError("The selling price cannot be lower than 90% of the expected price.")

    @api.ondelete(at_uninstall=False)
    def _prevent_delete(self):
        for record in self:
            if record.status not in ['new','cancelled']:
                raise UserError("You can only delete properties in 'New' or 'Cancelled' state.")
