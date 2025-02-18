from odoo import models, fields, api
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError,ValidationError
from odoo.tools.float_utils import float_compare 


class EstateProperty(models.Model):
    _name = "public.property"
    _description = "Estate related data"
    _inherit = ['mail.thread']
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        "Available From",
        default=lambda self: (datetime.today() + relativedelta(month=3)).date(),
        copy=False,
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [("north", "North"), ("east", "East"), ("west", "West"), ("south", "South")]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ("new", "New"),
            (
                "offer_received",
                "Offer Received",
            ),
            (
                "offer_accepted",
                "Offer Accepted",
            ),
            (
                "sold",
                "Sold",
            ),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        copy=False,
        tracking=True
    )
    property_type_id = fields.Many2one("public.property.type", string="Property type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson = fields.Many2one(
        "res.users", string="Sales Person", default=lambda self: self.env.user
    )
    tags_ids = fields.Many2many("public.property.tag", string="Tags")
    offer_ids = fields.One2many("public.property.offer", "property_id")
    total_area = fields.Float(compute="_compute_total")
    best_price = fields.Float(compute="_compute_best_price")
    company_id = fields.Many2one('res.company',required=True,string="Comapany",default = lambda self : self.env.user.company_id)
    property_image=fields.Image()
    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "The expected price must be positive.",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price > 0)",
            "The selling price must be positive.",
        ),
    ]

    rounding_precision = 0.0001 

    @api.constrains("selling_price")
    def _check_selling_price(self):
        for record in self:
            if (float_compare(record.expected_price * 0.9,record.selling_price,precision_rounding=self.rounding_precision)>= 0):
                raise ValidationError(
                    "The selling price cannot be less than the 90% of expected price"
                )
            record.state="offer_received"

    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = self.living_area + self.garden_area
       
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
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

    def action_sold(self):
        for record in self:
            accepted_offers=self.env['public.property.offer'].search([('property_id','=',record.id)])
            if len(accepted_offers) == 0 : 
                raise ValidationError("Accept at least one offer")
            if len(self.offer_ids) == 0 : 
                raise ValidationError("At least one valid offer needed")
            record.state = "sold"
        if self.state == "cancelled":
            raise UserError("A cancelled property cannot be sold")

    def action_cancelled(self):
        if self.state == "sold":
            raise UserError("A sold property cannot be cancelled")
        for record in self:
            record.state = "cancelled"

    @api.ondelete(at_uninstall = False) 
    def _unlink_public_property_offer(self): 
        for record in self : 
            if record.state not in ('new' , 'cancelled') : 
                raise UserError("A property cannot be deleted in this stage")

    def _track_state(self, init_values):
        self.ensure_one()
        if 'state' in init_values and self.state == 'confirmed':
            return self.env.ref('estate.mt_state_change')
        return super(EstateProperty, self)._track_state(init_values)
