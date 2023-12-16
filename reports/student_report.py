from odoo import fields,models,api
from odoo.exceptions import AccessError, UserError, ValidationError


class CourseList(models.TransientModel):
    _name="student.report"
    _description="student report"


    start_date=fields.Date(string='Start Date')
    end_date=fields.Date(string='End Date')
    student_id_list=fields.Text(string='Id list')


    # def search_student_via_admit_date(self):
    #     domain=[('admission_date','>=',self.start_date),('admission_date','<=',self.end_date)]
    #     student_ids = self.env['student.registration'].search(domain)

    #     return self.env.ref("university_management.student_list_date_interval").report_




