from flask import Flask


def test_get_hello(fx_wsgi_app: Flask):
    url = '/hello/'
    client = fx_wsgi_app.test_client()

    response = client.get(url)
    assert response.status_code == 200
    assert response.get_data(as_text=True) == 'Hello, world!'


def test_get_secured_hello(fx_wsgi_app: Flask):
    url = '/secured/hello/'
    client = fx_wsgi_app.test_client()

    response = client.get(url)
    assert response.status_code == 401

    response = client.get(url, headers={'X-Some-Access-Token': 'access_token'})
    assert response.status_code == 200
    assert response.get_data(as_text=True) == 'Hello, sneaky unknown!'

    response = client.get(
        url,
        headers={'X-Some-Access-Token': 'access_token'},
        query_string={'name': 'some_name'},
    )
    assert response.status_code == 200
    assert response.get_data(as_text=True) == 'Hello, sneaky some_name!'


def test_post_hello(fx_wsgi_app: Flask):
    url = '/post/hello/'
    client = fx_wsgi_app.test_client()

    response = client.post(url)
    assert response.status_code == 401

    response = client.post(
        url,
        headers={'X-Some-Access-Token': 'access_token'},
        json={'name': 'some_name'},
    )
    assert response.status_code == 400
    assert response.get_json() == {
        'invalidFields': {'mood': ['Missing data for required field.']},
    }

    response = client.post(
        url,
        headers={'X-Some-Access-Token': 'access_token'},
        json={'name': 'some_name', 'mood': 42},
    )
    assert response.status_code == 200
    assert response.get_json() == {
        'title': 'Hello, some_name!',
        'message': 'I hope your mood 42 be better.',
    }
