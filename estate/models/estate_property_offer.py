from odoo import api, fields, models
from odoo.tools.date_utils import date
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(
        copy=False, selection=[("accepted", "Accepted"), ("refused", "Refused")]
    )
    partner_id = fields.Many2one(comodel_name="res.partner", required=True)
    property_id = fields.Many2one(comodel_name="estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date if record.create_date else date.today()
            record.date_deadline = fields.Datetime.add(
                create_date, days=record.validity
            )

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept_offer(self):
        self.ensure_one()
        other_records = self.search(
            [("id", "!=", str(self.id)), ("property_id", "=", self.property_id.id)]
        )
        for rec in other_records:
            if rec.status == "accepted":
                raise UserError("Cannot have more than one accepted offer.")
        self.status = "accepted"
        self.property_id.buyer_id = self.partner_id
        self.property_id.selling_price = self.price
        return True

    def action_refuse_offer(self):
        self.ensure_one()
        old_status = self.status
        self.status = "refused"
        if old_status == "accepted":
            self.property_id.buyer_id = ""
            self.property_id.selling_price = 0
        return True
