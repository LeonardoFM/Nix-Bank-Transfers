import unittest

from pyramid import testing

import transaction


def dummy_request(dbsession):
    return testing.DummyRequest(dbsession=dbsession)


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp(settings={
            'sqlalchemy.url': 'sqlite:///:memory:'
        })
        self.config.include('.models')
        settings = self.config.get_settings()

        from .models import (
            get_engine,
            get_session_factory,
            get_tm_session,
            )

        self.engine = get_engine(settings)
        session_factory = get_session_factory(self.engine)

        self.session = get_tm_session(session_factory, transaction.manager)

    def init_database(self):
        from .models.meta import Base
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        from .models.meta import Base

        testing.tearDown()
        transaction.abort()
        Base.metadata.drop_all(self.engine)

class TestClientViewSuccessCondition(BaseTest):

    def setUp(self):
        super(TestClientViewSuccessCondition, self).setUp()
        self.init_database()

        from .models import Client

        model = Client(nome='João', cnpj='5598876')
        self.session.add(model)

    def test_client_view(self):
        from .views.default import client_view
        info = client_view(dummy_request(self.session))
        self.assertEqual(info['client'].nome, 'João')
        self.assertEqual(info['client'].cnpj, '5598876')
        self.assertEqual(info['project'], 'Pyramid Cornice')

class TestTransferViewSuccessCondition(BaseTest):

    def setUp(self):
        super(TestTransferViewSuccessCondition, self).setUp()
        self.init_database()

        from .models import Transfers

        trnsf = Transfers()

        trnsf.pagador_nome = 'João'
        trnsf.pagador_banco = '001'
        trnsf.pagador_agencia = '0002'
        trnsf.pagador_conta = '1234-5'

        trnsf.beneficiario_nome = 'Maria'
        trnsf.beneficiario_banco = '002'
        trnsf.beneficiario_agencia = '9999'
        trnsf.beneficiario_conta = '6789-0'

        trnsf.valor = 100000
        trnsf.tipo = 'CC'
        trnsf.status = 'OK'

        self.session.add(trnsf)

    def test_tranfers_view(self):
        from .views.default import transfers_view
        info = transfers_view(dummy_request(self.session))
        self.assertEqual(info['Transfer'].status,'OK')
        self.assertEqual(info['Transfer'].valor,100000)

    def test_client_transfer_association_view(self):
        from .views.default import client_transfer_association_view
        info = client_transfer_association_view(dummy_request(self.session))

        from .models import Client
        cliente = Client(nome='João', cnpj='5598876')


class TestMyViewFailureCondition(BaseTest):

    def test_failing_view(self):
        from .views.default import client_view
        info = client_view(dummy_request(self.session))
        self.assertEqual(info.status_int, 500)
