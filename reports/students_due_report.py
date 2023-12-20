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
  
    start_date=fields.Date(string='Start Date')
    end_date=fields.Date(string='End Date')
    student_id_list=fields.Text(string='Id list')


    def search_student_via_admit_date_for_faculty(self):
        domain=[('admission_date','>=',self.start_date),('admission_date','<=',self.end_date)]
        # domain=[('accepted_faculty','=',self.faculty_name)]
        student_ids = self.env['student.registration'].search(domain)

        data_line=list()

        for item in student_ids:
            if item.accepted_faculty==self.faculty_name and item.registration_status=="Enrolled":
                data_line.append(
                    {
                        'name':item.name,
                        'id':item.student_id,
                        'department':item.accepted_department,
                        'due':item.total_cost,
                        'status':item.registration_status,
                    }
                )
        datas={
            'faculty':self.faculty_name,
            'start_date':self.start_date,
            'end_date':self.end_date,
            'data_line':data_line,
        }        
        
        return self.env.ref("university_management.action_report_students_search_date_view").report_action([],data=datas)


