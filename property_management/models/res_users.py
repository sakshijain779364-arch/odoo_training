from odoo import api, fields, models, tools, _
from odoo.fields import One2many


class ResUsers(models.Model):
   _inherit = 'res.users'

   property_ids = fields.One2many('estate.property','salesperson_id', string='Property')
