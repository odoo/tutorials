from odoo import api, exceptions, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float(required=True)
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')], readonly=True)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(
        string="Validity (days)",
        default=7,
    )
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        string="Deadline",
    )
    property_type_id = fields.Many2one('estate.property.type', related='property_id.property_type_id')

    _offer_price_positive_constraint = models.Constraint(
        "CHECK (price > 0)",
        "An offer price must be positive",
    )

    @api.model
    def create(self, vals_list):
        for val in vals_list:
            best_price = self.env['estate.property'].browse(val.get('property_id')).best_price
            if best_price >= val.get('price'):
                raise exceptions.UserError(f'The offer must be higher than {best_price}')
        return super().create(vals_list)

    def _inverse_date_deadline(self):
        for record in self:
            date_created = fields.Date.to_date(record.create_date) if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - date_created).days

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            date_created = fields.Date.to_date(record.create_date) if record.create_date else fields.Date.today()
            record.date_deadline = fields.Date.add(date_created, days=record.validity)

    def action_confirm(self):
        if any(offer.status == 'accepted' for offer in self.property_id.offer_ids):
            raise exceptions.UserError("Only one offer can be accepted at a time")
        self.status = 'accepted'
        self.property_id.state = 'accept'
        self.property_id.buyer_id = self.partner_id
        self.property_id.selling_price = self.price
        return True

    def action_refuse(self):
        self.status = 'refused'
        # Next part can be used to reset buyer_id and selling_price when refusing an already accepted offer
        if not any(offer.status == 'accepted' for offer in self.property_id.offer_ids):
            self.property_id.buyer_id = False
            self.property_id.selling_price = 0
        return True
