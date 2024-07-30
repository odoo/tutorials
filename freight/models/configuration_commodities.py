from odoo import api, models, fields
from odoo.exceptions import ValidationError


class ConfigurationCommodities(models.Model):
    _name = "configuration.commodities"
    _description = "this is Configuration Commodities"

    name = fields.Text(string="Name")
    hs_code = fields.Char(string='HS Code')
    import_tax_number = fields.Float(string='Import Tax Number (%)', digits='Percent')
    vat = fields.Float(string='VAT (%)', digits='Percent')
    tag_id = fields.Many2one('configuration.freight.tags', string='Tag')
    commodity_group_id = fields.Many2one('configuration.commodity.group', string='Commodity Group')
    commodity_req = fields.Selection([
            ('dry', 'DRY'),
            ('reefer', 'Reefer'),
            ('imo', 'IMO')
        ], string='Commodity Req.', multiple=True)
    status = fields.Boolean(string='Status', default=True)

    industry_id = fields.Many2one('res.partner.industry', string='Industry')
    created_by_id = fields.Many2one('res.users', string='Created by', readonly=True, default=lambda self: self.env.user)
    created_on = fields.Datetime(string='Created on', readonly=True, default=fields.Datetime.now)
    last_updated_by_id = fields.Many2one('res.users', string='Last Updated by', readonly=True)
    last_updated_on = fields.Datetime(string='Last Updated on', readonly=True)

    import_approval_description_ids = fields.One2many(
        comodel_name='approval.description',
        inverse_name='commodity_data_id',
        string='Import Approval Descriptions'
    )

    export_approval_description_ids = fields.One2many(
        comodel_name='app.des',
        inverse_name='commodity_data_id',
        string='Export Approval Descriptions'
    )

    import_customs_description_ids = fields.One2many(
        comodel_name='customs.description',
        inverse_name='commodity_data_id',
        string='Import Customs Descriptions'
    )

    export_customs_description_ids = fields.One2many(
        comodel_name='cus.des',
        inverse_name='commodity_data_id',
        string='Export Customs Descriptions'
    )

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
            print(hs_code_parts)
            if len(hs_code_parts) != 5:
                raise ValidationError('HS Code must be split into 5 groups.')

            for part in hs_code_parts:
                if len(part) != 2 or not part.isdigit():
                    raise ValidationError('Each part of HS Code must be exactly 2 digits.')
                if int(part) % 2 != 0:
                    raise ValidationError('HS Code must contain only even numbers.')
