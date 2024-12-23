from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "price asc"

    price = fields.Float()
    status = fields.Selection(
        string="Type",
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        store=True,
        string="Property Type",
        related="property_id.property_type_id",
    )

    _sql_constraints = [
        (
            "check_positive_price",
            "CHECK(price>0)",
            "The offer price should be positive.",
        ),
    ]

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            if not record.create_date:
                record.create_date = fields.Datetime.today()
            record.date_deadline = fields.Datetime.add(
                record.create_date, days=record.validity
            )

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept(self):
        self.ensure_one()
        self.status = "accepted"
        self.property_id.selling_price = self.price
        self.property_id.buyer = self.partner_id
        self.property_id.state = "offer accepted"
        return True

    def action_refuse(self):
        for record in self:
            record.status = "refused"
        return True
