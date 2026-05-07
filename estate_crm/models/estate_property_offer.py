from odoo import api, models, fields


class EstatePropertyOffer(models.Model):
    _inherit = "estate.property.offer"

    lead_id = fields.Many2one("crm.lead")

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            new_lead = self.env['crm.lead'].create({
                'name':  f'Offer By {record.partner_id.name}',
                'expected_revenue' : record.price,
                'partner_id': record.partner_id.id,
                'user_id': record.property_id.salesperson_id.id,
                'email_from': record.partner_id.email,
                'phone': record.partner_id.phone,
                'date_deadline': record.date_deadline,
                # 'offer_ids': record.lead_id.id
            })
            record.lead_id = new_lead.id
        return records

    def action_accept(self):
        xyz = super().action_accept()
        for record in self:
            if record.lead_id:
                record.lead_id.action_set_won()
            # leads = self.env['crm.lead'].search([
            #     ('partner_id', '=', record.partner_id.id),
            #     ('expected_revenue', '=', record.price)
            # ])      
            # for lead in leads:
            #     lead.action_set_won()

            
            remaining = (record.property_id.offer_ids - record)
            for other in remaining:
                if other.lead_id:
                    other.lead_id.action_set_lost()
                # losts = self.env['crm.lead'].search([
                #     ('partner_id', '=', other.partner_id.id),
                #     ('expected_revenue', '=', other.price)
                # ])
                # for lost in losts:
                #     lost.action_set_lost()
        return xyz

    def action_refuse(self):
        abc = super().action_refuse()
        for record in self:
            if record.lead_id:
                record.lead_id.action_set_lost()
            # leads = self.env['crm.lead'].search([
            #     ('partner_id', '=', record.partner_id.id),
            #     ('expected_revenue', '=', record.price)
            # ])
                    
            # for lead in leads:
            #     lead.action_set_lost()

        return abc
