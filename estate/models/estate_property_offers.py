from odoo import fields, models, api, exceptions


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offers"
    _description = "Estate Property Offer"
    _order = "price desc"
    _sql_constraints = [
        ("postive_price", "CHECK(price > 0)", "Prices must be positive")
    ]

    price = fields.Float()
    status = fields.Selection(
        [("Accepted", "accepted"), ("refused", "Refused")], copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(
        "estate.property.type", related="property_id.property_type_ids", required=True
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_deadline", inverse="_inverse_deadline", store=True
    )

    # date_deadline
    @api.depends("create_date", "validity")
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(
                    record.create_date, days=record.validity
                )
            # if user adding new data then their is no available of create_date then use today
            else:
                record.date_deadline = fields.Date.add(
                    fields.Date.today(), days=record.validity
                )

    def _inverse_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (
                    record.date_deadline - record.create_date.date()
                ).days
            else:
                record.validity = (
                    record.date_deadline - record.fields.Date.today()
                ).days

    def action_accepted(self):
        for record in self:
            # selling price is default 0 and field is readonly then when the selling_price 0 so their is no offer is accepted yet
            if record.property_id.selling_price == 0:
                record.status = "Accepted"
                record.property_id.selling_price = record.price
                record.property_id.buyer = record.partner_id
                record.property_id.state = "offer_accepted"

                # if one offer is accepted then other offers are refused automatically

                other_record = self.env["estate.property.offers"].search(
                    [
                        ("property_id", "=", record.property_id.id),
                        ("id", "!=", record.id),
                    ]
                )
                other_record.write({"status": "refused"})

            else:
                raise exceptions.UserError("Already One Offer is Accepted")

    def action_refused(self):
        for record in self:
            record.status = "refused"

    @api.model_create_multi
    def create(self, vals):
        for record in vals:
            property_id = record["property_id"]
            if property_id:
                property = self.env["estate.property"].browse(property_id)
                if property.state == "new":
                    property.state = "offer_received"
                if record["price"] < property.best_price:
                    raise exceptions.UserError(
                        f"The offer price should be higher than {property.best_price}"
                    )
        return super().create(vals)
