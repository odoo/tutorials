from odoo import api, fields, models

class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float(
        "Price",
        help="This specifies the price offered for the property."
    )
    status = fields.Selection(
        string="Status",copy=False,
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ]
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(
        "Validity (in Days)", default=7,
        help="This shows the offer validity.",
    )
    date_deadline = fields.Date(
        "Deadline", compute="_compute_deadline", inverse="_inverse_deadline",
        help="This shows the offer validity date.",
    )
    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type",
        store=True, related="property_id.property_type_id"
    )

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)',
        'The offer price must be strictly positive.'),
    ]

    @api.depends('create_date', 'validity')
    def _compute_deadline(self):
        for line in self:
            if line.create_date and line.validity:
                line.date_deadline = fields.Date.add(line.create_date, days=line.validity)
            else:
                line.date_deadline = fields.Date.add(fields.Date.today(), days=line.validity)

    def _inverse_deadline(self):
        for line in self:
            if line.create_date and line.date_deadline:
                line.validity = (line.date_deadline - fields.Date.to_date(line.create_date)).days

    def accept_offer(self):
        other_offers = self.search(
            domain=[
                ('property_id', '=', self.property_id.id),
            ],
        )

        other_offers.write({"status": "refused"})

        self.status = "accepted"
        self.property_id.buyer = self.partner_id
        self.property_id.selling_price = self.price
        return True

    def refuse_offer(self):
        self.status = "refused"
        return True
