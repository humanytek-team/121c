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
        if self.stage_id.sequence > self._origin.stage_id.sequence:
            return {
                'warning': {
                    'title': 'Stage advanced',
                    'message': 'Do you register your hours?',
                }
            }
