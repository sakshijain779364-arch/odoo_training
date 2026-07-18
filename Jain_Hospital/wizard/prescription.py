from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import ValidationError

class HospitalPrescription(models.TransientModel):
    _name = 'hospital.prescription'
    _description = 'Hospital Prescription'
    _rec_name = 'name'

    name = fields.Char(string='Prescription Reference', required=True, copy=False, default='New')
    patient_id = fields.Many2one('hospital.patient', string='Patient')
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor')
    # appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
    date = fields.Date(default=fields.Date.today)
    notes = fields.Text(string='Doctor Notes')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('issued', 'Issued'),
        ('cancel', 'Cancelled')
    ], default='draft', string='State')

    line_ids = fields.One2many('hospital.prescription.line', inverse_name='prescription_id', string='Medicines')
    total_medicines = fields.Integer(compute='_compute_total_Medicines', string='Total Medicines')

    # @api.depends('line_ids')
    # def _compute_total_Medicines(self):
    #     for rec in self:
    #         rec.total_medicines = len(rec.line_ids)
    #
    # def action_issue(self):
    #     for rec in self:
    #         rec.state = 'issued'
    #
    # def action_cancel(self):
    #     for rec in self:
    #         rec.state = 'cancel'

    def action_send_appoinment(self):
        return True

    def action_save(self):
        self.ensure_one()
        appointment = self.env['hospital.appointment'].browse(self.env.context.get('appointment_id'))
        prescription_data = []
        for line in self.line_ids:
            prescription_data.append((0, 0,{
                'medicine_name': line.medicine_name,
                'dosage': line.dosage,
                'duration': line.duration,
                'instruction': line.instruction,
            }))

        if prescription_data:
            appointment.write({
                'line_ids': prescription_data
            })
        return {'type': 'ir.actions.act_window_close'}


class HospitalPrescriptionLine(models.TransientModel):
    _name = 'hospital.prescription.line'
    _description = 'Hospital Prescription Line'
    _rec_name = 'medicine_name'

    prescription_id = fields.Many2one('hospital.prescription', ondelete='cascade')
    sale_order_id = fields.Many2one('sale.order', string="Sale Order", ondelete='cascade')
    medicine_name = fields.Char(string='Medicine Name', required=True)
    dosage = fields.Char(string='Dosage')
    duration = fields.Integer(string='Days')
    instruction = fields.Text(string='Instruction')
    appointment_id = fields.Many2one('hospital.appointment',string='Appointment')


