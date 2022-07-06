class MessageGroup:
    list = {
        'group_contabil': {
            'name': 'contabil',
            'active': False,
            'databases': ['contabil', ],
            'telegram': ['elvisleyaraujo', 'Clezio', ],
        },
        'group_arquitetura': {
            'name': 'arquitetura',
            'active': False,
            'databases': ['dataflow', 'engenharia', 'engenharia_cdc', 'itsecurity', 'itservice', 'ittask', ],
            'telegram': ['estevao_goes', 'gerdandourado', ],
        },
        'group_catchup': {
            'name': 'catchup',
            'active': False,
            'databases': ['catchup', ],
            'telegram': ['antoniocaju', ],
        },
        'group_pdv': {
            'name': 'pdv',
            'active': False,
            'databases': ['maxipos', 'pdv_mateus', 'pix', 'sitef', ],
            'telegram': ['Andre_felippe', 'hugocfranco', 'Rayrone', ],
        },
        'group_dba': {
            'name': 'dba',
            'active': True,
            'databases': ['contabil', 'dataflow', 'engenharia', 'engenharia_cdc', 'itsecurity', 'itservice', 'ittask', 'catchup', 'maxipos', 'pdv_mateus', 'pix', 'sitef', ],
            'telegram': ['valerio_oliveira', 'renatoss32', ],
        },
    }
