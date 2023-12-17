from odoo import fields,models,api
from odoo.exceptions import AccessError, UserError, ValidationError


class CourseList(models.TransientModel):
    _name="student.report"
    _description="student report"


    start_date=fields.Date(string='Start Date')
    end_date=fields.Date(string='End Date')
    student_id_list=fields.Text(string='Id list')


    def search_student_via_admit_date(self):
        domain=[('admission_date','>=',self.start_date),('admission_date','<=',self.end_date)]
        student_ids = self.env['student.registration'].search(domain)
        print('--------id list------------')
        print(student_ids)
        
        # create dictionary for passing 
        # data_line=list()
        # for item in student_ids:
        #     data_line.append((item.name,item.student_id,item.accepted_department))

        # datas={
        #     'start_date':self.start_date,
        #     'end_date':self.end_date,
        #     'data_line':data_line,
        # }        
        
        # return self.env.ref("university_management.action_report_students_search_date_view").report_action([],student_ids)




