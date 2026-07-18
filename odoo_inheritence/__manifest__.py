{
"name": "odoo_inheritence",
"summary": """  """,
"description": "",
"author": "Sakshi",
"license": "LGPL-3",
"version": "18.0.1.0",
"sequence": -100,
"depends": ['sale','Jain_Hospital'],
"data": [
    'security/groups.xml',
    'security/ir.model.access.csv',
    'wizard/custom_report_view.xml',
    'report/saleorder_report.xml',
    'report/custom_report.xml',
    'views/sale_order_views.xml',
    'views/res_partner_view.xml',
    'views/config_settings_views.xml',
    'views/stock_picking_views.xml',




],
"demo": [],
}