from odoo import api, models, fields, exceptions


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float("Price")
    status = fields.Selection([
        ("accepted", "Accepted"),
        ("refused", "Refused")],
        string="Status", copy=False)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer("Validity (days)", default=7)
    date_deadline = fields.Date("Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type", related="property_id.property_type_id")

    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "Offer price must be positive.")
    ]

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(
                record.create_day if hasattr(record, "create_day") else fields.Date.today(),
                days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_day if hasattr(record, "create_day") else fields.Date.today()
            record.validity = (record.date_deadline - create_date).days

    def action_accept_offer(self):
        for record in self:
            if record.property_id.state not in ["offer_accepted", "sold"]:
                # if tools.float_utils.float_compare(record.price, 0.9 * record.property_id.expected_price, precision_rounding=2) == -1:
                # i don't know why the above didn't work (i tried for expected price 100 and offer price 89 and it still accepted the offer
                # so i wrote the below instead, which is not a good practice)
                if record.price < 0.9 * record.property_id.expected_price:
                    raise exceptions.ValidationError("The selling price cannot be lower than 90% of the expected price.")
                else:
                    record.status = "accepted"
                    record.property_id.state = "offer_accepted"
                    record.property_id.buyer_id = record.partner_id
                    record.property_id.selling_price = record.price
            else:
                raise exceptions.UserError("Only one offer can be accepted.")

    def action_refuse_offer(self):
        for record in self:
            record.status = "refused"

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            property = self.env["estate.property"].browse(val["property_id"])
            if val["price"] < property.best_price:
                raise exceptions.UserError(f"Price must be at least ${property.best_price}.")

            property.state = "offer_received"

        return super().create(vals)
