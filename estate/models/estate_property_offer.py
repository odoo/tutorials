from odoo import fields, models, api
class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "All the available offer for the property"

    property_id = fields.Many2one("estate.property", required = True)
    price = fields.Float(string = 'Price', required = True)
    buyer_id = fields.Many2one('res.partner', required = True)
    status = fields.Selection(
        string = "Status",
        copy = False,
        selection = [
            ("refuse", "Refuse"),
            ("accepted", "Accepted")
        ],
    )
    validity = fields.Integer(string = 'Validity(days)', default = 7)
    date_deadline = fields.Date(compute = '_compute_date_deadline', inverse = '_inverse_date_deadline')

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date and record.validity:
                record.date_deadline = fields.Date.add(record.create_date, days = record.validity)
            else:
                record.date_deadline = fields.Date.add(fields.Date.today(), days = record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
