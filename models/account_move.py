from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = "account.move"

    origin_id = fields.Many2one(
        comodel_name="sale.order",
        compute="_get_sale_order_origin",
    )
    po = fields.Char(related="origin_id.po")

    @api.depends("ref")
    def _get_sale_order_origin(self):
        for r in self:
            r.origin_id = self.env["sale.order"].search([("name", "=", r.ref)], limit=1)
