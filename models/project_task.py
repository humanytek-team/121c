from odoo import api, fields, models, _


class ProjectTask(models.Model):
    _inherit = "project.task"

    @api.onchange("stage_id")
    def _on_change_stage(self):
        if self._origin.stage_id.name == "WIP" and self.stage_id.name == "Review":
            return {
                "warning": {
                    "title": _("Stage advanced"),
                    "message": _("Did you register your hours?"),
                }
            }
