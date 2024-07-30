from odoo import api, models, fields
from odoo.exceptions import ValidationError


class Commodity(models.Model):
    _name = 'commodity'
    _description = 'Commodities'

    name = fields.Char(string='Name', required=True)
    hs_code = fields.Char(string='HS Code', required=True, placeholder='84 02 32 00 00')
    import_tax_number = fields.Float(string='Import Tax Number (%)')
    vat = fields.Float(string='VAT (%)')
    tag = fields.Many2one('freight.tag', string='Tag')
    commodity_group = fields.Many2one('commodity.group', string='Commodity Group')
    commodity_req = fields.Many2many('commodity.req', string='Commodity Requirements')
    status = fields.Boolean(string='Status', default=True)

    import_approvals_ids = fields.One2many('approvals', 'commodity_id', string='import')
    export_approvals_ids = fields.One2many('approvals', 'commodity_id', string='export')
    import_customs_req_ids = fields.One2many('customs.req', 'commodity_id', string='import')
    export_customs_req_ids = fields.One2many('customs.req', 'commodity_id', string='export')

    created_by = fields.Many2one('res.users', string='Created by', readonly=True, default=lambda self: self.env.user)
    created_on = fields.Datetime(string='Created on', readonly=True, default=fields.Datetime.now)
    industry = fields.Many2one('res.partner.industry', string='Industry')
    last_updated_by = fields.Many2one('res.users', string='Last Updated by', readonly=True)
    last_updated_on = fields.Datetime(string='Last Updated on', readonly=True)

    @api.constrains('hs_code')
    def _check_hs_code(self):
        for record in self:
            hs_code = record.hs_code.strip()
            if not hs_code:
                continue
            hs_code_digits = hs_code.replace(' ', '')
            if len(hs_code_digits) != 10 or not hs_code_digits.isdigit():
                raise ValidationError('HS Code must be exactly 10 digits.')

            hs_code_parts = hs_code.split()
            if len(hs_code_parts) != 5:
                raise ValidationError('HS Code must be split into 5 groups.')

            for part in hs_code_parts:
                if len(part) != 2 or not part.isdigit():
                    raise ValidationError('Each part of HS Code must be exactly 2 digits.')
                if int(part) % 2 != 0:
                    raise ValidationError('HS Code must contain only even numbers.')

    @api.model
    def create(self, vals):
        vals['created_by'] = self.env.user.id
        vals['created_on'] = fields.Datetime.now()
        return super().create(vals)

    def write(self, vals):
        vals['last_updated_by'] = self.env.user.id
        vals['last_updated_on'] = fields.Datetime.now()
        return super().write(vals)
