from odoo import http
from odoo.http import request


class WebsiteProperty(http.Controller):

    @http.route("/my/dental", auth="public", website=True)
    def display_patients(self, **kwargs):

        patients = http.request.env["dental.patients"].search([('guarantor_id', '=', request.env.user.partner_id.id)])
        return http.request.render(
            "dental.dental_patient_website", {"patients": patients }
        )
    
    @http.route("/patient/<int:patient_id>", auth="public", website=True)
    def display_patient_details(self, patient_id):
        patient = request.env['dental.patients'].sudo().browse(patient_id)

        if not patient:
            return request.not_found()

        return request.render("dental.dental_patient_details_page", {
            "patient": patient
        })
