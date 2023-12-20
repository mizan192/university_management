from odoo import fields,models,api
from odoo.exceptions import AccessError, UserError, ValidationError


class DueReport(models.TransientModel):
    _name="due.report"
    _description="student due report"


    STATUS_SELECTION = [
        ('Reviewing', 'Reviewing'),
        ('Enrolled', 'Enrolled'),
    ]

    admission_status = fields.Selection(
        selection=STATUS_SELECTION,
        string='Admission Status',
        default='Enrolled',  
    )
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env['res.currency'].search([('name', '=', 'BDT')]))
    
    faculty_name=fields.Selection([('engineering','Engineering'),('business', 'Business'), ('arts', 'Arts')], default='arts', string='Faculty Name' )

    department_name=fields.Many2one('department.information')
    due=fields.Monetary(string='Due')
    start_date=fields.Date(string='Start Date')
    end_date=fields.Date(string='End Date')
    student_id_list=fields.Text(string='Id list')


    def search_student_due_wise(self):
        domain=[('total_cost','>=',self.due)]
        # domain=[('accepted_faculty','=',self.faculty_name)]
        student_ids = self.env['student.registration'].search(domain)

        data_line=list()

        for item in student_ids:
            if item.accepted_department==self.department_name.department_name:
                data_line.append(
                    {
                        'name':item.name,
                        'id':item.student_id,
                        'due':item.total_cost,
                    }
                )
        datas={
            'department':self.department_name.department_name,
            'due':self.due,
            'data_line':data_line,
        }        
        
        return self.env.ref("university_management.action_reporst_for_due").report_action([],data=datas)


