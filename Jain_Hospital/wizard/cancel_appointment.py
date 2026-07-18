
import datetime
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class CancelAppointment(models.TransientModel):
    _name = "cancel.appointment"
    _description = "Cancel Appointment"

    @api.model
    def default_get(self, fields):
        res = super(CancelAppointment, self).default_get(fields)
        res['date_cancel'] = datetime.date.today()
        if self.env.context.get('active_id'):
            res['appointment_id'] = self.env.context.get('active_id')
        return res

    appointment_id = fields.Many2one('hospital.appointment', string="Appointment", required=True,
                                     domain=[('state', '=', 'draft')])
    reason = fields.Text(string="Reason")
    date_cancel = fields.Date(string="Cancellation Date")

    def action_cancel(self):
        cancel_days = self.env['ir.config_parameter'].get_param('Jain_Hospital.cancel_days')
        allowed_date = self.appointment_id.appointment_date - relativedelta(days=int(cancel_days))
        # if cancel_days != 0 and allowed_date < date.today():
        if allowed_date < fields.Datetime.now():
            raise ValidationError("Sorry, cancellation is not allowed on the same day of appointment!")
        self.appointment_id.state = 'cancel'
        # return {
        #     'type': 'ir.actions.client',
        #     'tag': 'reload',
        # }
        #


