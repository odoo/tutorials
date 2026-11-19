from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(required=True, string="title")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string="Available from", copy=False,
                                    default=lambda self: fields.Date.add(fields.Date.today(), months=3), required=True)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2, required=True)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean(onchange="_onchange_garden")
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
        help="Orientation of the garden")
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        selection=[("new", "New"), ("offer_received", "Offer Received"), ("offer_accepted", "Offer Accepted"),
                   ("sold", "Sold"), ("cancelled", "Cancelled")], required=True,
        copy=False, default="new")
    type_id = fields.Many2one("estate.property.type", string="Property Type")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    salesperson = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Integer(compute="_compute_best_price")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids", "offer_ids.state")
    def _compute_best_price(self):
        for record in self:
            offers = self.offer_ids.filtered(lambda offer: offer.state == "accepted")
            record.best_price = max(offers.mapped("price")) if offers else 0

    @api.onchange("garden")
    def _onchange_garden(self):
        self.garden_area = 10
        self.garden_orientation = "north"  # return {'warning': {  #     'title': ("Warning"),  #     'message': ('Garden area and description set')}}

    def action_do_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError(_("Sold properties cannot be canceled"))
            else:
                record.state = "cancelled"
        return True

    def action_do_sell(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError(_("Cancelled properties cannot be sold"))
            else:
                record.state = "sold"
        return True
