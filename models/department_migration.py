from odoo import fields,models,api

class DepartmentMigration(models.Model):
    _name="department.migration"
    _description="Department switch process"

    student_info=fields.Many2one('student.profile')

    student_name=fields.Char(related='student_info.name',string='Student Name')
    student_id=fields.Char(related='student_info.student_id',string='Student ID')
    previous_faculty=fields.Char(related='student_info.accepted_faculty',string="Previous Faculty")
    previous_department=fields.Char(related='student_info.accepted_department',string="Previous Department")

    faculty_name=fields.Selection([('engineering','Engineering'),('business', 'business'), ('arts', 'Arts')], string='Select Faculty')

    engineering_departments=fields.Many2one(
        comodel_name='engineering.faculty',
        # inverse_name='eng_student_id',
        string='Engineering Department'
    )
    business_departments=fields.Many2one(
        comodel_name='business.faculty',
        # inverse_name='business_student_id',
        string="Business Department"
    )
    arts_departments=fields.Many2one(
        comodel_name='arts.faculty',
        # inverse_name='arts_student_id',
        string="Arts Department"
    )

    accepted_faculty=fields.Char(string="Faculty", readonly=True)
    accepted_department=fields.Char(string="Department",readonly=True)
    congres_group=fields.Char(default="not_confirm")
    is_admitted=fields.Boolean(default=False)
    department_obj =fields.Char(string="Object")