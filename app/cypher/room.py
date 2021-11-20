GET_ROOM_BY_ID="""MATCH(n:Room {id: $id}) RETURN n"""
GET_ROOMS="""MATCH(n:Room) RETURN n"""
GET_ROOMS_BY_USERNAME="""MATCH(n: Room)-[r:HAS_MEMBER]->(m: User {username: $username}) RETURN n
"""
CREATE_ROOM="""CREATE(n:Room $room) RETURN n"""
EDIT_ROOM = """MATCH(n:Room {id: $id}) SET n += $room RETURN n"""
DELETE_ROOM="""MATCH(n:Room {id: $id}) DETACH DELETE n"""