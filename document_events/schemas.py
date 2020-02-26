import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from document_events.models import DocumentEvents
from flask_graphql_auth import AuthInfoField


class EventObject(SQLAlchemyObjectType):
    class Meta:
        model = DocumentEvents
        interfaces = (graphene.relay.Node, )


class SearchResult(graphene.Union):
    class Meta:
        types = (EventObject)


class MessageField(graphene.ObjectType):
    message = graphene.String()


class ProtectedUnion(graphene.Union):
    class Meta:
        types = (MessageField, AuthInfoField)

    @classmethod
    def resolve_type(cls, instance, info):
        return type(instance)


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_events = SQLAlchemyConnectionField(EventObject)
    event = graphene.Field(lambda: EventObject, cpf=graphene.String())
    search = graphene.List(SearchResult, q=graphene.String())

    def resolve_search(self, info, **args):
        q = args.get("q")
        query = EventObject.get_query(info)
        query = query.filter(DocumentEvents.cpf == q)
        objs = query.all()

        return objs

schema = graphene.Schema(query=Query, types=[EventObject, SearchResult])

