import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import DocumentEvents
from flask_graphql_auth import AuthInfoField


class EventObject(SQLAlchemyObjectType):
    class Meta:
        model = DocumentEvents
        interfaces = (graphene.relay.Node, )


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_events = SQLAlchemyConnectionField(EventObject)
    find_event = graphene.Field(EventObject, cpf=graphene.String())

    def resolve_find_event(self, info, **args):
        cpf = args.get("cpf")
        query = EventObject.get_query(info)
        return query.filter(DocumentEvents.cpf == cpf).first()


schema = graphene.Schema(query=Query, types=[EventObject])

