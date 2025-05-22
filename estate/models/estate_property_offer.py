from odoo import api, fields, models, exceptions
from dateutil.relativedelta import relativedelta


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "An offer made by a buyer to acquire a property"
    _order = "price desc"

    status = fields.Selection([("accepted", "Accepted"), ("refused", "Refused")], copy=False)
    price = fields.Float()
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    property_type_id = fields.Many2one("estate.property.type", related="property_id.property_type_id", string="Property Type")
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", string="Deadline")

    _sql_constraints = [("positive_price", "CHECK(price > 0)", "The offer price must be positive.")]

    @api.depends("validity")
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = (
                (offer.create_date if offer.create_date else fields.Datetime().today()) + relativedelta(days=offer.validity)
            ).date()

    def _inverse_date_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline - (offer.create_date.date() if offer.create_date else fields.Date().today())).days

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            self.env["estate.property"].browse(vals["property_id"]).state = "received"
        return super().create(vals_list)

    def action_confirm(self):
        for offer in self:
            if offer.property_id.state == "sold" or offer.property_id.state == "cancelled":
                raise exceptions.UserError("You can accept an offer on a properties that is cancelled or already sold !")
            offer.status = "accepted"
            offer.property_id.state = "accepted"
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price

    def action_refuse(self):
        for offer in self:
            offer.status = "refused"
        return True
