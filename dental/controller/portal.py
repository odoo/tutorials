from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.portal.controllers.portal import pager as portal_pager


class DentalPortal(CustomerPortal):
    @http.route(['/my/dental', '/my/dental/page/<int:page>'], type='http', auth='user', website=True)
    def portal_my_dental(self, page=1, **kw):
        current = request.env.user.id
        dental_patient = request.env['dental.patient']
        domain = [('guarantor_id', '=', current)]

        items_per_page = 2
        total_users = dental_patient.search_count(domain)

        pager = portal_pager(
            url='/my/dental',
            total=total_users,
            page=int(page),
            step=items_per_page,
        )

        users = dental_patient.search(
            domain,
            limit=items_per_page,
            offset=pager['offset'],
        )

        return request.render('dental.portal_my_dental', {
            'users': users,
            'pager': pager
        })

    @http.route('/my/dental/<int:patient_id>', type='http', auth='user', website=True)
    def portal_my_dental_user(self, patient_id, **kw):
        patient = request.env['dental.patient'].browse(patient_id)
        return request.render('dental.portal_my_dental_user', {
            'patient': patient
        })

    @http.route('/my/dental/<int:patient_id>/personal', type='http', auth='user', website=True)
    def portal_my_dental_personal(self, patient_id, **kw):
        patient = request.env['dental.patient'].browse(patient_id)
        return request.render('dental.portal_my_dental_personal', {
            'patient': patient
        })

    @http.route('/my/dental/<int:patient_id>/medical_history', type='http', auth='user', website=True)
    def portal_my_dental_medical_history(self, patient_id, **kw):
        medical_historys = request.env['medical.history'].search([('patient_id', '=', patient_id)])
        return request.render('dental.portal_my_dental_medical_history', {
            'medical_historys': medical_historys
        })

    @http.route('/my/dental/<int:patient_id>/medical_aid', type='http', auth='user', website=True)
    def portal_my_dental_medical_aid(self, patient_id, **kw):
        medical_aids = request.env['dental.patient'].browse(patient_id).insurance_id
        return request.render('dental.portal_my_dental_medical_aid', {
            'medical_aids': medical_aids
        })

    @http.route('/my/dental/<int:patient_id>/dental_history', type='http', auth='user', website=True)
    def portal_my_dental_dental_history(self, patient_id, **kw):
        medical_historys = request.env['medical.history'].search([('patient_id', '=', patient_id)])
        return request.render('dental.portal_my_dental_dental_history', {
            'medical_historys': medical_historys
        })

    @http.route('/my/dental/<int:patient_id>/dental_history/<int:history_id>', type='http', auth='user', website=True)
    def portal_my_dental_medical_history_form(self, patient_id, history_id, **kw):
        medical_historys = request.env['medical.history'].search(
            [('patient_id', '=', patient_id)])
        medical_history = medical_historys.browse(history_id)
        return request.render('dental.portal_teeth_staining', {
            'medical_history': medical_history,
        })
