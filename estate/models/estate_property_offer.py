from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate properties offer"
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused")
        ],
        string="Status",
        help="Offer status",
        copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Offerer", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id")

    @api.model
    def create(self, vals):
        if len(self.env["estate.property"].browse(vals["property_id"]).offer_ids) > 0 and vals["price"] < min(self.env["estate.property"].browse(vals["property_id"]).offer_ids.mapped("price")):
            raise UserError("Cannot create an offer lower than an existing one.")
        self.env["estate.property"].browse(vals["property_id"]).state = "received"
        return super().create(vals)
        
    def action_estate_property_offer_accept(self):
        for record in self:
            if "accepted" in record.property_id.offer_ids.mapped("status"):
                raise UserError("An offer has already been accepted.")
            else:
                record.status = "accepted"
                record.property_id.buyer = record.partner_id
                record.property_id.selling_price = record.price
                record.property_id.state = 'accepted'

    def action_estate_property_offer_refuse(self):
        for record in self:
            if record.status == "accepted":
                record.property_id.state = "received"
                record.property_id.buyer = ""
                record.property_id.selling_price = 0
            record.status = "refused"

    @api.ondelete(at_uninstall=False)
    def _unlink_offer(self):
        for record in self:
            if record.status == "accepted":
                record.property_id.state = "received"
                record.property_id.buyer = ""
                record.property_id.selling_price = 0
            record.status = "refused"
    
    _sql_constraints = [
        ("check_offer_price", "CHECK(price > 0)",
         "The price should be > 0.")
    ]
