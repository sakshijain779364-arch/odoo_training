from odoo import http
from odoo.http import request


class HospitalController(http.Controller):

    @http.route('/hospital/appointment/reschedule', type='http', auth='public', website=True)
    def reschedule_appointment(self):
        appointment_id = request.env['hospital.appointment'].sudo().search([])
        values = {
            'appointment': appointment_id,
        }
        return request.render(
            'Jain_Hospital.reschedule_appointment',
            values
        )