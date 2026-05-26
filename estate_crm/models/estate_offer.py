from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _inherit = 'estate.property.offer'

    lead_id = fields.Many2one('crm.lead')

    # def create(self):
    #     self.env['crm.lead'].create({
    #             'name': 'mohit',
    #             })
    #
    #     super().create()

    @api.model_create_multi
    def create(self, vals_list):
        # breakpoint()
        record = super().create(vals_list)

        for rec in record:
            rec.lead_id = self.env['crm.lead'].create({
                    'name': rec.partner_id.name,
                    'partner_id': rec.partner_id.id,
                    'email_from': rec.partner_id.email,
                    })
            # print(rec.lead_id)

        return record

    def action_accept(self):
        c = super().action_accept()
        # self.env['crm.stage'].create({
        #         'is_won':'True',
        #         'fold':'f',
        #     })
        # # a = super().action_set_won()

        # self.lead_id.action_set_won()
        # self.lead_id.stage_id.name
        for rec in self:
            if rec.lead_id:
                rec.lead_id.action_set_won()
        for i in self.property_id.offer_ids:
            if i.status == 'refused':
                i.lead_id.action_set_lost()

        return c

    def action_refuse(self):
        for j in self:
            if j.lead_id:
                j.lead_id.action_set_lost()
        return super().action_refuse()
