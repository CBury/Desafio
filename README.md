# Desafio

## Arquitetura proposta
![Image of architecture](images/architecture.png)

### Armazenamento
* A Base A precisa de Alta segurança, porém não necessita de uma boa performance. Optei por usar MySQL, porém PostgreSQL seria uma solução igualmente boa pois atende aos critérios.
* A basa B precisa de uma segurança mediana e uma performance alta. Para isso MySQL também é uma opção boa.
* A base C não necessita de tanta segurança e precisa de uma performance altíssima. Tanto MySQL quanto MongoDB são opções viáveis, cada uma com seus pontos fortes. O gráfico(*) abaixo mostra como, num  experimento comparativo, MySQL foi bem mais rápido em select, enquanto MongoDB em update e insert. Levando-se isso em consideração, optei por usar MySQL aqui também.
![Image of mysql-vs-mongo](images/mysql-vs-mongo.png)
Fonte: https://dzone.com/articles/comparing-mongodb-amp-mysql
(*Performance para 1.000.000 de registros.)

### Tráfego
Os três micro serviços serão acessados por Flask. Entre os frameworks mais populares de Python (Django, Flask e Pyramid) ele é o que permite um projeto menor e com menos camadas e complexidade de código, o que aumenta um pouco a performance. Como será desenvolvido um micro serviço simples para conectar a base de dados com o usuário ele é ideal.

### Disponibilização dos Dados
Os dados serão disponibilizados via GraphQL. Diferente das APIs Restful o GraphQL dá ao usuário mais liberdade em relação a quais dados ele irá acessar no mesmo endpoint. Isso pode aumentar a velocidade de trânsito de dados para casos em que o usuário precisa de poucas informações.
![Imagen of GraphQL](images/graphql.png)
Cada projeto terá sua própria implementação da ferramenta, pormitindo que cada usuário tenha acesso apenas ao micro serviço que lhe for necessário.
A conecção entre o GraphQL e o micro serviço é feita por JWT para os micro serviços A e B, onde o usuário precisa fornecer um login e senha para o micro serviço e receberá um token temporário de acesso.
![Imagen of GraphQL](images/post1.png)
![Imagen of GraphQL](images/post2.png)

## Como executar o projeto
Instalar docker
### Micro serviço A
```
sudo docker-compose build mysql data-debts
sudo docker-compose up mysql data-debts
```
* Acessar: http://0.0.0.0:5000/login com username: 'admin' e password: 'desafio123' para o código de autenticação.
* Acessar: http://0.0.0.0:5000/graphql com a autenticação do passo anterior.

Exemplos de buscas: 
* Para acessar todas as dívidas na base de dados:
```
{
  allDebts{
    edges{
      node{
        value
        company
        description
        date
        status
        debtor{
          cpf
          name
          address
        }
      }
    }
  }
}
```
* Para acessar todas as pessoas com as respectivas dívidas:
```
{
  allPersons{
    edges{
      node{
        cpf
        name
        address
        debts{
          edges{
            node{
              value
              company
              date
              status
            }
          }
        }
      }
    }
  }
}
```
* Para buscar um CPF específico:
```
{search(q: "12312312345") {
    __typename
    ... on PersonObject {
      cpf
      name
      address
      debts {
        edges {
          node {
            value
            company
            description
            status
          }
        }
      }
    }
  }
}
```
### Micro serviço B

```
sudo docker-compose build mysql_b score
sudo docker-compose up mysql_b score
```
* Acessar: http://0.0.0.0:5000/login com username: 'admin' e password: 'desafio123' para o código de autenticação.
* Acessar: http://0.0.0.0:5000/graphql com a autenticação do passo anterior.

Exemplos de buscas: 
* Para acessar todos os bens na base de dados:
```
{
  allAssets{
    edges{
      node{
        value
        description
        owner{
          cpf
          name
          address
        }
      }
    }
  }
}
```
* Para acessar todas as pessoas com os respectivos bens:
```
{
  allPersons{
    edges{
      node{
        cpf
        name
        address
        assets{
          edges{
            node{
              value
              description
            }
          }
        }
      }
    }
  }
}
```
* Para buscar um CPF específico:
```
{search(q: "12312312345") {
    __typename
    ... on PersonObject {
      cpf
      name
      address
      assets {
        edges {
          node {
            value
            description
          }
        }
      }
    }
  }
}
```

### Micro serviço C
```
sudo docker-compose build mysql_c document-events
sudo docker-compose up mysql_c document-events
```

* Acessar: http://0.0.0.0:5000/graphql

* Para buscar todos os eventos:
```
{
  allEvents{
    edges{
      node{
        cpf
        lastQuery
        financialTransactions
        lastBuy
      }
    }
  }
}
```
* Para buscar um CPF específico:
```
query{
  findEvent(cpf: "12312312345") {
    lastQuery
    financialTransactions
    lastBuy
  }
}
```