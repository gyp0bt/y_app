# y_app
## Concept1
某SNSを模したツイート型SNS、「Y」。投稿は「ツイート」、投稿の再共有は「リツイート」と呼称する。
## Conept2
データベースをDjango(y_db)、UIをReact(y_ui)で実装する。localhost上にDjangoサーバーとReactサーバーを立てて、http responseにてデータのやり取りを行う。Django側のhttpインターフェースにはDRFを使用する。
## How to Use
### Djangoサーバーの起動
bin/run_db
### Reactサーバーの起動
bin/run_ui
