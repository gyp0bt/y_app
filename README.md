# y_app
## Concept1
某SNSを模したツイート型SNS「Y」。投稿は「ツイート」、投稿の再共有は「リツイート」と呼称する。
## Conept2
データベースをDjango(y_db)、UIをReact(y_ui)で実装する。localhost上にDjangoサーバーとReactサーバーを立てて、http responseにてデータのやり取りを行う。Django側のhttpインターフェースにはDRFを使用する。
## How to Use
### Djangoサーバーの起動
#### install
pip install y_app/y_db/requirement.txt
#### run server
cd y_app/y_db && bash bin/run_db.sh
### Reactサーバーの起動
#### run server
bash bin/run_ui.sh
