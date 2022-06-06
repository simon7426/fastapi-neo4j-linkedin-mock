from datetime import datetime
from typing import Any, List, Type

from pydantic import BaseModel

from project.utils.exceptions import BAD_REQUEST_EXCEPTION, UserNotExist
from project.utils.schema import RelationShipSchema, User


def get_user(cls: Type[BaseModel], username: str, sess: Any) -> Type[BaseModel]:
    query = f"MATCH (a:User) WHERE a.username = '{username}' RETURN a"

    user_in_db = sess.run(query)
    record = user_in_db.single()
    if record:
        user_data = record["a"]
        return cls(**user_data)
    else:
        raise UserNotExist(username)


def create_user(parameters: dict[str, Any], sess: Any) -> User:
    query = "CREATE (user:User $params) RETURN user"
    response = sess.run(query=query, parameters={"params": parameters})
    user_data: Any = response.data()[0]["user"]
    user: User = User(**user_data)
    return user


def follow_user(user1: str, user2: str, sess: Any) -> RelationShipSchema:
    query = (
        f"MATCH (a:User) WHERE a.username = '{user1}'\n"
        f"MATCH (b:User) WHERE b.username = '{user2}'\n"
        "CREATE (a)-[relationship:Follows]->(b)\n"
        f"SET relationship.created_at = '{str(datetime.utcnow())}'\n"
        "RETURN relationship\n"
    )
    response = sess.run(query=query)
    record = response.single()
    if record:
        user_data = record["relationship"]
        return user_data
    else:
        raise BAD_REQUEST_EXCEPTION


def delete_follow(user1: str, user2: str, sess: Any) -> bool:
    query = (
        f"MATCH (a:User) WHERE a.username = '{user1}'\n"
        f"MATCH (b:User) WHERE b.username = '{user2}'\n"
        "MATCH (b)-[relationship:Follows]->(a)\n"
        "DELETE relationship\n"
    )
    response = sess.run(query=query)
    summary = response.consume()
    if summary.counters.relationships_deleted:
        return True
    else:
        return False


def get_requests(username: str, sess: Any) -> List[User] | None:
    query = (
        f"MATCH (a:User) WHERE a.username = '{username}'\n"
        "MATCH (b:User)-[relationship:Follows]->(a)\n"
        "RETURN b\n"
    )
    response = sess.run(query=query)
    record = response.data("b")
    if record:
        return [User(**val.get("b")) for val in record]
    else:
        return None


def send_request_validation(user1: str, user2: str, sess: Any) -> bool:
    query = (
        f"MATCH (a:User) WHERE a.username = '{user1}'\n"
        f"MATCH (b:User) WHERE b.username = '{user2}'\n"
        "MATCH (a:User)-[relationship:Follows]->(b)\n"
        "RETURN a\n"
    )
    response = sess.run(query=query)
    record = response.data("b")
    if record:
        return True
    else:
        return False


def friend_validation(user1: str, user2: str, sess: Any) -> bool:
    query = (
        f"MATCH (a:User) WHERE a.username = '{user1}'\n"
        f"MATCH (b:User) WHERE b.username = '{user2}'\n"
        "MATCH (a:User)-[relationship:Friends]-(b)\n"
        "RETURN a\n"
    )
    response = sess.run(query=query)
    record = response.data("b")
    if record:
        return True
    else:
        return False


def accept_friend_request(user1: str, user2: str, sess: any) -> RelationShipSchema:
    query = (
        f"MATCH (a:User) WHERE a.username = '{user1}'\n"
        f"MATCH (b:User) WHERE b.username = '{user2}'\n"
        "MATCH (b:User) -[old_rel:Follows]-> (a:User)\n"
        "CREATE (a)-[new_rel:Friends]->(b)\n"
        f'SET new_rel.created_at = "{str(datetime.utcnow())}"\n'
        "DELETE old_rel\n"
        "RETURN new_rel\n"
    )
    response = sess.run(query=query)
    record = response.single()
    if record:
        user_data = record["new_rel"]
        return user_data
    else:
        raise BAD_REQUEST_EXCEPTION


def list_friends(username: str, sess: Any) -> List[User] | None:
    query = (
        f"MATCH (a:User) WHERE a.username = '{username}'\n"
        "MATCH (b:User)-[relationship:Friends]-(a)\n"
        "RETURN b\n"
    )
    response = sess.run(query=query)
    record = response.data("b")
    if record:
        return [User(**val.get("b")) for val in record]
    else:
        return None


def delete_friend(user1: str, user2: str, sess: Any) -> bool:
    query = (
        f"MATCH (a:User) WHERE a.username = '{user1}'\n"
        f"MATCH (b:User) WHERE b.username = '{user2}'\n"
        "MATCH (b)-[relationship:Friends]-(a)\n"
        "DELETE relationship\n"
    )
    response = sess.run(query=query)
    summary = response.consume()
    if summary.counters.relationships_deleted:
        return True
    else:
        return False
