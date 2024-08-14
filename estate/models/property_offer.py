from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from odoo import api, models, fields


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float(string="Price", required=True)
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")],
        string="Status",
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one(
        "estate.property", string="Property", ondelete="cascade"
    )
    validity = fields.Integer(string="Validity (days)", default=7)
    deadline_date = fields.Date(
        string="Deadline", compute="_compute_deadline", inverse="_inverse_deadline"
    )
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )

    @api.depends("property_id.create_date", "validity")
    def _compute_deadline(self):
        for record in self:
            if record.property_id.create_date:
                record.deadline_date = record.property_id.create_date + relativedelta(
                    days=record.validity
                )
            else:
                record.deadline_date = False

    def _inverse_deadline(self):
        for record in self:
            if record.property_id.create_date and record.deadline_date:
                record.validity = (
                    record.deadline_date - record.property_id.create_date.date()
                ).days
            else:
                record.validity = 7

    def action_refused(self):
        for record in self:
            record.status = "refused"

    def action_accepted(self):
        for record in self:
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id

    @api.model
    def create(self, vals):
        property_users = self.env["estate.property"].browse(vals.get("property_id"))
        property_users.state = "offer received"
        if property_users.offer_ids.filtered(lambda o: o.price >= vals.get("price")):
            raise UserError(
                "You cannot create an offer with a lower amount than an existing offer."
            )
        return super().create(vals)
