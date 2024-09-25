from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import _
from odoo.tools.float_utils import float_compare, float_is_zero


# TODO: refactor record into a better name
class Estate(models.Model):
    _name = "estate.property"
    _description = "Estate business object"
    _sql_constraints = [
        ('check_expected_price_positive', 'CHECK (expected_price >= 0)', 'The expected price must be positive.'),
        ('check_selling_price_positive', 'CHECK (selling_price >= 0)', 'The selling price must be positive.')

    ]

    _order = "sequence, name, id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.add(fields.Date.today(), months=3))

    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(default=0)
    garden_orientation = fields.Selection(
        string="Type",
        default=None,
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West")
        ]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="State",
        default="new",
        copy=False,
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled")
        ]
    )

    property_type_id = fields.Many2one("estate.property.type")
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    salesperson_id = fields.Many2one('res.users', default=lambda self: self.env.user)
    estate_property_tag_ids = fields.Many2many(comodel_name="estate.property.tag")
    offer_ids = fields.One2many(comodel_name="estate.property.offer", inverse_name="property_id")

    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Integer(compute="_compute_best_price")

    sequence = fields.Integer(string="Sequence",default=1)

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            if record.garden_area and record.living_area:
                record.total_area = record.garden_area + record.living_area
            else:
                record.total_area = None
            # record.total_area = '%s %s' % (record.garden_area, record.living_area)

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                # mapped: apply the param func on all records in self and return the result as a list of recordset
                record.best_price = max(record.mapped("offer_ids.price"))
            else:
                record.best_price = None

    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = "north"
            else:
                record.garden_area = 0
                record.garden_orientation = None

    def action_sold(self):
        for record in self:
            if record.state == "canceled":
                raise UserError(_("Canceled properties cannot be sold"))
            record.state = "sold"
        return True

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError(_("A sold property cannot be canceled"))
            record.state = "canceled"
        return True

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price_expected_price_threshold(self):
        THRESHOLD = 0.9
        for record in self:
            if not float_is_zero(record.selling_price,precision_rounding=0.01) and float_compare(record.selling_price,record.expected_price * THRESHOLD, precision_rounding=0.01) <= 0:
                raise ValidationError(_(f"The selling price cannot be lower than 90% of the expected price"))

    # we do this instead of overriding unlink because when we unisntall the app there should not be potentials user error thrown
    @api.ondelete(at_uninstall=False)
    def _unlink_if_property_new_or_canceled(self):
        for record in self:
            if record.state == "offer_received" or record.state == "offer_accepted" or record.state == "sold":
                raise UserError(_(f"You cannot delete a property that is not new or canceled"))