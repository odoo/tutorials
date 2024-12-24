from datetime import date, timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers"
    _order = "price desc"

    price = fields.Float(string="Offer Price")
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one(
        "estate.property", string="Property Name", required=True
    )
    status = fields.Selection(
        string="Status",
        selection=[("refused", "Refused"), ("accepted", "Accepted")],
        copy=False,
    )
    validity = fields.Integer(default=7, string="validity (days)")
    date_deadline = fields.Date(
        compute="_compute_deadline", inverse="_compute_validity", string="Deadline"
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        related="property_id.property_type_id",
        store=True,
        string="Property Type",
    )

    _sql_constraints = [
        (
            "check_price",
            "CHECK(price > 0)",
            "The offer price should be strictly positive",
        ),
        # (
        #     "check_price_highe"
        # )
    ]

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = date.today() + timedelta(record.validity)

    def _compute_validity(self):
        for record in self:
            record.validity = (record.date_deadline - date.today()).days

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for vals in vals_list:
            prop_id = vals["property_id"]
            offer_price = vals["price"]
            res = self.env["estate.property"].browse(prop_id)
            if prop_id:
                res.write({"state": "offer_received"})
                if offer_price:
                    existing_offers = self.search(
                        [("property_id", "=", prop_id), ("price", ">", offer_price)],
                        limit=1,
                    )
                    if existing_offers:
                        raise UserError(
                            "An offer with the higher price already exists."
                        )
        return records

    @api.ondelete(at_uninstall=False)
    def _unlink_except_status_accepted(self):
        for record in self:
            if record.status == "accepted":
                raise UserError("Accepted offers cannot be deleted.")

    def action_accept(self):
        for record in self:
            for offer in record.property_id.offer_ids:
                offer.status = "refused"
            record.status = "accepted"
            record.property_id.state = "offer_accepted"
            record.property_id.selling_price = record.price
            record.property_id.partner_id = record.partner_id

    def action_refuse(self):
        for record in self:
            record.status = "refused"
            record.property_id.state = "new"
