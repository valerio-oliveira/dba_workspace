global db_groups
global db_err_list


db_groups = {
    'contabil': {
        'host': 'deb86',
        'databases': ['contabil'],
    },
    'arquitetura': {
        'host': 'deb35',
        'databases': ['dataflow'],
    },
    'catchup': {
        'host': 'deb6-142',
        'databases': ['catchup'],
    },
    'pdv': {
        'host': 'deb6-142',
        'databases': ['pdv_mateus', 'pix', 'sitef'],
    },
    'maxipos': {
        'host': 'deb225',
        'databases': ['maxipos'],
    },
}


db_err_list = {
    {
        'code': 1,
        'type': 'sintax error',
        'strings': ['ERROR:', 'syntax error at or near ', ' at character'],
    },
    {
        'code': 2,
        'type': 'idle-in-transaction timeout',
        'strings': ['FATAL:', 'terminating connection due to idle-in-transaction timeout'],
    },
    {
        'code': 3,
        'type': 'sintax error',
        'strings': ['ERROR:', 'syntax error at end of input at character'],
    },
    {
        'code': 4,
        'type': 'not-null constraint',
        'strings': ['ERROR:', 'null value in column ', ' violates not-null constraint'],
    },
}
