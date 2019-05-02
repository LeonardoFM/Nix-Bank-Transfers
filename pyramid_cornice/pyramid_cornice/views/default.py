from pyramid.view import view_config
from pyramid.response import Response

from sqlalchemy.exc import DBAPIError

from .. import models


@view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
def client_view(request):
    try:
        query = request.dbsession.query(models.Client)
        joao = query.filter(models.Client.nome == 'João').first()
        cnpj = joao.cnpj
        print('eitcha',cnpj)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'client': joao, 'cnpj': cnpj, 'project': 'Pyramid Cornice'}


# @view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
# def transfers_view(request):
#     try:
#         query = request.dbsession.query(models.Transfers)
#         transfer = query.filter(models.Transfers.pagador_nome == 'João').first()
#     except DBAPIError:
#         return Response(db_err_msg, content_type='text/plain', status=500)
#     return {'Transfer': transfer}


# @view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
# def client_transfer_association_view(request):
#     try:
#         query = request.dbsession.query(models.Client)
#         query_t = request.dbsession.query(models.Transfers)
#
#         client = query.filter(models.Client.nome == 'João').first()
#         transfer = query_t.filter(models.Transfers.pagador_nome == 'João').first()
#         if(transfer):
#             client.transfers = transfer
#         else:
#             print('Erro: não existe transferências associadas a esse cliente')
#     except DBAPIError:
#         return Response(db_err_msg, content_type='text/plain', status=500)
#     return {'client_id': client.id,'transfer_id': transfer.id}

db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Check your README.txt for descriptions and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
