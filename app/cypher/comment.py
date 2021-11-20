#GET
GET_COMMENT_BY_ID = """MATCH(n:Comment {id: $id}) RETURN n"""
GET_COMMENT_BY_POST_ID = """MATCH(n:Comment {post_id: $post_id}) RETURN n"""
GET_COMMENT_BY_USERNAME = """MATCH(n:Comment {username: $username}) RETURN n"""
GET_COMMENTS = """MATCH(n:Comment) RETURN n"""

#POST
CREATE_COMMENT ="""
    MATCH(m:User {username: $username})
    MATCH(p:Post {id: $post_id})
    CREATE(m)-[r:IS_COMMENTATOR {since: $since}]->(n:Comment $comment)<-[pr:HAS_COMMENT {since: $since}]-(p)
    RETURN n
"""

#PATCH
EDIT_COMMENT = """MATCH(n:Comment {id: $id}) SET n += $comment RETURN n"""

#DELETE
DELETE_COMMENT="""MATCH(n:Comment {id: $id}) DETACH DELETE n"""
