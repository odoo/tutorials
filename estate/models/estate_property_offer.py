from dateutil.relativedelta import relativedelta
from odoo import fields, models, api


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property offer"
    _order = "price desc"

    price = fields.Float(required=True)
    partner_id = fields.Many2one("res.partner", required=True, string="Buyer")
    status = fields.Selection(selection=[("awaiting", "Awaiting"), ("refused", "Refused"), ("accepted", "Accepted")], required=True, default="awaiting", copy=False)

    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(store=True, related="property_id.property_type_id")

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    _sql_constraints = [
        ("price", "CHECK(price > 0)", "Offer price must be positive.")
    ]

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            origin = record.create_date or fields.Date.today()
            record.date_deadline = origin + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            origin = record.create_date or fields.Date.today()
            record.validity = (record.date_deadline - origin.date()).days


    def action_accept(self):
        self.ensure_one()
        self.property_id.buyer_id = self.partner_id
        self.property_id.selling_price = self.price
        # delayed orm operations with write? or just shorter, either way
        self.property_id.write({"status": "refused"})

        self.status = "accepted"
        return True

    def action_refuse(self):
        self.ensure_one()
        self.status = "refused"
        return True

    @api.model
    def create(self, vals):
        self.env["estate.property"].search([("id", "=", vals["property_id"])]).status = "offer_received"
        return super().create(vals)
