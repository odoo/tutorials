from odoo import fields, models


class DentalStage(models.Model):

    _name = "dental.stage"
    _description = "dental stages"

    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer(default=1, string="Sequence")