from odoo import api, fields, models
from odoo.exceptions import ValidationError


class CommodityData(models.Model):
    _name = 'commodity.data'
    _description = 'Commodity Data'

    name = fields.Char(string='Name', required=True)
    hs_code = fields.Char(string='HsCode', required=True, placeholder='84 02 34 00 00')
    import_tax_number = fields.Float(string='Import Tax Number %')
    vat = fields.Float(string='VAT %')
    tag = fields.Many2one('freight.tags', string='Tag')
    commodity_group = fields.Many2one('commodity.group', string='Commodity Group', domain="[('status', '=', True)]")
    commodity_req = fields.Selection([
        ('dry', 'DRY'),
        ('reefer', 'Reefer'),
        ('imo', 'IMO')
    ], string='Commodity Req.', multiple=True)
    status = fields.Boolean(string='Status', default=True)

    import_approval_description_ids = fields.One2many(
        comodel_name='approval.import.description',
        inverse_name='commodity_data_id',
        string='Import Approval Descriptions'
    )

    export_approval_description_ids = fields.One2many(
        comodel_name='approval.export.description',
        inverse_name='commodity_data_id',
        string='Export Approval Descriptions'
    )

    import_customs_description_ids = fields.One2many(
        comodel_name='customs.import.description',
        inverse_name='commodity_data_id',
        string='Import Customs Descriptions'
    )

    export_customs_description_ids = fields.One2many(
        comodel_name='customs.export.description',
        inverse_name='commodity_data_id',
        string='Export Customs Descriptions'
    )

    created_by = fields.Many2one('res.users', string='Created by', default=lambda self: self.env.user, readonly=True)
    created_on = fields.Datetime(string='Created on', default=fields.Datetime.now, readonly=True)
    industry_id = fields.Many2one('res.partner.industry', string='Industry')
    last_updated_by = fields.Many2one('res.users', string='Last Updated by', default=lambda self: self.env.user, readonly=True)
    last_updated_on = fields.Datetime(string='Last Updated on', default=fields.Datetime.now, readonly=True)

    @api.model
    def create(self, vals):
        vals['created_by'] = self.env.user.id
        vals['last_updated_by'] = self.env.user.id
        return super().create(vals)

    def write(self, vals):
        vals['last_updated_by'] = self.env.user.id
        vals['last_updated_on'] = fields.Datetime.now()
        return super().write(vals)

    @api.constrains('hs_code')
    def _check_hs_code(self):
        for record in self:
            if not record.hs_code or not all(int(digit) % 2 == 0 for digit in record.hs_code if digit.isdigit()) or len(record.hs_code.replace(' ', '')) != 10:
                raise ValidationError("HsCode must be five even numbers, e.g., 00 00 00 00 00")
