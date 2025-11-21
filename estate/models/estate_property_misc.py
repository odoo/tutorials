from odoo import fields, models, api, exceptions


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(required=True)

    _check_unique_name = models.Constraint(
        "unique(name)",
        "Type must be unique",
    )


class PropertyTags(models.Model):
    _name = "estate.property.tags"
    _description = "Estate Property Tags"

    name = fields.Char(required=True)

    _check_unique_name = models.Constraint(
        "unique(name)",
        "Tag must be unique",
    )


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

    date_deadline = fields.Datetime(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )

    _check_positive_price = models.Constraint(
        "CHECK(price > 0.001)",
        "Prices Must Be Positive",
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for property in self:
            create_date = property.create_date or fields.Datetime.now()
            property.date_deadline = fields.Datetime.add(
                create_date,
                days=property.validity,
            )

    def _inverse_date_deadline(self):
        for property in self:
            create_date = property.create_date or fields.Datetime.now()
            property.validity = (property.date_deadline - create_date).days

    def accept_offer(self):
        self.ensure_one()
        if self.property_id.status == "sold":
            raise exceptions.UserError("Property is already sold")
        self.property_id.buyer_id = self.buyer_id
        self.property_id.selling_price = self.price
        self.status = "accepted"
        return True

    def refuse_offer(self):
        self.ensure_one()
        if self.property_id.status == "sold":
            raise exceptions.UserError("Property is already sold")
        self.status = "refused"
        return True
