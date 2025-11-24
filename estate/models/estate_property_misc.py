from odoo import fields, models, api, exceptions


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"

    name = fields.Char(required=True, string="Type Name")
    description = fields.Char()
    sequence = fields.Integer("Sequence", default=1)

    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count", default=0)

    _check_unique_name = models.Constraint(
        "unique(name)",
        "Type must be unique",
    )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for type in self:
            count = 0
            for offer in type.offer_ids:
                count += 1
            type.offer_count = count


class PropertyTags(models.Model):
    _name = "estate.property.tags"
    _description = "Estate Property Tags"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _check_unique_name = models.Constraint(
        "unique(name)",
        "Tag must be unique",
    )


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float(required=True)
    state = fields.Selection(
        string="State",
        copy=False,
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
    )
    validity = fields.Integer(default=7)

    buyer_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )

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
        if self.property_id.state == "sold":
            raise exceptions.UserError("Property is already sold")
        self.property_id.buyer_id = self.buyer_id
        self.property_id.selling_price = self.price
        self.state = "accepted"
        return True

    def refuse_offer(self):
        self.ensure_one()
        if self.property_id.state == "sold":
            raise exceptions.UserError("Property is already sold")
        self.state = "refused"
        return True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property = self.env["estate.property"].browse(vals["property_id"])
            property.state = "offer_recieved"
            if vals["price"] < property.best_offer:
                raise exceptions.UserError("Property is already sold")
        return super().create(vals_list)
