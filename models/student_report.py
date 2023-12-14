from odoo import fields,models,api
from odoo.exceptions import AccessError, UserError, ValidationError


class CourseList(models.TransientModel):
    _name="student.report"
    _description="student report"


    start_date=fields.Date(string='Start Date')
    end_date=fields.Date(string='End Date')
    student_id_list=fields.Text(string='Id list')



    def get_students_list_vai_date(self):
        domain=[('admission_date', '>=', self.start_date), ('admission_date', '<=', self.end_date)]
        rec = self.env['student.registration'].search(domain)
        print("----------------- id list ---------------------")
        print(rec)

        record_list=""
        for single_rec in rec:
            s_id = single_rec.student_id
            if s_id:
                line="ID No. : "+s_id+"\n"
                record_list=record_list+line
        self.student_id_list=record_list


