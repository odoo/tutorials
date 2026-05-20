from odoo import models, fields, api, _
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property_offer"
    _description = "Offers received for property"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )
    partner_id = fields.Many2one(comodel_name="res.partner", required=True)
    property_id = fields.Many2one(comodel_name="estate_property", required=True, ondelete='cascade')
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )

    _check_price = models.Constraint(
        "CHECK(price > 0)", "offer price should be strictly positive"
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(
                (
                    record.create_date.date()
                    if record.create_date
                    else fields.Date.context_today(record)
                ),
                days=record.validity,
            )

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                record.validity = (
                    record.date_deadline
                    - (
                        record.create_date.date()
                        if record.create_date
                        else fields.Date.context_today(record)
                    )
                ).days

    @api.model
    def create(self, val_lists):
        for vals in val_lists:
            property = self.env["estate_property"].browse(vals["property_id"])
            if property.best_price > vals.get("price", 0):
                raise UserError(_("offer with price greater than current offer exists"))
            if property.state == "new":
                property.state = "offer_received"
        return super().create(val_lists)

    def action_accept_offer(self):
        if self.property_id.state == "offer_accepted":
            raise UserError(_("offer is already accepted"))
        (self.property_id.offer_ids - self).status = "refused"
        self.status = "accepted"
        self.property_id.buyer_id = self.partner_id
        self.property_id.selling_price = self.price
        self.property_id.state = "offer_accepted"

    def action_refuse_offer(self):
        for record in self:
            if record.status == "accepted":
                record.property_id.buyer_id = False
                record.property_id.selling_price = False
            record.status = "refused"

    def _refuse_pending_offers(self):
        offers = self.search([("status", "!=", "accepted")])
        offers.filtered(
            lambda self: self.date_deadline < fields.Date.today()
        ).status = "refused"
