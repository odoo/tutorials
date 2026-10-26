from odoo import api, exceptions, fields, models


class Offer(models.Model):
    _name = "estate.property.offer"
    _description = "Property offer"
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection(
        copy=False,
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')]
    )
    validity = fields.Integer(default=7, compute="_inverse_date_deadline", inverse="_compute_date_deadline")
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id")

    _price_check = models.Constraint('CHECK(price >= 0)', 'An offer price must be strictly positive')

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            base_date = record.create_date or fields.Date.today()
            record.date_deadline = fields.Date.add(base_date, days=record.validity)

    @api.depends("date_deadline", "validity")
    def _inverse_date_deadline(self):
        for record in self:
            if (fields.Date.today() < record.date_deadline):
                record.validity = (record.date_deadline - fields.Date.today()).days
            else:
                record.validity = 0

    @api.model
    def create(self, vals_list):
        properties_ids = self.env['estate.property'].browse([item.get('property_id') for item in vals_list])
        properties_set = {p.id: p for p in properties_ids}

        for vals in vals_list:
            property = properties_set.get(vals.get('property_id'))
            if (vals['price'] < max(property.offer_ids.mapped('price'), default=0)):
                raise exceptions.UserError("New offers must have a higher price that existing ones")
            property.state = 'offer_received'
            return super().create(vals)

    def action_accepted(self):
        for record in self:
            property = record.property_id

            if ('accepted' in property.offer_ids.mapped('status')):
                raise exceptions.UserError("An offer has already been accepted for this property")

            if (property.state in ('cancelled', 'sold')):
                raise exceptions.UserError("You cannot accept an offer for a property that is sold or cancelled")

            record.status = 'accepted'
            property.buyer_id = record.partner_id
            property.selling_price = record.price
            property.state = 'offer_accepted'
        return True

    def action_refused(self):
        for record in self:
            if (not record.status):
                record.status = 'refused'
        return True
