from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _check_expected_price = models.Constraint("CHECK(expected_price>0)", "Le prix doit être strictement positif.")
    _check_selling_price = models.Constraint("CHECK(selling_price>=0)", "Le prix doit être positif.")

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=fields.Date.add(fields.Date.today(), months=3), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden orientation',
        selection=[('North', 'N'), ('South', 'S'), ('East', 'E'), ('West', 'W')],
        help="Specify the orientation of the garden to know when you're gonna enjoy the sun")
    state = fields.Selection(
        selection=[('New', 'New'), ('Offer Received', 'Offer Received'), ('Offer Accepted', 'Offer Accepted'), ('Sold', 'Sold'), ('Cancelled', 'Cancelled')],
        default='New'
    )
    active = fields.Boolean(default=True)
    salesman = fields.Many2one("res.users")
    buyer = fields.Many2one("res.partner", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Float(compute="_compute_total")
    best_price = fields.Float(compute="_compute_highest_price")

    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_highest_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price")) if record.offer_ids else 0

    @api.onchange("garden")
    def _onchange_garden(self):
        self.garden_area = 10 if self.garden else 0
        self.garden_orientation = "North" if self.garden else None

    def action_mark_as_sold(self):
        if self.state == "Cancelled":
            raise UserError("Cette vente a été annulée")
        self.state = "Sold"
        return True

    def action_mark_as_cancelled(self):
        if self.state == "Sold":
            raise UserError("Cette maison a déjà été vendue")
        self.state = "Cancelled"
        return True

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price_is_ok(self):
        for record in self:
            if float_compare(self.selling_price, 0.9 * self.expected_price, 2) == -1:
                raise ValidationError("Le prix de vente doit valoir au moins 90 pourcents du prix attendu.")
