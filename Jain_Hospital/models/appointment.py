from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Appointment'
    _rec_name = 'appointment_sequence'
    _order = 'patient_id asc,id desc'

    appointment_sequence = fields.Char(string='Appointment Sequence')
    appointment_number = fields.Char(string='Appointment Number', required=True, copy=False, readonly=True,
                                     default='New')
    appointment_date = fields.Date(string='Appointment Date',default=fields.Date.today())
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True, ondelete='restrict')
    gender = fields.Selection(string='Gender', related='patient_id.gender')
    appointment_date = fields.Datetime(string='Appointment Time', default=fields.Datetime.now)
    prescription = fields.Html(string='Prescription')
    pharmacy_details = fields.Html(string='Pharmacy')
    priority = fields.Selection([
        ('0', 'Normal'), ('1', 'Low'), ('2', 'High'), ('3', 'Very High')], string='Priority', default='0')
    state = fields.Selection([('draft', 'Draft'), ('consultation', 'Consultation'), ('done', 'Done'),
                              ('cancel', 'Cancelled')], default='draft', string='Status', required=True)
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', required=True, domain="[('away', '=', False)]")
    hide_pharmacy_price = fields.Boolean(string='Hide Pharmacy Price')
    sale_order_id = fields.Many2one('sale.order', string="Sale Order")
    line_ids = fields.One2many('hospital.prescription.line',inverse_name='appointment_id', string='Prescription Lines')


    def unlink(self):
        print("Test...........")
        if self.state =='done':
            raise ValidationError(("you cannot delete appointment with 'done' status !"))
        return super(HospitalAppointment, self).unlink()


    def action_test(self):
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'click Successful!',
                'type': 'rainbow_man',
            }
        }

    def action_send_appointment(self):
        mail_template = self.env.ref('Jain_Hospital.mail_template_schedule_appointment')
        if mail_template:
            mail_template.send_mail(self.id, force_send=True)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': 'Appointment confirmation email has been sent successfully!',
                'type': 'success',
                'sticky': False,
            }
        }

    def send_appointment_reminder(self):
        appointments = self.search([('appointment_date', '<', fields.Date.today())])
        mail_template = self.env.ref('Jain_Hospital.mail_template_appointment_missed')
        for record in appointments:
            if mail_template and record.state != 'done':
                mail_template.sudo().send_mail(record.id, force_send=True)
        return True


    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            sequence_id = self.env.ref("Jain_Hospital.appointment_numbers").ids
            if sequence_id:
                record_name = self.env["ir.sequence"].browse(sequence_id).next_by_id()
            else:
                record_name = "/"
            val.update({"appointment_sequence": record_name or ""})
        return super(HospitalAppointment, self).create(vals)

    def action_consulation(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'consultation'

    def action_done(self):
        for rec in self:
            if rec.state == 'consultation':
                rec.state = 'done'

    # def open_form(self):
    #         return

    def action_create_bill(self):
        self.ensure_one()
        partner_id = self.env["res.partner"].create({'name':self.patient_id.name})
        res_id = self.sale_order_id.id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sale Order',
            'res_model': 'sale.order',
            'res_id': res_id,
            'view_mode': 'form',
            'target': 'current',
            'context': {'default_partner_id': partner_id.id},
        }


    def action_add_prescription(self):
        self.ensure_one()

        return {
            'name': 'New Prescription',
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.prescription',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'appointment_id': self.id,
            }
        }


class AppointmentPharmacyLines(models.Model):
    _name = "appointment.pharmacy.lines"
    _description = "Appointment Pharmacy Lines"

    drug_name = fields.Many2one('product.product', string='Drug Name')
    price_unit = fields.Float(string='Price')
    qty = fields.Integer(string='Quantity')