from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _check_offer_price = models.Constraint(
        'CHECK(price > 0)',
        'The offer price should be stricly positive'
    )

    price = fields.Float()
    status = fields.Selection(
        string="Status",
        copy=False,
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ]
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)

    @api.onchange("date_deadline")
    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.today()).days

    def action_accept_offer(self):
        for record in self:
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            for offer in record.property_id.offer_ids:
                offer.status = "refused"
            record.status = 'accepted'
        return True

    def action_refuse_offer(self):
        for record in self:
            if record.status == 'accepted':
                record.property_id.selling_price = 0.0
                record.property_id.buyer_id = None
            record.status = 'refused'
        return True
    
    @api.ondelete(at_uninstall=False)
    def _unlink_if_deleted(self):
        print("#"*100)
        for record in self:
            print(record)
            record.property_id.selling_price = 0.0
