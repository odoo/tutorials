from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
    )
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    property_id = fields.Many2one("estate.property", required=True, ondelete="cascade")

    property_type_id = fields.Many2one(
        "estate.property.type", related="property_id.property_type_id", store=True
    )

    _check_positive_price = models.Constraint(
        "CHECK(price > 0)", "The Price Should be Positive"
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            date = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )
            record.date_deadline = date + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            date = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )
            record.validity = (
                (record.date_deadline - date).days if record.date_deadline else 0
            )

    @api.model
    def _check_offer_deadline(self):
        overdue_offers = self.search(
            [
                ("date_deadline", "<", fields.Date.today()),
                ("status", "=", False),
            ]
        )
        for rec in overdue_offers:
            id = self.env["estate.property.offer"].browse(rec.id)
            id.unlink()

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = self.env["estate.property"].browse(vals.get("property_id"))
            if property_id:
                if property_id.offer_ids:
                    max_price = max(property_id.offer_ids.mapped("price"))
                    if vals.get("price") < max_price:
                        raise UserError(
                            self.env._(
                                "The offer price must be higher than the existing offer price."
                            )
                        )
            if property_id and property_id.state == "new":
                property_id.state = "offer_received"
        return super().create(vals_list)

    def action_accept(self):
        for record in self:
            record.status = "accepted"
            record.property_id.write(
                {
                    "buyer_id": record.partner_id.id,
                    "selling_price": record.price,
                    "state": "offer_accepted",
                }
            )
            other_offers = record.property_id.offer_ids - record
            other_offers.write({"status": "refused"})
        return True

    @api.ondelete(at_uninstall=False)
    def _unlink_offer(self):
        for property in self.mapped("property_id"):
            offers_to_delete = self.filtered(lambda o: o.property_id == property)
            remaining_offers = property.offer_ids - offers_to_delete
            if not remaining_offers:
                property.state = "new"

    def action_refuse(self):
        for record in self:
            record.status = "refused"
        return True
