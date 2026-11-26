from odoo import api, models, fields


class EstatePropertyOfferModel(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer Model"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        copy=False
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline",
                                inverse="_compute_validity_from_deadline")
    partner_id = fields.Many2one(comodel_name='res.partner', required=True)
    property_id = fields.Many2one(
        comodel_name='estate.property', required=True)

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'The Price must be strictly positive!'
    )

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            create_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = fields.Date.add(create_date, days=record.validity)

    def _compute_validity_from_deadline(self):
        for record in self:
            create_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - create_date).days

    def offer_accepted(self):
        self.ensure_one()

        self.status = 'accepted'
        self.property_id.buyer_id = self.partner_id
        self.property_id.selling_price = self.price

        existing_offers = self.property_id.offer_ids - self
        if existing_offers:
            existing_offers.status = 'refused'

    def offer_refused(self):
        self.ensure_one()
        self.status = 'refused'
