from dateutil.relativedelta import relativedelta
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.tools.translate import _


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "A property managed by the Estate module."
    _order = "id desc"
    sequence = fields.Integer("Sequence", default=1, help="Manual order field")

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda x: fields.Date.today()+relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False, default=0)

    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()

    active = fields.Boolean(default=True)
    #state = fields.Char()

    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area= fields.Integer()
    garden_orientation = fields.Selection(
        selection=[("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")]
    )
    status = fields.Selection(
        selection=[("new", "New"), ("offer_received", "Offer Received"), ("offer_accepted", "Offer Accepted"), ("sold", "Sold"), ("cancelled", "Cancelled") ],
        copy=False,
        default="new",
        required=True
    )

    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    property_type_id = fields.Many2one("estate.property.type")
    property_tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    total_area = fields.Integer(compute="_compute_total_area")

    best_price = fields.Float(compute="_compute_best_price")

    # Do SQL constraints need to be written with single-quotes, as you would in an actual SQL expression? Or are double-quotes always ok?
    _sql_constraints = [
        ("expected_price", "CHECK(expected_price > 0)", "Expected price must be positive." ),
        ("selling_price", "CHECK(selling_price >= 0)", "Can't sell for a negative price!")
    ]

    @api.constrains("selling_price", "expected_price")
    def _price_in_expectations(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2) and float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) < 0:
                raise ValidationError(_("You may not accept an offer for a price inferior to 90%% of expected sale price!"))


    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            lr = record.living_area or 0
            gr = record.garden_area or 0
            record.total_area = lr + gr

    @api.depends("offer_ids.price", "offer_ids.status")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped(lambda x : 0 if x.status == "refused" else x.price), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_cancel(self):
        for record in self:
            if record.status != "sold":
                record.status = "cancelled"
            else:
                raise UserError(_("This property has already been sold!"))
        return True

    def action_is_sold(self):
        for record in self:
            if record.status != "cancelled":
                record.status = "sold"
            else:
                raise UserError(_("This property sale has been cancelled and can no longer be sold."))
        return True

    @api.ondelete(at_uninstall=False)
    def _nodelete_property_with_contents(self):
        if any((prop.status not in ["new", "cancelled"]) for prop in self):
            raise UserError(_("Can't delete a property if its status isn't New or Cancelled!"))
