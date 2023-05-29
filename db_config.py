config = {
    'Sales': {
        'date': {
            'type': 'TEXT', 
            'is_nullable': 0, 
            'default_value': None
        },
        'date2': {
            'type': 'TEXT', 
            'is_nullable': 0, 
            'default_value': 'NULL'
        },
        'amount': {
            'type': 'REAL', 
            'is_nullable': 0, 
            'default_value': None
        },
        'cost': {
            'type': 'REAL', 
            'is_nullable': 0, 
            'default_value': None
        }
    },
    'Items': {
        'name': {
            'type': 'TEXT', 
            'is_nullable': 0, 
            'default_value': None
        },
        'measure': {
            'type': 'TEXT', 
            'is_nullable': 0, 
            'default_value': None
        }
    },
    'Production': {
        'name_production': {
            'type': 'TEXT',
            'is_nullable': 0,
            'default_value': None
        },
        'location': {
            'type': 'TEXT', 
            'is_nullable': 0, 
            'default_value': None
        }
    },
    'Actors': {
        'name_actor': {
            'type': 'TEXT',
            'is_nullable': 0,
            'default_value': None
        },
        'type': {
            'type': 'TEXT', 
            'is_nullable': 0, 
            'default_value': None
        }
    },
    'Markets': {
        'name_market': {
            'type': 'TEXT',
            'is_nullable': 0,
            'default_value': None
        },
        'location': {
            'type': 'TEXT', 
            'is_nullable': 0, 
            'default_value': None
        }
    },
    'Storage': {
        'fund': {
            'type': 'INTEGER',
            'is_nullable': 0,
            'default_value': None
        },
        'inventory': {
            'type': 'INTEGER', 
            'is_nullable': 0, 
            'default_value': None
        }
    },
    'Archives': {
        'name_archive': {
            'type': 'TEXT',
            'is_nullable': 0,
            'default_value': None
        }
    },
    'Sources': {
        'name_source': {
            'type': 'TEXT',
            'is_nullable': 0,
            'default_value': None
        }
    }
}