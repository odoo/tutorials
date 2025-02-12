from datetime import datetime, timedelta

from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float(
        string="Price",
        help="The price offered for the property.",
    )

    status = fields.Selection(
        string="Status",
        help="The status of the offer.",
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )

    partner_id = fields.Many2one(
        string="Partner",
        help="The partner who made the offer.",
        required=True,
        comodel_name="res.partner",
    )

    property_id = fields.Many2one(
        string="Property",
        help="The property the offer is for.",
        required=True,
        comodel_name="estate.property",
    )

    validity = fields.Integer(
        string="Validity (days)",
        help="The number of days the offer is valid for.",
        default=7,
    )

    date_deadline = fields.Date(
        string="Deadline",
        help="The date the offer expires.",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    property_type_id = fields.Many2one(
        string="Property Type",
        help="The type of the property.",
        related="property_id.property_type_id"
    )

    # -------------------------------------------------------------------------
    # SQL QUERIES
    # -------------------------------------------------------------------------

    _sql_constraints = [
        ('check_price', 'CHECK(price >= 0)', 'The price must be positive.'),
    ]

    # -------------------------------------------------------------------------
    # COMPUTED FIELDS
    # -------------------------------------------------------------------------

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.create_date = record.create_date or datetime.now().date()
            record.date_deadline = datetime.now().date() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.create_date = record.create_date or datetime.now().date()
            record.validity = (record.date_deadline - datetime.now().date()).days

    # -------------------------------------------------------------------------
    # ONCHANGE METHODS
    # -------------------------------------------------------------------------

    @api.onchange('price')
    def _onchange_price(self):
        if self.price == 0:
            return
        if self.price <= 0:
            raise ValidationError("The price must be positive.")

    # -------------------------------------------------------------------------
    # ACTION METHODS
    # -------------------------------------------------------------------------

    def action_confirm(self):
        self.property_id.offer_ids.status = "refused"
        self.status = "accepted"
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
        self.property_id.state = "offer_accepted"

    def action_cancel(self):
        self.status = "refused"

    # -------------------------------------------------------------------------
    # CONSTRAINTS METHODS
    # -------------------------------------------------------------------------

    rounding_precision = 0.0001
    @api.constrains('price')
    def _check_price(self):
        compare_value = float_compare(self.price,0.9*self.property_id.expected_price,precision_digits=2)
        if compare_value == -1:
            raise UserError("Offer Price must be atleast 90% of the expected price.")

        return True

    # -------------------------------------------------------------------------
    # CRUD METHODS
    # -------------------------------------------------------------------------

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            state = self.env['estate.property'].browse(val['property_id']).state
            if state == 'new' or not state:
                self.env['estate.property'].browse(val['property_id']).state = 'offer_received'

            min_price = min(self.env['estate.property.offer'].search([('property_id', '=', val['property_id'])]).mapped('price'), default=0)
            if val['price'] <= min_price:
                raise ValidationError("The price must be higher than any existing offer.")

            return super().create(vals)
