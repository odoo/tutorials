from odoo import api, fields, models
from odoo.exceptions import UserError


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"
    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)',
        'The offer price must be strictly positive.'),
    ]

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
        "Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline",
        help="This shows the offer validity date.",
    )
    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type",
        store=True, related="property_id.property_type_id"
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for line in self:
            if line.create_date and line.validity:
                line.date_deadline = fields.Date.add(line.create_date, days=line.validity)
            else:
                line.date_deadline = fields.Date.add(fields.Date.today(), days=line.validity)

    def _inverse_date_deadline(self):
        for line in self:
            if line.create_date and line.date_deadline:
                line.validity = (line.date_deadline - fields.Date.to_date(line.create_date)).days

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            property_id = self.env['estate.property'].browse(val['property_id'])

            if property_id.state == "new":
                property_id.state = "offer_received"

            if val['price'] <= property_id.best_price:
                raise UserError(f"The offer must be higher than {property_id.best_price}")

        return super().create(vals)

    def action_accept_offer(self):
        self.ensure_one()

        other_offers = self.search(
            domain=[
                ('property_id', '=', self.property_id.id),
            ],
        )

        other_offers.write({"status": "refused"})

        self.status = "accepted"
        self.property_id.buyer_id = self.partner_id
        self.property_id.selling_price = self.price
        self.property_id.state = "offer_accepted"

        return True

    def action_refuse_offer(self):
        self.ensure_one()

        self.status = "refused"
        return True
