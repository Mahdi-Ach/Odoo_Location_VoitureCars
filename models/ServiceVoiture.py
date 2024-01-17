from odoo import api, fields, models, _
class ServiceVoiture(models.Model):
    _name = 'location_cars.service'
    _description = 'Services des vehicules'
    _rec_name = 'reference_service'

    description = fields.Char('Description', required=True)
    type_service_id = fields.Many2one('location_cars.type', 'Type du Service',copy=True, required=True)
    cout = fields.Monetary('Cout', required=True)
    reference_service = fields.Char('Service Reference', required=True)
    notes = fields.Text(required=True)
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', required=True)
    contract_id = fields.Many2one('location_cars.contract', string='Contrat', help='Vehicle concerned by this log',default=lambda self : self._context.get('contract_id'), ondelete='cascade', required=True)
    _sql_constraints = [
        ('unique_reference_service', 'unique(reference_service)', 'reference service must be unique!'),
    ]