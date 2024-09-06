from odoo import models, fields


class DentalStage(models.Model):

    _name = "dental.stage"
    _description = "Dental stage"

    name = fields.Char()
    sequence = fields.Integer('Sequence', default=1)
