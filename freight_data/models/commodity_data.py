from odoo import api, models, fields
from odoo.exceptions import ValidationError


class CommodityData(models.Model):
    _name = "commodity.data"
    _description = "Commodity Data"

    name = fields.Char(string='Name', required=True)
    hs_code = fields.Char(string='HS Code', placeholder='84 02 39 00 00', required=True)
    import_tax_number = fields.Float(string='Import Tax No.(%)')
    vat = fields.Float(string='VAT (%)')
    commodity_group_id = fields.Many2one('commodity.group', string='Commodity Group', required=True, domain="[('status', '=', 'True')]")
    is_selection_ids = fields.Many2many(comodel_name='commodity.request', string='Commodity Request')
    status = fields.Boolean(string='Status', default=True)
    freight_tag_id = fields.Many2one('freight.tags', string='Freight Tag', domain="[('status', '=', 'True')]")

    create_uid = fields.Many2one('res.users', string='Created by', readonly=True, default=lambda self: self.env.user)
    create_date = fields.Datetime(string='Created on', readonly=True, default=fields.Datetime.now)
    write_uid = fields.Many2one('res.users', string='Last Updated by', readonly=True)
    write_date = fields.Datetime(string='Last Updated on', readonly=True)
    industry_id = fields.Many2one('res.partner.industry', string='Industry')

    import_approval_description_ids = fields.One2many(comodel_name='approval.description', inverse_name='commodity_data_id', string='Import Approval Descriptions')
    export_approval_description_ids = fields.One2many(comodel_name='approval.description', inverse_name='commodity_data_id', string='Export Approval Descriptions')
    import_customs_description_ids = fields.One2many(comodel_name='customs.description', inverse_name='commodity_data_id', string='Import Customs Descriptions')
    export_customs_description_ids = fields.One2many(comodel_name='customs.description', inverse_name='commodity_data_id', string='Export Customs Descriptions')

    @api.constrains('hs_code')
    def _check_hs_code(self):
        for commodity_data in self:
            hs_code = commodity_data.hs_code
            if not hs_code or len(hs_code.split()) != 5 or not all(part.isdigit() and int(part) % 2 == 0 for part in hs_code.split()):
                raise ValidationError(
                    "HS Code must consist of five even numbers separated by spaces. Example: 84 02 39 00 00."
                )
