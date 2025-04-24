import datetime

from odoo import api, fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    name = fields.Char(string="Title")
    seller_id = fields.Many2one(
        "res.users", string="Salesperson", index=True, copy=True, default=lambda self: self.env.user
    )
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=datetime.datetime.now()
        + datetime.timedelta(days=90),  # Setting the date availability 3 months from now.
        copy=False,
    )
    validity_days = fields.Integer(default=7)
    deadline_date = fields.Date(compute="_compute_deadline_date", inverse="_inverse_validity_days")
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True, copyright=False, copy=False)
    bedrooms = fields.Integer(default=4)
    living_area = fields.Integer()
    garden_area = fields.Integer()
    total_area = fields.Integer(compute="_compute_total_area")
    facades = fields.Integer()
    has_garage = fields.Boolean()
    has_garden = fields.Boolean()
    active = fields.Boolean(default=True)
    garden_orientation = fields.Selection(
        selection=[("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")]
    )
    status = fields.Selection(
        selection=[("new", "New"), ("offer_receieved", "Offer Recieved"), ("sold", "Sold"), ("cancelled", "Cancelled")],
        readonly=True,
        default="new",
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property type")
    property_tag_id = fields.Many2many("estate.property.tag", string="Property tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    best_offer_price = fields.Float(compute="_compute_best_offer_price")

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer_price(self):
        for record in self:
            record.best_offer_price = max(record.offer_ids.mapped("price")) if record.offer_ids else 0.0

    def _compute_deadline_date(self):
        for record in self:
            record.deadline_date = datetime.date.today() + datetime.timedelta(days=record.validity_days)

    @api.depends("deadline_date")
    def _inverse_validity_days(self):
        for record in self:
            record.validity_days = (record.deadline_date - datetime.date.today()).days

    @api.onchange("has_garden")
    def _onchange_has_garden(self):
        for record in self:
            if record.has_garden:
                record.garden_orientation, record.garden_area = "north", 10
            else:
                record.garden_orientation, record.garden_area = None, None
