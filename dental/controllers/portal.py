import math
import logging
from odoo.http import Controller, route, request


class PortalDental(Controller):

    @route(
        ["/my/dental", "/my/dental/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_dental(self, page=1, per_page=6, **kw):
        page = int(page)
        per_page = int(per_page)
        offset = (page - 1) * per_page
        limit = per_page
        patients = request.env["dental.patients"].search([], limit=limit, offset=offset)
        total_patinets = patients.search_count([])
        total_pages = math.ceil(total_patinets / per_page)
        pager = {
            "url": "/my/dental/page/" + str(page),
            "total": total_patinets,
            "current_page": page,
            "total_page": total_pages,
            "step": per_page,
        }
        values = {"patinets": patients, "pager": pager}
        return request.render("dental.dental_patient_template", values)

    @route("/my/dental/<string:name>/<int:patient_id>", type="http", auth="user", website=True)
    def portal_dental_patients(self, patient_id, **kw):
        patients = request.env["dental.patients"].browse(patient_id)
        values = {"patinets": patients}
        return request.render("dental.dental_individual_patient_template", values)

    @route(
        "/my/dental/<string:name>/<int:patient_id>/<string:data>",
        type="http",
        auth="user",
        website=True,
    )
    def portal_dental_patient_data(self, patient_id, data, **kw):
        patient = request.env["dental.patients"].browse(patient_id)
        if not patient.exists():
            return request.render("website.page_404", {})
        elif data == "dentalhistory":
            patient_history = self.get_patient_dental_history_appointment(patient)
            values = {
                "patient": patient,
                "patient_history": patient_history,
            }
            return request.render("dental.dental_patient_history_template", values)
        else:
            return request.render("website.page_404", {})

    def get_patient_dental_history_appointment(self, patient):
        logging.info("Patient dental history fetching...")
        return request.env["dental.history"].search([("patient", "=", patient.id)])
