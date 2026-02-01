from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "This is the table of offer that is received for property"
    _order = "price desc"

    price = fields.Float("price")
    status = fields.Selection(
        string="Status",
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True
    )
    property_type_id = fields.Many2one(
        "estate.property.type", related="property_id.property_type_id", store=True
    )

    _check_offer_price = models.Constraint(
        "check(price > 0)",
        "Offer price must be positive",
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            create = record.create_date or fields.Date.today()
            record.date_deadline = create + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create = record.create_date or fields.Date.today()
            record.validity = (record.date_deadline - fields.Date.today(create)).days

    @api.model
    def create(self, vals):
        for record in vals:
            property_id = record.get("property_id")
            offer_price = record.get("price")
            if property_id:
                property_record = self.env["estate.property"].browse(property_id)
                if offer_price < property_record.best_price:
                    raise ValidationError(
                        _("Offer price must be greater than best offer.")
                    )
                property_record.state = "offer received"
        return super().create(vals)

    def action_accept_offer(self):
        self.ensure_one()
        better_offer = self.property_id.offer_ids.filtered(
            lambda s: s.price > self.price
        )
        if better_offer:
            return {
                "type": "ir.actions.act_window",
                "res_model": "estate.offer.wizard",
                "view_mode": "form",
                "target": "new",
                "context": {"default_offer_id": self.id},
            }
        return self.accept_offer()

    def accept_offer(self):
        self.ensure_one()
        if self.property_id.customer_id:
            raise UserError(_("Only one offer can be accepted."))
        self.property_id.customer_id = self.partner_id
        self.property_id.selling_price = self.price
        self.status = "accepted"
        self.property_id.state = "offer accepted"
        other_offer = self.property_id.offer_ids.filtered(
            lambda s: s.status != self.status
        )
        other_offer.status = "refused"

    def action_refuse_offer(self):
        self.ensure_one()
        self.status = "refused"
        return True
