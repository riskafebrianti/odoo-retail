# -*- coding: utf-8 -*-
{
    'name': 'Odoo Backup Cron',
    'version': '1.0',
    'category': 'Hidden',
    'description': """
The kernel of Odoo, needed for all installation.
===================================================
""",
    'depends': [
        "base",
        ],
    'data': [
        "data/ir_cron.xml"        
    ],
    'demo': [
    ],
    'test': [],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
