from odoo import api, exceptions, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer for Estate Poperty"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one(
        "estate.property",
        string="Estate Property",
        required=True,
    )
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        string="Date Deadline",
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        related="property_id.property_type_id",
        store=True,
    )

    _positive_price = models.Constraint(
        "CHECK(price > 0)",
        "The price of an offer for a real estate property should be above zero.",
    )

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            base_date = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )
            record.date_deadline = fields.Date.add(
                base_date,
                days=record.validity,
            )

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date).days
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("property_id") and vals.get("price"):
                prop = self.env["estate.property"].browse(vals["property_id"])

                if prop.offer_ids:
                    max_offer = max(prop.offer_ids.mapped("price"))
                    if vals["price"] < max_offer:
                        raise exceptions.UserError(
                            f"The offer must be strictly higher than {max_offer:,.2f}",
                        )

                prop.stage = "offer_received"

        return super().create(vals_list)

    def action_accept(self):
        for record in self:
            if "accepted" not in record.property_id.offer_ids.mapped("status"):
                record.status = "accepted"
                record.property_id.stage = "offer_accepted"
                record.property_id.buyer_id = record.partner_id
                record.property_id.selling_price = record.price
                return True
            raise exceptions.UserError(
                "There is already an offer accepted for the same property",
            )

    def action_refuse(self):
        for record in self:
            record.status = "refused"
            return True
