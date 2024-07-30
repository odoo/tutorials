from odoo import fields, models


class ApprovalImportDescription(models.Model):
    _name = "approval.import.description"
    _description = "Import Description Model"

    import_id = fields.Many2one(
        comodel_name="freight.commodity.data",
    )
    description_import_approval = fields.Char("Description")


class ApprovalExportDescription(models.Model):
    _name = "approval.export.description"
    _description = "Import Description Model"

    import_id = fields.Many2one(
        comodel_name="freight.commodity.data",
    )
    description_export_approval = fields.Char("Description")


class CustomsImportDescription(models.Model):
    _name = "customs.import.description"
    _description = "Import Description Model"

    import_id = fields.Many2one(
        comodel_name="freight.commodity.data",
    )
    description_import_customs_req = fields.Char("Description")


class CustomsExportDescription(models.Model):
    _name = "customs.export.description"
    _description = "Import Description Model"

    import_id = fields.Many2one(
        comodel_name="freight.commodity.data",
    )
    description_export_customs_req = fields.Char("Description")
