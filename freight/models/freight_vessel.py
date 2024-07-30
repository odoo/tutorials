from odoo import models, fields


class FreightVessel(models.Model):
    _name = "freight.vessel"
    _description = "this is freight vessel"

    code = fields.Char(string="Code")
    name = fields.Char(string="Name")
    vessel_owner_id = fields.Many2one("res.partner", string="Vessel Owner")
    status = fields.Boolean(string='Status', default=True)
