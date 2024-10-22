from odoo import api, fields, models


class Estate(models.Model):
    _name = "estate.estate"
    _description = "This is the estate model."

    address = fields.Char(compute="_compute_address")
    status_id = fields.Many2one("estate.status")
    price = fields.Float()
    bed = fields.Integer()
    bath = fields.Integer()
    street = fields.Char()
    city_id = fields.Many2one("res.city")
    house_size = fields.Float()
    is_archived = fields.Boolean(default=False)

    @api.depends("street", "city_id")
    def _compute_address(self):
        for record in self:
            record.address = f"{record.street}, {record.city_id.name}, {record.city_id.country_id.name}"


class Status(models.Model):
    _name = "estate.status"
    _description = "This is the description."

    name = fields.Char(required=True)