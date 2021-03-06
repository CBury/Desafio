import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import Person, Debt
from flask_graphql_auth import AuthInfoField, query_jwt_required


class DebtObject(SQLAlchemyObjectType):
    class Meta:
        model = Debt
        interfaces = (graphene.relay.Node, )


class PersonObject(SQLAlchemyObjectType):
   class Meta:
       model = Person
       interfaces = (graphene.relay.Node, )


class SearchResult(graphene.Union):
    class Meta:
        types = (PersonObject, DebtObject)


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
    all_debts = SQLAlchemyConnectionField(DebtObject)
    all_persons = SQLAlchemyConnectionField(PersonObject)
    person = graphene.Field(lambda: PersonObject, cpf=graphene.String())
    search = graphene.List(SearchResult, q=graphene.String())  # List field for search results

    def resolve_search(self, info, **args):
        q = args.get("q")
        person_query = PersonObject.get_query(info)

        query = person_query.join(Person.debts)
        query = query.filter(Person.cpf == q)
        objs = query.all()

        return objs

    @query_jwt_required
    def resolve_protected(self, info):
        return MessageField(message="Hello World!")

schema = graphene.Schema(query=Query, types=[PersonObject, DebtObject, SearchResult])

