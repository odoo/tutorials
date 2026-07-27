from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Table for offers of a property"
    _order = "price desc"

    price = fields.Float("Price")
    _check_price = models.Constraint(
        "CHECK(price >= 0)",
        "Le prix doit être strictement positif",
    )
    status = fields.Selection(
        string="Status",
        copy=False,
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
    )
    partner_id = fields.Many2one("res.partner", required=True, string="Partner")
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Datetime(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    property_type_id = fields.Many2one(related="property_id.property_type_id")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get("property_id")
            price = vals.get("price", 0)

            if not property_id:
                continue

            if self.env["estate.property.offer"].search_count(
                [
                    ("property_id", "=", property_id),
                    (
                        "price",
                        ">",
                        price,
                    ),
                ],
            ):
                raise UserError(
                    self.env._(
                        "You cannot create a offer with a lower price than a existing one for this property",
                    ),
                )

            self.env["estate.property"].browse(property_id).state = "offer received"
        return super().create(vals_list)

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Datetime.add(
                record.create_date.date() or fields.Datetime.now().date(),
                days=record.validity,
            )

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date).days

    def action_accept(self):
        for record in self:
            record.property_id.offer_ids.status = "refused"
            record.status = "accepted"
            record.property_id.state = "offer accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id

    def action_refuse(self):
        for record in self:
            record.status = "refused"
