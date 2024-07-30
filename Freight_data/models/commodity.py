from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class Commodity(models.Model):
    _name = 'commodity'
    _description = 'Commodity'

    name = fields.Char(string='Name', required=True)
    hscode = fields.Char(string='HsCode', required=True, placeholder="84 02 39 00 00")
    import_tax = fields.Float(string='Import Tax (%)', required=True)
    vat = fields.Float(string='VAT (%)', required=True)
    tag_id = fields.Many2many('freight.tags', string='Tag')
    commodity_group_id = fields.Many2one('commodity.group', string='Commodity Group')
    commodity_req = fields.Selection([
        ('dry', 'DRY'),
        ('reefer', 'Reefer'),
        ('imo', 'IMO')
    ], string='Commodity Requirements', required=True)
    import_approval = fields.Char(string="Import Approval")
    export_approval = fields.Char(string="Export Approval")
    import_customs_req = fields.Char(string="Import customs req")
    export_customs_req = fields.Char(string="Export customs req")
    created_by = fields.Many2one("res.users", string="Created By")
    created_on = fields.Char(string="Created on")
    industry = fields.Char(string="Industry")
    last_updated_by = fields.Char(string="Last updated by")
    last_updated_on = fields.Char(string="Last updated on")

    @api.constrains('hscode')
    def _check_hscode(self):
        for record in self:
            if not re.match(r'^(\d{2} ){4}\d{2}$', record.hscode):
                raise ValidationError("HsCode must be in the format of five pairs of even numbers separated by spaces. Example: 84 02 39 00 00")
