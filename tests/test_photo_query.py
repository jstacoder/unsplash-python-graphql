import json

plain_test_photo_query = '''
    query {
        get_photos(
            query_filter: { 
                order_by: LATEST 
            }
        ){
            id           
        }
    }
'''

filtered_test_photo_query = '''
    query {
        get_photos(
            query_filter: { 
                order_by: LATEST
                per_page: 20 
            }
        ){
            id           
        }
    }
'''

random_photo_query = '''
    query {
        get_random_photo {
            id
        }
    }
'''

search_photo_query = '''
    query {
        search_photos(query_filter: { 
            query: "test"
            per_page: 15
        }){
            results {
                id
            }
        }
    }
'''

# data = json.loads('''
# {"data":
#     {"get_photos": [
#
#         {"id": "X1sIr53DhzA", "description": null, "location": null, "user": {"username": null}},
#         {"id": "kdafHZZzmTI", "description": null, "location": null, "user": {"username": null}},
#         {"id": "kYh-O1Jk7EE", "description": null, "location": null, "user": {"username": null}},
#         {"id": "fPN1w7bIuNU", "description": null, "location": null, "user": {"username": null}},
#         {"id": "0mZIT-EcH5k", "description": null, "location": null, "user": {"username": null}},
#         {"id": "BxJ67hRaIBM", "description": null, "location": null, "user": {"username": null}},
#         {"id": "4TtSy9demP4", "description": null, "location": null, "user": {"username": null}},
#         {"id": "5crtSv9RzBc", "description": null, "location": null, "user": {"username": null}},
#         {"id": "kR9X7BhwzEY", "description": null, "location": null, "user": {"username": null}},
#         {"id": "5zJ2FZ5M6DM", "description": null, "location": null, "user": {"username": null}}
#     ]}
# }
# ''')


def test_query_defaults(client):
    result = client.execute(plain_test_photo_query)

    assert 'data' in result
    assert 'get_photos' in result['data']
    assert len(result['data']['get_photos']) == 10

def test_query_filters(client):
    result = client.execute(filtered_test_photo_query)
    assert 'data' in result
    assert 'get_photos' in result['data']
    assert len(result['data']['get_photos']) == 20

def test_random_photo_query(client):
    result = client.execute(random_photo_query)
    assert 'data' in result
    assert 'get_random_photo' in result['data']
    assert len(result['data']['get_random_photo']) == 1

def test_search_photo(client):
    result = client.execute(search_photo_query)
    assert 'data' in result
    assert 'search_photos' in result['data']
    assert 'results' in result['data']['search_photos']
    assert len(result['data']['search_photos']['results']) == 15
