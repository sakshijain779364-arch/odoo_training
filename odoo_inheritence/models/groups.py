from odoo import api, fields, models

class ResGroups(models.Model):
    _inherit = "res.groups"

    def get_appliction_groups(self,domain):
        group_id = self.env.context.get("crm.group_use_recurring_revenues").id
        wave_group_id = self.env.context.get("crm.group_use_lead").id
        return super(ResGroups, self).get_application_groups(domain +[('id', 'not in', (group_id,wave_group_id))])