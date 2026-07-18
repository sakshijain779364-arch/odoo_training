from datetime import date

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import ValidationError

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Patient'
    _rec_name = 'name'

    name = fields.Char(string='Name', tracking=True, required=True)
    patient_sequence = fields.Char(string='Patient Sequence')
    appointment_line = fields.One2many('hospital.appointment', inverse_name='patient_id', string='Appointment')
    date_of_birth = fields.Date(string='Date of Birth', required=True)
    # ref= fields.Char(string='Reference', required=False)
    appointment_date = fields.Datetime(string='Appointment Date', compute='_compute_appointment_date')
    age = fields.Integer(string='Age', compute ='_compute_age', inverse='inverse_compute_age',
                         search='search_age', required=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', tracking=True,
                              required=True)
    active = fields.Boolean(string='Active', default=True)

    priority = fields.Selection([('0', 'Normal'), ('0', 'Low'), ('0', 'High'), ('0', 'Very High')], string='Priority')

    state = fields.Selection([('draft', 'Draft'), ('consultation', 'Consultation'), ('done', 'Done'),
                              ('cancel', 'Cancelled')], default='draft', string='Status', required=True)
    # prescription = fields.Html(string='Prescription')
    pharmacy_details = fields.Html(string='Pharmacy')
    image = fields.Image(string='Image')
    tag_ids = fields.Many2many('crm.tag', string='Tags')
    appointment_count = fields.Integer(string='Appointment Count', compute='_compute_appointment_count', store=True)
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string='Appointments')
    parent = fields.Char(string='Parent')
    marital_status = fields.Selection([('married','Married'),('single','Single')],string="Marital Status", tracking=True)
    partner_name = fields.Char(string='Partner Name')
    partner_id = fields.Many2one('res.partner', string='Customer')

    @api.ondelete(at_uninstall=False)
    def _check_appointments(self):
        for rec in self:
            if rec.appointment_ids:
                raise ValidationError(("You cannot delete a patient with appointments !"))

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])


    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.date.today():
                raise ValidationError(("Please enter a valid date of birth"))


    @api.depends('name')
    def _compute_appointment_date(self):
        for record in self:
            if record.name:
                record.appointment_date = fields.Datetime.now() + relativedelta(days=5)
            else:
                record.appointment_date = None

    @api.onchange('age')
    def _onchange_type(self):
        if self.age and self.age <= 0:
            raise ValidationError(("Please enter an age greater than 0."))

    def action_schedule_appointment(self):
        return True

    def action_add_prescription(self):
        return True


    def write(self, vals):
        if not self.patient_sequence and not vals.get('patient_sequence'):
            vals['patient_sequence'] = self.env['ir.sequence'].next_by_id()
        # print("write method is triggered", vals)
        return super(HospitalPatient, self).write(vals)

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            sequence_id = self.env.ref("Jain_Hospital.patient_numbers").id
            if sequence_id:
                record_name = self.env["ir.sequence"].browse(sequence_id).next_by_id()
            else:
                record_name = "/"
            val.update({"patient_sequence": record_name or ""})
        return super(HospitalPatient, self).create(vals)


    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 0

    @api.depends('age')
    def inverse_compute_age(self):
        today = date.today()
        for rec in self:
            rec.date_of_birth = today - relativedelta(years=rec.age)

    def _search_age(self, operation, value):
        date_of_birth = date.today()-relativedelta(years=value)
        print(".......today",date.today())
        return [('date_of_birth', '=', date_of_birth)]


    def name_get(self):
        for record in self:
            name = "%s:%s" % (record.name, record.id)
            return name
        # return [(record.id, "%s:%s" % (record.name, record.id)) for record in self]

    def action_test(self):
        print("Clicked")
        return True

    def open_form(self):
        return

    def action_demo_orm(self):
        # new_record = self.env['hospital.patient'].create({'name':'Anishka',
        #                                                   'date_of_birth':'2003-12-8',
        #                                                   'gender':'female'})
        # new_record = self.env['hospital.patient'].browse(64)
        # print("Gender for browsed record is %s.", new_record.gender)
        new_record = self.env['hospital.patient'].search([('name', '=', 'Anishka')])
        print(new_record.read(['name','age']))
        # print(new_record.mapped('name'))
        # new_record = self.env['hospital.patient'].read([('name', '=', 'state')])
        # 'John Doe' naam ke jitne bhi partners honge, yeh un sabhi ko delete kar dega
        # new_record = self.env['hospital.patient'].search([('name', '=', 'Anishka')]).unlink()
        # new_record = self.env['hospital.patient'].search([('name', '=', 'Anishka')])
        # self.line_ids = self.line_ids.sorted(key=lambda x: r.name)

    def action_view_appointment(self):
        self.ensure_one()
        appointment = (self.env['hospital.appointment'].search([('patient_id', '=', self.id)],
                                                               ))

        if len(appointment) == 1:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Appointment',
                'res_model': 'hospital.appointment',
                'res_id': appointment.id,
                'view_mode': 'form',
                'target': 'current',
            }
        else:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Appointment',
                'res_model': 'hospital.appointment',
                'view_mode': 'list',
                'target': 'current',
            }
