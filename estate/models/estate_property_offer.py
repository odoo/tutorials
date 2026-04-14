from odoo import fields, models, api


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    name = fields.Char(string="Property Offer", required=True)
    price = fields.Integer(string="Price", required=True)
    status = fields.Selection(string="Status", selection=[("accepted", "Accepted"), ("refused", "Refused")], copy=False)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    # create_date = fields.Date(string="Date for creation")
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_deadline", inverse="_inverse_deadline", readonly=False)

    # It gets changed on each changes because it works based on cache
    @api.depends("create_date", "validity")
    def _compute_deadline(self):
        for records in self:
            default_date = records.create_date.date() if records.create_date else fields.Date.today()
        records.date_deadline = fields.Date.add(default_date, days=records.validity) 

    #Inverse is triggered when the computed field is written (usually during save), not during live editing.
    def _inverse_deadline(self):
        for records in self:
            default_date = records.create_date.date() if records.create_date else fields.Date.today()
            if records.date_deadline:
                records.validity = (records.date_deadline - default_date).days
