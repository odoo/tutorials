from odoo import api, fields, models


class estatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _descreption = "The offer of estate property"

    price = fields.Float("Price")
    partner_id = fields.Many2one("res.partner", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline (days)",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline"
    )
    property_id = fields.Many2one('estate.property', required=True)
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Datetime.add(record.create_date, days=record.validity)
            else:
                record.date_deadline = fields.Datetime.add(fields.Datetime.today(), days=record.validity)        
    
    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.crate_date).days
            else:
                record.validity = (record.date_deadline - fields.Datetime.today()).days
