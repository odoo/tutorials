from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class DentalPortal(CustomerPortal):

    @http.route(['/my/dental', '/my/dental/page/<int:page>'], type='http', auth='user', website=True)
    def portal_my_dental(self, page=1, **kw):
        domain = [('guarantor_id', '=', request.env.user.id)]
        dental_patients = request.env['dental.patient'].search_count(domain)

        pager = request.website.pager(
            url='/my/dental',
            total=dental_patients,
            page=page,
            step=6,
        )
        patients = request.env['dental.patient'].search(
            domain, limit=6, offset=pager['offset'])
        return request.render('dental.portal_my_dental', {
            'patients': patients,
            'pager': pager,
        })

    @http.route('/my/dental/<int:patient_id>', type='http', auth='user', website=True)
    def portal_my_dental_user(self, patient_id, **kw):
        patient = request.env['dental.patient'].browse(patient_id)
        return request.render('dental.portal_my_dental_user', {
            'patient': patient
        })

    @http.route('/my/dental/<int:patient_id>/<string:data>', type='http', auth='user', website=True)
    def portal_my_dental_info(self, patient_id, data, **kw):
        patient = request.env['dental.patient'].browse(patient_id)
        if data == "personal":
            return request.render('dental.portal_my_dental_personal', {
                'patient': patient
            })

        elif data == "medical_aid":
            medical_aid = patient.medical_aid_id
            return request.render('dental.portal_my_dental_medical_aid', {
                'medical_aid': medical_aid
            })

        elif data == "dental_history":
            dental_history = request.env['dental.medical.history'].search([('patient_id', '=', patient_id)])

            return request.render('dental.portal_my_dental_dental_history', {
                'dental_history': dental_history,
            })

        elif data == "medical_history":
            dental_history = request.env['dental.medical.history'].search([('patient_id', '=', patient_id)])

            return request.render('dental.portal_my_dental_medical_history', {
                'medical_history': dental_history
            })

        return request.render("website.page_404", {})

    @http.route('/my/dental/<int:patient_id>/dental_history/<int:history_id>', type='http', auth='user', website=True)
    def portal_my_dental_medical_history_form(self, patient_id, history_id, **kw):
        dental_histories = request.env['dental.medical.history'].search([('patient_id', '=', patient_id)])
        dental_history = dental_histories.browse(history_id)
        return request.render('dental.portal_my_dental_medical_history_form', {
            'dental_history': dental_history,
        })
