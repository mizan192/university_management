from odoo import fields,models,api
from odoo.exceptions import AccessError, UserError, ValidationError


class MigrationReport(models.TransientModel):
    _name="migration.report"
    _description="student report"


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
    
  
    department_name=fields.Many2one('department.information')
  
    start_date=fields.Date(string='Start Date')
    end_date=fields.Date(string='End Date')
    student_id_list=fields.Text(string='Id list')


    def migrated_students_in_date_inteval(self):
        # domain=[('migration_date','>=',self.start_date),('migration_date','<=',self.end_date)]
        # domain=[('accepted_department','=',self.department_name.department_name)]
        student_ids = self.env['department.migration'].search([])

        data_line=list()
        # print(student_ids)
        for item in student_ids:
            # print(item.accepted_department)
            if item.accepted_department==self.department_name.department_name:
            #     print(item.name)
                data_line.append(
                    {
                    'name':item.name,
                    'id':item.student_new_id,
                    'pre_department':item.previous_department,
                    'due':item.due,
                    }
                )
        datas={
            'department':self.department_name.department_name,
            'start_date':self.start_date,
            'end_date':self.end_date,
            'data_line':data_line,
        }        
        
        return self.env.ref("university_management.action_report_migrated_students_rec").report_action([],data=datas)


