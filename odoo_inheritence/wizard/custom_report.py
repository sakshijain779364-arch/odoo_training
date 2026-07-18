from odoo import api, fields, models, tools



class CustomReport(models.TransientModel):
    _name = 'custom.report'

    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)

    def action_print_custom_report(self):
        query=''' SELECT appointment_sequence,patient_id,doctor_id,appointment_date FROM hospital_appointment 
            WHERE appointment_date BETWEEN %s AND %s'''

        self.env.cr.execute(query,(self.start_date, self.end_date))
        report = self.env.cr.dictfetchall()
        for rec in report:
            patient = self.env['hospital.patient'].browse(rec['patient_id'])
            patient_name = patient.name
            doctor = self.env['hospital.doctor'].browse(rec['doctor_id'])
            doctor_name = doctor.name
            res_company = self.env['res.company'].search([], limit=1)
            data = {'date': self.read()[0],'report': report,'res_company': res_company,
                    }
        return self.env.ref('odoo_inheritence.action_custom_report_pdf12').report_action(None, data=data)

        data = self.env.cr.dictfetchall()
        print(data)

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['custom.report'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'custom.report',
            'docs': docs,
            'data': data,
        }