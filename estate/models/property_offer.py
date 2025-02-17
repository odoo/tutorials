from odoo import models, fields, api 
from datetime import timedelta
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare


class PropertyOffer(models.Model):
    _name = "public.property.offer"
    _description = "Property Offers"
    _order = "price desc"

    _sql_constraints = [
        ("check_price", "CHECK(price >= 0)", "The offer price must be positive.")
    ]

    price = fields.Float()
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True, string="partner")
    property_id = fields.Many2one("public.property", required=True)
    validity = fields.Integer(string="Validity (Days)", default=7)

    property_type_id = fields.Many2one(
        "public.property.type", related="property_id.property_type_id", store=True
    )

    date_deadline = fields.Date(
        string="Deadline Date",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
    )
    
    rounding_precision = 0.0001
    @api.constrains("price")
    def _check_price(self):
        for record in self:
            if (
                float_compare(
                    record.property_id.expected_price * 0.9,
                    record.price,
                    precision_rounding=self.rounding_precision,
                )
                >= 0
            ):
                raise ValidationError(
                    "The selling price cannot be less than the 90% of expected price"
                )
            record.property_id.state = "offer_received"

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(
                    days=record.validity
                )
            else:
                record.date_deadline = False

    @api.depends("date_deadline")
    def _inverse_date_deadline(self):
        for record in self : 
            if record.date_deadline:
                deadline = record.date_deadline
                record.validity = (deadline - record.create_date.date()).days

    def action_confirm(self):
        for record in self:
            self.property_id.offer_ids.status = "refused"
            self.status = "accepted"
            self.property_id.selling_price = self.price
            self.property_id.buyer_id = self.partner_id
            self.property_id.state = "offer_accepted"
    def action_cancel(self):
        for record in self:
            record.status = "refused"

    
    # @api.model
    # def create(self,vals):
    #     min_price = min(self.env['public.property.offer'].search([('property_id', '=', vals['property_id'])]).mapped('price'), default=0)
    #     if vals['price'] <= min_price:
    #         raise ValidationError("The price must be higher than any existing offer.")
    #     return super().create(vals)
