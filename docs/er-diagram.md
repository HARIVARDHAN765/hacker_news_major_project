# Entity Relationship Diagram (ERD)

## Overview

This ER Diagram represents the database design for the Hacker News Clone project. It models users, posts, comments, and votes. Users can create news posts, Ask posts, comment on discussions, and upvote content.

```mermaid
erDiagram

    USER {
        int id PK
        string username
        string email
        string password
        datetime date_joined
    }

    POST {
        int id PK
        string title
        string url
        string post_type
        datetime created_at
        int user_id FK
    }

    COMMENT {
        int id PK
        string content
        datetime created_at
        int user_id FK
        int post_id FK
    }

    VOTE {
        int id PK
        datetime created_at
        int user_id FK
        int post_id FK
    }

    USER ||--o{ POST : creates
    USER ||--o{ COMMENT : writes
    USER ||--o{ VOTE : casts

    POST ||--o{ COMMENT : has
    POST ||--o{ VOTE : receives
```

## Relationship Summary

* One User can create many Posts.
* One User can write many Comments.
* One User can cast many Votes.
* One Post can have many Comments.
* One Post can receive many Votes.

## Notes

* NEWS posts contain a title and URL.
* ASK posts contain a title and discussion question.
* Users can upvote posts.
* Users can comment on posts.
* Each vote belongs to one user and one post.
* Each comment belongs to one user and one post.
