from datetime import timedelta,datetime
from odoo import api, models, fields
from odoo.tools.float_utils import float_compare
from odoo.exceptions import UserError

class estatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order="price desc"

    price = fields.Float("Price")
    status = fields.Selection([
        ("accepted", "accepted"),
        ("cancelled", "cancelled"),
        ("refused","refused")
    ], string="Status")
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
        related="property_id.property_type_id",
        store=True,
    )
    validity = fields.Integer(string="validity", default=7)
    date_deadline = fields.Date(string="date_deadline", compute="compute_date_deadline", inverse="inverse_date_deadline" , store="true")

    _sql_constraints = [
        ("check_offer_price", "CHECK(price > 0)", "Offer Price must be positive"),
    ]

    def inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                if record.create_date:
                    record.validity = (record.date_deadline - record.create_date.date()).days

    @api.depends("create_date", "validity")
    def compute_date_deadline(self):
        for record in self:
            if record.create_date:
                # Compute the deadline by adding the validity (days) to the creation date
                record.date_deadline = (record.create_date.date() + timedelta(days=record.validity))
    
    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            if val.get("property_id") and val.get("price"):
                prop = self.env["estate.property"].browse(val["property_id"])

                if prop.offer_ids:
                    max_offer = max(prop.mapped("offer_ids.price"))
                    if float_compare(val["price"], max_offer, precision_rounding=0.01) <= 0:
                        raise UserError("The offer must be higher than %.2f" % max_offer)
                prop.state = "offer_received"
        return super().create(vals_list)
    
    def action_accept_offer(self):
        for record in self:
            if record.property_id.state == "sold":
                raise UserError("This property is already sold!")
            if record.property_id.buyer_id:
                raise UserError("This property already has a buyer!")
            record.status = "accepted"
            print("set user")
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = "sold"

    def action_refuse_offer(self):
        for record in self:
            record.status = "refused"
            record.property_id.state="not sold"
            record.property_id.buyer_id =False
            record.property_id.selling_price =False

