from odoo import api ,fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price >= 0)', 'A property expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'A property selling price must be positive.')
    ]
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date("Availability Date", copy=False, default=fields.Datetime.today() + relativedelta(days=90))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )

    active = fields.Boolean(default=True)

    state = fields.Selection(
        string="State",
        default="new",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        copy=False,
    )

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    tags_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    total_area = fields.Integer(compute="_compute_totalArea", store=True)
    @api.depends("living_area", "garden_area")
    def _compute_totalArea(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    best_price = fields.Integer(compute="_compute_bestPrice", store=True)
    @api.depends("offer_ids.price")
    def _compute_bestPrice(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""
    
    def action_property_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("This property is already Cancelled.")
            else:
                record.state = "sold"
        return True

    def action_property_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("This property is already Sold.")
            else:
                record.state = "cancelled"
        return True
      
    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2):
                if float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) == -1:
                    raise ValidationError("Selling price cannot be lower than 90% of the expected price.")