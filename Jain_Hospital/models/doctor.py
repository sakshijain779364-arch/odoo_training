from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Doctor'
    _rec_name = 'name'

    _sql_constraints = [
        ('unique_doctor_name', 'UNIQUE(first_name, last_name)',
         'The combination of First Name and Last Name must be unique!'),
    ]
    
    name = fields.Char(string='First Name', required=True)
    name_2 = fields.Char(string='Last Name', required=True)
    specialization = fields.Char(string='Specialization', required=True)
    active = fields.Boolean(default=True)
    doctor_availability = fields.Boolean(default=True)
    available = fields.Boolean(string="Available", default=True)
    away = fields.Boolean(string="Away", default=False)

    def action_available(self):
        if not self.doctor_availability:
            self.doctor_availability = True
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Success',
                    'message': 'Doctor is available!',
                    'type': 'success',
                    'sticky': False,
                }
            }

    def action_away(self):
        if self.doctor_availability:
            self.doctor_availability = False
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Success',
                    'message': 'Doctor is away!',
                    'type': 'success',
                    'sticky': False,
                }
            }

        @api.returns('self')
        def copy(self, default=None):
            if default is None:
                default = {}
            if not default.get('name'):
                default['name'] = self.name + "(copy)"
                return super(HospitalDoctor, self).copy(default=default)
