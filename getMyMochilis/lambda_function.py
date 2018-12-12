import boto3
from boto3.dynamodb.conditions import Key, Attr
import util

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    # 送られてくるUserIdを取得
    userId = event["UserId"]
    cognitoId = event['CognitoId']

    # checkUser
    if not (util.checkUser(userId, cognitoId)):
        return []

    # MochiliSharesテーブルよりシェアされているMochiliIdを取得
    mochiliSharesTable = dynamodb.Table('MochiliShares')
    mochiliSharesResponse = mochiliSharesTable.query(
        IndexName='UserId-MochiliId-index',
        KeyConditionExpression=Key('UserId').eq(userId)
    )

    # 取得したMochiliIdよりMochiliテーブルから各Mochili情報を取得
    mochilisTable = dynamodb.Table('Mochilis')
    mochilis = []
    for mochiliShare in mochiliSharesResponse['Items']:
        mochiliId = mochiliShare['MochiliId']
        mochiliResponse = mochilisTable.get_item(
            Key={
                'MochiliId': mochiliId
            }
        )
        mochili = mochiliResponse['Item']

        # mochiliMembersをMochiliSharesより取得
        mochiliMembersResponse = mochiliSharesTable.query(
            KeyConditionExpression=Key('MochiliId').eq(mochili['MochiliId'])
        )
        returnMochiliMembers = []
        for mochiliMember in mochiliMembersResponse['Items']:
            # mochiliIdよりmochiliNameを取得
            # Usersテーブルよりuserを取得
            usersTable = dynamodb.Table('Users')
            usersResponse = usersTable.get_item(
                Key={
                    'UserId': mochiliMember['UserId']
                }
            )
            returnMochiliMembers.append({
                'MemberId': usersResponse['Item']['UserId'],
                'MemberName': usersResponse['Item']['UserName']
            })

        # mochilisに追加
        mochili['MochiliMember'] = returnMochiliMembers
        mochilis.append(mochili)

    # mochiliの配列であるmochilisを返す
    return mochilis
