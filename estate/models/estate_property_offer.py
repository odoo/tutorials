from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offers"
    _order = "price desc"

    price = fields.Float(required=True)
    state = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
        readonly=True,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
    )

    property_type_id = fields.Many2one(
        related="property_id.property_type_id",
        store=True,
    )

    show_offer_action = fields.Boolean(compute="_compute_show_offer_action")

    _check_price = models.Constraint(
        "CHECK(price > 0)",
        "Offer price must be strictly positive.",
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for offer in self:
            create_date = offer.create_date or fields.Date.today()
            offer.date_deadline = fields.Date.add(create_date, days=offer.validity)

    @api.depends("date_deadline")
    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_date.date() or fields.Date.today()
            record.validity = (record.date_deadline - create_date).days

    @api.depends("property_id.state")
    def _compute_show_offer_action(self):
        for offer in self:
            offer.show_offer_action = offer.property_id.state in {
                "offer_accepted",
                "sold",
                "cancelled",
            }

    def action_offer_accepted(self):
        self.ensure_one()
        self.state = "accepted"
        self.property_id.state = "offer_accepted"
        self.property_id.buyer_id = self.partner_id
        self.property_id.selling_price = self.price

    def action_offer_refused(self):
        self.ensure_one()
        self.state = "refused"
