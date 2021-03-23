# flask-marshmallow-apispec-example-web-server

Flask + marshmallow + apispec으로 OpenAPI 3.0 명세 문서화 자동화 예제 코드입니다.
이 예제 코드에 대한 자세한 설명은
[스포카 기술 블로그의 "Flask, marshmallow, apispec으로 API 문서화 자동화하기"](https://spoqa.github.io/2021/03/23/flask-marshmallow-apispec.html)
포스트를 참고해주세요.

## Usage

### Web

```sh
$ python run.py --help
usage: run.py [-h] [-H HOST] [-p PORT]

optional arguments:
  -h, --help            show this help message and exit
  -H HOST, --host HOST  Address to bind (default: 0.0.0.0)
  -p PORT, --port PORT  Port number to bind (default: 8080)
$ python run.py
 * Serving Flask app "example_web_server.wsgi" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 000-000-000
```

`run.py` 를 실행하면 기본값으로 `8080` 포트를 이용해 서빙됩니다.

이 예제 코드는 3가지의 API를 가지고 있습니다.

```sh
$ http :8080/hello/
HTTP/1.0 200 OK
Content-Length: 13
Content-Type: text/html; charset=utf-8
Server: Werkzeug/1.0.1 Python/3.8.2

Hello, world!

$ http :8080/secured/hello/ name==Rusty X-Some-Access-Token:secure-access-token
HTTP/1.0 200 OK
Content-Length: 20
Content-Type: text/html; charset=utf-8
Server: Werkzeug/1.0.1 Python/3.8.2

Hello, sneaky Rusty!

$ http -j POST :8080/post/hello/ name=Thomas mood=5 X-Some-Access-Token:secure-access-token
HTTP/1.0 200 OK
Content-Length: 79
Content-Type: application/json
Server: Werkzeug/1.0.1 Python/3.8.2

{
    "message": "I hope your mood 5 be better.",
    "title": "Hello, Thomas!"
}
```

자세한 API 동작은 `example_web_server/api.py` 코드를 참고해주세요.

## License

_flask-marshmallow-apispec-example-web-server_ is distributed under the terms of the MIT License.

See [LICENSE](LICENSE) for more details.
