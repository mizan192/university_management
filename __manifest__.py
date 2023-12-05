{
    'name':'University Management System',
    'summary': 'Student Registration and Migration system for University',
    'description': 'A module for managing student registration, department switching and related processes in a university system.',
    'category': 'Education',
    'version':'16.0.1.1',
    'author':'Mizan',
    'depends':["base"],
    'data':[
        'views/menu.xml',
        'views/student_registration_view.xml',
        'views/department_information_view.xml',
        'security/ir.model.access.csv',
    ],
    
    'installable': True,
    'application': True,
    'license':'LGPL-3',
    'images': ['static/description/icon.png'],
    'sequence': -1,

}
