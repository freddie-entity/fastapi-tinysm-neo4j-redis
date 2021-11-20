#GET
GET_POST_BY_ID = """MATCH(n:Post {id: $id}) RETURN n"""
GET_POST_BY_USERNAME = """MATCH(n:Post {username: $username}) RETURN n SKIP $skip LIMIT $limit"""
GET_POSTS = """MATCH(n:Post) RETURN n SKIP $skip LIMIT $limit"""
GET_USERS_LIKED_POST="""MATCH(n:Post {id: $post_id})-[r:RECEIVE_POST_LIKE]->(u) return u.username as userlike"""
GET_USERS_LIKED_COMMENT="""MATCH(n:Comment {id: $comment_id})-[r:RECEIVE_COMMENT_LIKE]->(u) return u.username as userlike"""


#POST
CREATE_POST = """
MATCH(m:User {username: $username})
CREATE(m)-[r:IS_AUTHOR {since: $since}]->(n:Post $post)
RETURN n
"""

#PATCH
EDIT_POST = """MATCH(n:Post {id: $id}) SET n += $post RETURN n"""

#DELETE
DELETE_POST="""MATCH(n:Post {id: $id}) DETACH DELETE n"""
