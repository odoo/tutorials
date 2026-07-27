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
        compute="_date_deadline",
        inverse="_set_date_deadline",
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
    def _date_deadline(self):
        for record in self:
            record.date_deadline = fields.Datetime.add(
                record.create_date or fields.Datetime.now(),
                days=record.validity,
            )

    def _set_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date).days

    def accept(self):
        self.property_id.offer_ids.status = "refused"
        self.status = "accepted"
        self.property_id.state = "offer accepted"
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id

    def refuse(self):
        self.status = "refused"
        self.property_id.selling_price = None
        self.property_id.buyer_id = None
