# Simple Twitter Clone
* [Endpoint Map](https://developer.twitter.com/en/docs/twitter-api/migrate/twitter-api-endpoint-map)

## TODO

* Mermaid
  + いい感じにグラフが書ける js plugin
  + これが本当にいい感じ

* fastapi
  + query parameters
    - https://fastapi.tiangolo.com/ja/tutorial/query-params-str-validations/

* RESTful Design
  + Goto wiki

## ER Diagram

```mermaid
erDiagram
  users {
    int        id       PK
    string     name
    string     password
    references tweets
  }

  tweets {
    int  id      PK
    int  user_id FK
    text message
  }

  likes {
    int id       PK
    int tweet_id FK
    int user_id  FK
  }

  users  ||--o{ tweets : "A User has Many Tweets"
  users  ||--o{ likes  : "A User has Many Likes"
  tweets ||--o{ likes  : "A Tweet has Many Likes"
```

## Model

```sql
sqlite> .table
likes tweets     users

CREATE TABLE likes (
        id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        tweet_id INTEGER NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(user_id) REFERENCES users (id),
        FOREIGN KEY(tweet_id) REFERENCES tweets (id)
);

CREATE TABLE tweets (
        id INTEGER NOT NULL,
        message VARCHAR NOT NULL,
        user_id INTEGER NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE TABLE users (
        id INTEGER NOT NULL,
        name VARCHAR NOT NULL,
        password VARCHAR NOT NULL,
        PRIMARY KEY (id)
);
```

## Schema

* Pydantic
  + [ ] Pydantic Schema Validation
    - [x] Field min_length, max_length
    - [x] @validation decorator
    - [x] Raise HTTPException in Pydantic validator
    - [ ] @root_validator

## Endpoint

* users
  + [x] GET   /users
  + [x] POST  /users
  + [x] GET   /users/:user_id
  + [x] PATCH /users
  + [x] DEL   /users

* tweets
  + [x] GET   /tweets
  + [x] POST  /tweets
  + [x] GET   /tweets/:tweet_id
  + [x] PATCH /tweets/:tweet_id
  + [x] DEL   /tweets/:tweet_id

* likes
  + [x] GET  /tweets/:tweet_id/likes
  + [x] POST /tweets/:tweet_id/likes
  + [x] DEL  /tweets/:tweet_id/likes

## TODO

* [Favorites](https://developer.twitter.com/en/docs/twitter-api/v1/tweets/post-and-engage/api-reference/get-favorites-list)

* [Likes](https://developer.twitter.com/en/docs/twitter-api/tweets/likes/migrate/manage-likes-standard-to-twitter-api-v2)

なんと Favorites は古いAPIだったことが判明
現在は Likes というAPIに変わっておった すごい量の変更点が発生

* [Lists](https://help.twitter.com/ja/using-twitter/twitter-lists)

> リストを使用することで、タイムラインに表示するツイートをカスタマイズ、整理、優先順位付けできます
> Twitterで他のユーザーが作成したリストに参加したり、自分のアカウントから、グループ、トピック、
> または興味関心の対象別に、他のアカウントのリストを作成したりできます
> リストタイムラインには、リストに登録されたアカウントのツイートのみが表示されます
> また、お気に入りのリストを自分のタイムラインの上部に固定しておけば
> 重要なアカウントからのツイートを見逃すこともありません。

こんなに複雑なものはいらない
Lists/members (tweet users) があればOKかな

そこに登録されている members のツイートを一覧で表示できるみたいな機能でOK

* Tags

Twitter には message にタグと呼ばれるものを埋め込める
面倒なので作らない
