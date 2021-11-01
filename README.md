# word-management

manages dialects words

## word schema

- word
  - id
  - tags (VARCHAR, comma separated_values, no comma allowed, hashtag) -> transformed to #xxx#xxx#xxxx
  - explanation (VARCHAR) -> versions -> each versions has contributors
  - usage (VARCHAR) -> versions -> each versions has contributors
  - pronunciation (VARCHAR) -> versions -> each versions has contributors

## database design

- words

  - id (uuid)
  - name (62)
  - locked_for_edit (bool)
  - merged_to_another (id)
  - dialect (str, dialect enum)
  - created_at (datetime)
  - created_by (user_id)
  - modified_by (user_id) # only admin can modify
  - modified_at (datetime)

- word\_(explanation|usage|pronunciation|tags)\_versions

  - id (uuid)
  - w_id (FK, word_id)
  - content (the explanation|usage|pronounciation|tag)
  - created_at (datetime)
  - created_by (user_id)
  - up_votes (int)
  - down_votes (int)
  - modified_by (user_id) # only creator can modify
  - modified_at (datetime)

- users

  - id
  - name
  - email

- suggestions
  - id
  - created_by (FK, u_id)
  - created_at (FK, u_id))
  - v_id (FK, version id)
  - w_id (FK, word id)
  - field (explanation|usage|pronunciation|tags)
  - content
  - accepted (bool)
  - modified_by (user_id) # only creator can modify
  - modified_at (datetime)

## how things work

user creates a word, he creates versions of tag/exp/usage/pronouciation. (or can leave some empty, which is fine)

other user can suggest by creating a new version.
the version showed by default is the only with most up_votes - down_votes

other user can also give suggestions to the current version owner
so in each field, there are 2 options (suggestion to version owner | create by own version)

suggestion -> trigger email to the owner, and owner can see those while modifiying and can tick accepted!
create -> trigger create page

## scoring

- create word = 20
- create version (version of each field) = 20
- modify version = 10
- suggestion = 10

  - accepted = 10

- vote up|down = 1
