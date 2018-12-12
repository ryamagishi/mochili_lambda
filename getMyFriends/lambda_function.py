import boto3
from boto3.dynamodb.conditions import Key, Attr
import util

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    # 送られてくるUserId, CognitoIdを取得
    userId = event['UserId']
    cognitoId = event['CognitoId']

    # checkUser
    if not (util.checkUser(userId, cognitoId)):
        return []

    # Friendsテーブルより友達のUserIdであるFriendIdを取得
    friendsTable = dynamodb.Table('Friends')
    friendsResponse = friendsTable.query(
        KeyConditionExpression=Key('UserId').eq(userId)
    )

    # 取得したFriendIdよりUserテーブルから各User情報を取得
    usersTable = dynamodb.Table('Users')
    friends = []
    for friendItem in friendsResponse['Items']:
        friendId = friendItem['FriendId']
        userResponse = usersTable.get_item(
            Key={
                'UserId': friendId
            }
        )
        # friendsのcreatedAt,updatedAtはFriendsテーブルデータより設定
        friend = {}
        friend['FriendId'] = userResponse['Item']['UserId']
        friend['FriendName'] = userResponse['Item']['UserName']
        friend['CreatedAt'] = friendItem['CreatedAt']
        friend['UpdatedAt'] = friendItem['UpdatedAt']
        friends.append(friend)

    # userの配列であるfriendsを返す
    return friends
