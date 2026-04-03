from odoo import api, models, fields


class Portal(models.Model):
    _name = "portal"
    _description = "portal model"
    #_inherit = "res.partner"

    name = fields.Char(default="test name",required=True)