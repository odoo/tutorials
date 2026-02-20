from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer"
    _order = "sequence, id"

    property_id = fields.Many2one("estate.property", string="Property", required=True)
    partner_id = fields.Many2one("res.partner", string="Partner", index=True, required=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type", related="property_id.property_type_id")

    # Deadline Part
    def _current_date(self):
        return fields.Date.today()

    def _seven_days_from_now_date(self):
        return fields.Date.add(fields.Date.today(), days=7)

    deadline = fields.Date("Deadline", default=_seven_days_from_now_date)
    creation_date = fields.Date("Creation Date", default=_current_date)
    validity = fields.Integer("Validity (days)", store=True, compute="_compute_validity", inverse="_inverse_validity")

    # Currency Part
    currency_id = fields.Many2one("res.currency", "Currency")
    property_currency_id = fields.Many2one("res.currency", "Partner Currency", related="property_id.currency_id")
    price = fields.Monetary("Original Price", required=True)
    translated_price = fields.Monetary("Price", store=True, compute="_compute_translated_price")

    # State / validation part
    status = fields.Selection([
        ("accepted", "Accepted"),
        ("refused", "Refused"),
    ], copy=False)

    sequence = fields.Integer("Sequence", default=0)

    # Deadline part
    @api.depends("deadline")
    def _compute_validity(self):
        for offer in self:
            offer.validity = (offer.deadline - offer.creation_date).days

    # Reverse from _compute_validity, with real-time update because otherwise it's only after closing the form
    @api.onchange("validity")
    def _inverse_validity(self):
        for offer in self:
            offer.deadline = fields.Date.add(offer.creation_date, days=offer.validity)

    # Currency part

    # Translate currency to the one of the property so it's easier to compare
    # Also, the webpage doesn't like showing multiple currency signs (as $ and €),
    # so we put everything in the base currency for display

    def _compute_currency(self):
        if self.property_currency_id == self.currency_id:
            return self.price
        return self.currency_id._convert(self.price, self.property_currency_id)

    @api.depends("property_currency_id", "price", "currency_id")
    def _compute_translated_price(self):
        for offer in self:
            offer.translated_price = offer._compute_currency()

    # Validation part
    def action_confirm(self):
        for offer in self:
            if offer.property_id.stage in ["offer_accepted", "sold", "cancelled"]:
                raise UserError(_("You can't accept new offers"))
            offer.property_id.selling_price = offer.translated_price
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.stage = "offer_accepted"
            offer.status = "accepted"

    def action_refuse(self):
        for offer in self:
            offer.status = "refused"

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            property = self.env["estate.property"].browse(val["property_id"])
            if property.stage == "new":
                property.stage = "offer_received"

            if property.stage != "offer_received":
                raise ValidationError(_("You can't create offers at this point"))

        return super().create(vals_list)

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'The price has to be stricly positive'
    )
