from odoo import fields, models

class ResPartnerStatus(models.Model):
    _name = "res.partner.status"
    _description = "Partner Status"
    _order = "sequence, name"

    name = fields.Char(required=True, translate=True)
    code = fields.Char(required=True)  # e.g. EC, PC
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ("code_unique", "unique(code)", "Status code must be unique."),
    ]