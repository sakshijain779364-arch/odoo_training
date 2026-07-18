{
    "name": "Property Management",
    "author":"Sakshi",
    "license": "LGPL-3",
    "version": "18.0.1.0",
    "category": "Property",
    "sequence": -200,
    "summary":"Property Management System",
    "depends":['base'],
    "data":[
            'security/ir.model.access.csv',
            'views/estate_view.xml',
            'views/property_type_view.xml',
            'views/property_offer_view.xml',
            'views/menu.xml',
            'views/res_users_view.xml',

    ],
    "demo":[],
    "application":True,
    "auto_install":False,

}