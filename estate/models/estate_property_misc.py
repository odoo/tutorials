from odoo import fields, models, api


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(required=True)


class PropertyTags(models.Model):
    _name = "estate.property.tags"
    _description = "Estate Property Tags"

    name = fields.Char(required=True)


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float(required=True)
    status = fields.Selection(
        string="Status",
        copy=False,
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date", inverse="_inverse_date")

    @api.depends("validity")
    def _compute_date(self):
        for record in self:
            create_date = record.create_date
            if not create_date:
                create_date = fields.Date.today()
            record.date_deadline = fields.Date.add(
                create_date,
                days=record.validity,
            )

    def _inverse_date(self):
        for record in self:
            create_date = record.create_date.date()
            if not create_date:
                create_date = fields.Date.today()
            record.validity = (record.date_deadline - create_date).days
