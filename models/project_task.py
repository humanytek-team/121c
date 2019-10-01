from odoo import api, fields, models, _


class ProjectTask(models.Model):
    _inherit = 'project.task'

    date_deadline = fields.Datetime(
    )
    remaining_hours_to_deadline = fields.Float(
        compute='_compute_remaining_hours_to_deadline',
        # store=True,
        # readonly=True,
    )

    def _compute_remaining_hours_to_deadline(self):
        for task in self:
            if task.date_deadline:
                task.remaining_hours_to_deadline = (task.date_deadline - fields.Datetime.now()).total_seconds() / 60 / 60 # secods / minutes / hours
    
    @api.onchange('stage_id')
    def _on_change_stage(self):
        if self._origin.stage_id.name == 'WIP' and self.stage_id.name == 'Review':
            return {
                'warning': {
                    'title': _('Stage advanced'),
                    'message': _('Did you register your hours?'),
                }
            }
    
    @api.model
    def create(self, vals):
        task = super(ProjectTask, self).create(vals)
        task.sudo().message_follower_ids.unlink()
        return task

    @api.multi
    def message_subscribe(self, partner_ids=None, channel_ids=None, subtype_ids=None):
        res = super(ProjectTask, self).message_subscribe(partner_ids, channel_ids, subtype_ids)
        self.project_id.message_subscribe(partner_ids=self.message_partner_ids.ids, subtype_ids=[1])
        return res
