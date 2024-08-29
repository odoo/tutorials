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


pick 5308379 [ADD] Discover the JavaScript framework
s 6203e77 creation of estate dir
s 9921695 creation of estate mainfest
s 3a13e67 mv mainfes to manifest
s 259ab1c converting estate to app
s a87fadd [ADD] estate: createing the tabe and it fields
s 49c29d6 [IMP] fixing all style errors in estate directory
s 141850c [IMP] fixing all style errors in TUTORIALS directory
s 8b520ea [IMP] fixing all style errors in TUTORIALS directory
s 1c380c9 [IMP] fixing all style errors in TUTORIALS directory
s dea91f2 [ADD] I added access rights to estate_property_type model
s ee83294 [ADD] I added license to estate manifest
s 0f66e44 [ADD] I Buyer and salesman atributes to estate_property model
s 8e14921 [ADD] I added the Property tag view and link it to estate property
s 0804a8b [ADD] saving ..
s 6712a8a [IMP] Made revisions based on reviewer feedback
s 692ceb6 [IMP] Made revisions based on reviewer feedback
s d3ffafa [IMP] estate: Made revisions based on reviewer feedback
s 5ab3982 [ADD] estate: I add What was asked in chapters 'till 11
s b6ad338 [ADD] estate: I add chapter up to 11
s c6fa411 [IMP] estate: style improving to match runbot requirements
