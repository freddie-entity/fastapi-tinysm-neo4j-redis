#GET
GET_USERS="""MATCH (n:User) RETURN n"""
GET_USER_BY_USERNAME="""MATCH (n:User {username: $username}) RETURN n"""
GET_USER_LABEL_BY_USERNAME="""MATCH (n:User {username: $username}) RETURN labels(n)"""

GET_USER_FOLLOWING = """MATCH(m:User {username: $username})-[r:FOLLOWS]->(n) return n.username as following"""
GET_USER_FOLLOWER = """MATCH(m:User {username: $username})<-[r:FOLLOWS]-(n) return n.username as follower"""

GET_USER_RECOMMENDATION = """
    MATCH (a: User {username: $username})-[:FOLLOWS]-(b: User)-[:FOLLOWS]-(n: User) 
    WHERE NOT (a: User)-[:FOLLOWS]-(n: User) AND NOT n.username = $username  
    RETURN n;
"""

#POST
CREATE_USER="""CREATE(n: User $user) RETURN n"""
FOLLOW_USER="""
    MATCH (j: User {username: $me})
    MATCH (m: User {username: $you})
    MERGE (j)-[r: FOLLOWS {since: $since}]->(m)
    RETURN r
"""
UNFOLLOW_USER="""
    MATCH (j: User {username: $me})-[r:FOLLOWS]->(m: User {username: $you}) DELETE r
"""
LIKE_POST="""
    MATCH (j: User {username: $username})
    MATCH (m: Post {id: $post_id})
    MERGE (m)-[r: RECEIVE_POST_LIKE {since: $since}]->(j) RETURN r
"""
    # MATCH (m)-[c: RECEIVE_POST_LIKE]->(j)
    # WITH c
    # CALL apoc.do.when(c.since IS NOT NULL, 'DELETE c', 'MERGE (m)-[r: RECEIVE_POST_LIKE {since: $since}]->(j) RETURN r',{})
    # YIELD value
    # RETURN value.r

UNLIKE_POST="""
    MATCH (j: Post {id: $post_id})-[r:RECEIVE_POST_LIKE]->(m: User {username: $username}) DELETE r
"""
LIKE_COMMENT="""
    MATCH (j: User {username: $username})
    MATCH (m: Comment {id: $comment_id})
    MERGE (m)-[r: RECEIVE_COMMENT_LIKE {since: $since}]->(j)
    RETURN r
"""
UNLIKE_COMMENT="""
    MATCH (j: Comment {id: $comment_id})-[r:RECEIVE_COMMENT_LIKE]->(m: User {username: $username}) DELETE r
"""

JOIN_ROOM="""
    MATCH (j: User {username: $username})
    MATCH (m: Room {id: $room_id})
    MERGE (m)-[r: HAS_MEMBER {since: $since}]->(j)
    RETURN r
"""
LEAVE_ROOM="""
    MATCH (m: Room {id: $room_id})-[r:HAS_MEMBER]->(j: User {username: $username}) DELETE r
"""

#PATCH
EDIT_USER="""MATCH(n:User {username: $username}) SET n += $user RETURN n"""

#DELETE
DELETE_USER="""MATCH(n:User {username: $username}) DETACH DELETE n"""