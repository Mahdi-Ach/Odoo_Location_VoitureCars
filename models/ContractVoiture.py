import os
import tempfile
from email.mime.application import MIMEApplication

from pdf2docx import Converter
from werkzeug.wrappers import request

from odoo import api, fields, models, _,exceptions
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import base64
from email import encoders
from werkzeug.wrappers import request  # Import request for response creation

class ContratVoiture(models.Model):
    _name = 'location_cars.contract'
    _description = 'Vehicle Contract'
    _rec_name = 'reference'
    def compute_next_year_date(self, strdate):
        oneyear = relativedelta(years=1)
        start_date = fields.Date.from_string(strdate)
        return fields.Date.to_string(start_date + oneyear)

    date_affectation = fields.Date(string="Date d'affectation", default=fields.Date.context_today, required=True)
    reference = fields.Char('Reference', size=64, required=True)
    responsable = fields.Many2one('res.users', 'Responsible',default=lambda self: self.env.ref('base.user_admin').id, required=True)
    date_debut = fields.Date('Date de début du contrat', default=fields.Date.context_today,
        help='Date when the coverage of the contract begins', required=True)
    date_expiration = fields.Date("Date d'expiration du contrat", default=lambda self:
        self.compute_next_year_date(fields.Date.context_today(self)),
        help='Date when the coverage of the contract expirates (by default, one year after begin date)', required=True)
    days_left = fields.Integer(compute='_compute_days_left', string='Warning Date', required=True)
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', required=True)
    state = fields.Selection([
        ('not_active','Ready to be Active'),
        ('open', 'In Progress'),
        ('expired', 'Expired'),
        ], 'Status', default='not_active', readonly=True,
        help='Choose whether the contract is still valid or not',
        tracking=True,
        compute = '_compute_status',
        copy=False,
        store=True
    )
    notes = fields.Text(help='Write here all supplementary information relative to this contract', copy=False, required=True)
    cout_activation = fields.Monetary(string="Cout d'activation", required=True)
    service_ids = fields.One2many('location_cars.service', 'contract_id', required=True, string='Service', copy=True, ondelete='cascade')
    conducteure_id = fields.Many2one("location_cars.conducteur", string="Conducteur", required=True)
    lieu = fields.Char(string="Lieu",help='Location of the vehicle (garage, ...)', required=True)
    total_service_cost = fields.Monetary(string="Total Service Cost")
    combined_cost = fields.Monetary(string="Combined Cost",compute="_compute_combined_cost",store=True)
    vehicle_id = fields.Many2one('location_cars.vehicule', string='Vehicle', help='Vehicle concerned by this log', ondelete='cascade', required=True)
    _sql_constraints = [
        ('unique_reference', 'unique(reference)', 'reference must be unique!'),
    ]

    @api.depends('service_ids.cout', 'cout_activation')
    def _compute_combined_cost(self):

        for record in self:
            record.total_service_cost = sum(record.service_ids.mapped('cout'))
            record.combined_cost = int(record.total_service_cost + record.cout_activation)


    @api.onchange('date_debut', 'date_expiration','date_affectation')
    def check_dates(self):
        for record in self:
            expiration_date = fields.Datetime.from_string(record.date_expiration).date()
            assigne_date = fields.Datetime.from_string(record.date_affectation).date()
            if record.date_debut > assigne_date:
                raise ValidationError(_('Start date cannot be greater than assigning date.'))
            elif assigne_date > expiration_date:
                raise ValidationError(_('expiration date should be greater than assignement date'))


    @api.depends('date_debut', 'date_expiration')
    def _compute_status(self):
        for record in self:
            current_date = datetime.now().date()
            expiration_date = fields.Datetime.from_string(record.date_expiration).date()
            if current_date < expiration_date:
                record.state = 'open'
            else:
                record.state = 'expired'

    @api.model
    def create(self, values):
        # Check if there is an existing contract on the same vehicle that is not expired
        existing_contract = self.env['location_cars.contract'].search([
            ('vehicle_id', '=', values.get('vehicle_id')),
            ('state', '!=', 'expired')
        ])
        if existing_contract:
            raise ValidationError(_("Cannot create a new contract. Existing contract is not expired."))
        # Proceed with the creation of the new contract
        new_contract = super(ContratVoiture, self).create(values)
        # Example usage
        return new_contract
    def send_email_to_client(self):
        file_path = f'C:/Users/achba/Downloads/Contract-{self.reference}.pdf'

        # Check if the file exists
        if os.path.exists(file_path):
            self.send_email(f'Bonjour {self.conducteure_id.name},\n\nVous trouverez ci-joint Votre Contract. \n\nCordialment, \n{self.responsable.name}',
                        f'{self.conducteure_id.email}',
                        f'C:/Users/achba/Downloads/Contract-{self.reference}.pdf')
        else:
            raise ValidationError(_("you didnt download file to send it in email"))
        return True
    def action_report(self):
        report = self.env.ref('location_cars.action_report_pdf_print').report_action(self)
        file_path = f'C:/Users/achba/Downloads/Contract-{self.reference}.pdf'

        # Check if the file exists
        if os.path.exists(file_path):
            os.remove(file_path)
        return report  # Return response for download

    def send_email(self, body, to_email, attachment_path=None):
        """Sends an email with optional attachment."""

        # Set up the MIME message
        msg = MIMEMultipart()
        msg['From'] = 'achbabmahdi120@gmail.com'  # Replace with your Gmail email address
        msg['To'] = to_email
        msg['Subject'] = "Contract"
        msg.attach(MIMEText(body, 'plain'))

        # Attach the file if provided
        if attachment_path:
            with open(attachment_path, 'rb') as f:
                part = MIMEApplication(f.read(), Name=os.path.basename(attachment_path))
                msg.attach(part)
        # Connect to Gmail's SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login('achbabmahdi120@gmail.com', 'wuasfmamtzkprntj')  # Use an App Password for security
            server.sendmail(msg['From'], msg['To'], msg.as_string())



