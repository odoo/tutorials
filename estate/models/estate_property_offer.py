from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class estatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "The offer of estate property"
    _order = "price desc"
    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)',
         'A property offer price must be strictly positive'),
    ]

    price = fields.Float("Price")
    partner_id = fields.Many2one("res.partner", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    property_id = fields.Many2one('estate.property', required=True)
    property_type_id = fields.Many2one("estate.property.type", related="property_id.type_id", store=True)

    state = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Status",
        copy=False,
        default=False,
    )
    date_deadline = fields.Date(
        string="Deadline (days)",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Datetime.add(record.create_date, days=record.validity)
            else:
                record.date_deadline = fields.Datetime.add(fields.Datetime.today(), days=record.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - date).days

    def action_accepted(self):
        if "Accepted" in self.mapped("state"):
            raise UserError("An offer as already been accepted.")
        self.write(
            {
                "state": "accepted",
            }
        )
        return self.mapped("property_id").write(
            {
                "state": "offer_accepted",
                "selling_price": self.price,
                "buyer_id": self.partner_id.id,
            }
        )

    def action_refused(self):
        return self.write(
            {
                "state": "refused",
            }
        )

    @api.constrains("price", "property_id.expected_price")
    def check_price(self):
        for record in self:
            if record.price < (0.9 * record.property_id.expected_price):
                raise ValidationError("The selling price must be at least 90%% of the expected price")

