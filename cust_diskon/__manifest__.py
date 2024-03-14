# -*- coding: utf-8 -*-
{
    'name': "cust_diskon",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','web','contacts','sale','sale_management','product','purchase','account','base_accounting_kit'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/diskon.xml',
        'views/saleorder.xml',
        'views/asset.xml',
        'views/barcode.xml',
        'views/tagihan.xml',
        'report/header.xml',
        # 'report/report.xml',
        'report/suratjalan.xml',
        'report/sale_report.xml',
        'report/inv_report.xml',
        'report/fu.xml',
        'report/purchase_po_report.xml',
        'report/stock_picking_report.xml',
        'report/stock_dileveryS_report.xml',    
    ],
    # 'qweb': [
    #     'report/product_product_reports.xml',
    #     'report/product_product_templates.xml',
    # ],
'assets': {
   'web.assets_backend': [
       'cust_diskon/static/src/js/tes.js',

   ],
   
    # 'web.assets_qweb':[
    #     'report/sale_report.xml',
    # ],

},
    # 'assets': {
    # #     'point_of_sale.assets': [
    # #         'cust_diskon/static/src/xml/button.xml',
    # #         'cust_diskon/static/src/js/button.js',
    # #     ],
    #  },

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    

}



