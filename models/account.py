from odoo import fields,models,api
from odoo.exceptions import AccessError, UserError, ValidationError
from datetime import date
from dateutil.relativedelta import relativedelta
import random

class StudentAccount(models.Model):
    _name="student.account"
    _description="Students account"


    name=fields.Char(string='Name')
    student_id=fields.Char(string='Id')
    faculty=fields.Char(string='Faculty')
    department=fields.Char(string='Department')
    course_fee=fields.Monetary(string='Course Cost',  readonly='1')

    admission_fee=fields.Monetary(string='Admission Fee', default=20000, readonly='1')  
    registration_fee=fields.Monetary(string='Registration Fee', default=5000, readonly='1')
    department_fee=fields.Monetary(string='Department Fee', compute='_check_department_fee', store = True)
    fine=fields.Monetary(string='Fine', default=0)
    scholarship=fields.Monetary(string='Scholarship', compute='_scholarship_calculation', store=True)
    total_fee=fields.Monetary(string='Total Fee', compute='_calculate_total_Fee', currency_field='currency_id', store=True)

    student_relation = fields.Many2one('student.profile')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env['res.currency'].search([('name', '=', 'BDT')]))
    

    invoice_date=fields.Date(string='Invoice Date', default=fields.Date.today, readonly='1')
    due_date=fields.Date(string='Due Date')
    ready_to_invoiced=fields.Boolean(default=False)
    
    show_button=fields.Boolean(default=False)
    
    student_reference=fields.Many2one(
        comodel_name='student.registration',
        domain="[('student_id','=',student_id)]",
    )

    INVOICE_STATUS_SELECTION = [
        ('Draft', 'Draft'),
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Cancel', 'Cancelled'),
    ]

    invoice_status = fields.Selection(
        selection=INVOICE_STATUS_SELECTION,
        string='Invoice Status',
        default='Draft',  # Set a default value if needed
        help='Select the status of the invoice.',
    )


# register payment field 
    journal_id=fields.Selection(
        selection=[('Bank', 'Bank'),('Cash', 'Cash'),('Bkash','Bkash')],
        default='Cash',
        help='Select Payment Option',
        string='Journal',
    )
    amount_paid=fields.Monetary(string='Amcount', currency_field='currency_id')
    payment_date=fields.Date(string='Payment Date', default=fields.Date.today)
    recipient_bank_account=fields.Char(string='Recipient Bank No')
    transaction_id=fields.Char(string='Transaction ID')
    record_id=fields.Char(string='Record ID')
    memo_no=fields.Char(string='Memo')
    payment_phone_num=fields.Char(string='Phone No')
    
    fee_received = fields.Monetary(string='Received Fee', readonly='1')



# other 
    smart_button_title=fields.Char(default='Register Payment')
    








    @api.depends('faculty')
    def _check_department_fee(self):
        for rec in self:
            fees=12000
            if rec.faculty=='engineering':
                fees=fees+5000
            if self.department=='business':
                fees=fees+2500
            rec.department_fee=fees


    @api.depends('student_id')
    def _scholarship_calculation(self):
        return
        for obj in self:
            obj.scholarship=0
            domain = [('student_id','=',obj.student_id)]
            rec = self.env['student.profile'].search(domain)
            discount=0
            fees=obj.admission_fee+obj.registration_fee
            hsc_result = rec.hsc_result
            ssc_result = rec.ssc_result

            if hsc_result>=5.00:
                discount=fees
            elif hsc_result>=4.75 and ssc_result>=5.00:
                discount=fees-(fees*.75)
            elif hsc_result>=4.50:
                discount=fees-(fees*.5)
            elif hsc_result>=4.00 and ssc_result>=4.25:
                discount=fees-(fees*.3)
            else:
                discount=0
            obj.scholarship=discount




    @api.depends('student_id')
    def _calculate_total_Fee(self):
        for rec in self:
            rec.total_fee=rec.admission_fee+rec.course_fee+rec.registration_fee+rec.department_fee+rec.fine-rec.scholarship
        # self.total_fee=self.admission_fee+self.course_fee+self.registration_fee+self.department_fee+self.fine-self.scholarship

    

    @api.onchange('due_date')
    def check_due_date(self):
        self.show_button=False
        
        if self.due_date==False:
            self.ready_to_invoiced=False
        
        elif fields.Date.from_string(self.due_date)<fields.Date.from_string(self.invoice_date):
            self.ready_to_invoiced=False
            # raise ValidationError("Due date can't be erailer than invoice-date")
            # ValidationError("Due date can't be erailer than invoice-date")
        else:
            self.ready_to_invoiced=True
        
        print('------------------------')

        # for course in self.course_list:
        #     print('------ course name : ', course.course_name)
        #     print('------ course cost : ', course.single_course_fee)

# fee confirm button 
    def confirm_fee(self):
        self.show_button=True
        domain = [('student_id','=',self.student_id)]
        rec = self.env['student.profile'].search(domain)
        rec.write({'total_fee':self.total_fee})
        rec = self.env['student.registration'].search(domain)
        rec.write({'total_cost':self.total_fee,'due_date':self.due_date})
        


# registration method button 
    def register_payment_method_action(self):
        context = {
        'default_name': self.name,
        'default_student_id': self.student_id,
        }
        

        return {
            'name': "Register Payment",
            'res_model':'student.account',
            'res_id':self.id,
            'type': 'ir.actions.act_window',
            'view_mode':'form',
            'view_id':self.env.ref('university_management.um_accounts_fees_registration_views').id,
            'target':'new',
            'context':context,

        }    
    
    def get_random(self):
        random_number = ''.join(str(random.randint(0, 9)) for _ in range(4))
        return random_number



    # confirm payment registration 
    def create_payments(self):

        if not self.amount_paid:
            raise ValidationError("Payment amount must be positive amount!!!")



        self.fee_received+=self.amount_paid
        self.total_fee-=self.amount_paid
        self.invoice_status='Paid'

        domain = [('student_id','=',self.student_id)]
        rec = self.env['student.profile'].search(domain)
        rec.write({'fee_received':self.fee_received})
        
        # add to  transaction record model
        rec = self.env['student.registration'].search(domain)
        reg_id = rec.registration_id
        random_num = self.get_random()
        dict_key={
            's_name':self.name,
            's_id':self.student_id,
            'amount_paid':self.amount_paid,
            'payment_date':self.payment_date,
            'transaction_id':self.transaction_id,
            'record_id':reg_id.lower()+"-"+random_num,
        }
        rec = self.env['account.transaction.record'].create(dict_key)
        
        
    
            




    def smart_button_transaction_list_preview(self):
        domain = [('s_id','=',self.student_id)]
        return {
            'name' : 'Transaction Record',
            'type' : 'ir.actions.act_window',
            'res_model' : 'account.transaction.record',
            'view_mode' : 'tree',
            # 'target' : 'new',
            'target' : 'current',
            'domain' : domain,
        }
        







    @api.model
    def create(self,vals):
        if 'student_id' not in vals.keys():
            return super(StudentAccount,self).create(vals)
        s_id = vals['student_id']
        record_exist = self.env['student.account'].search(['student_id','=',s_id])

        if record_exist:
            rec = self.write(vals)
        else:
            return super(StudentAccount,self).create(vals)













   



