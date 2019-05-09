from flask import Flask
from flask_graphql import GraphQLView

from unsplash.schema import schema

app = Flask(__name__)

class MyGraphqlView(GraphQLView):
    schema = schema
    graphiql = True

@app.route('/')
def hello_world():
    return 'Hello World!'

app.add_url_rule('/___graphql', view_func=MyGraphqlView.as_view(name='graphql'))


if __name__ == '__main__':
    app.run()
