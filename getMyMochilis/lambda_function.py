import boto3
from boto3.dynamodb.conditions import Key, Attr
import util

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    # 送られてくるUserIdを取得
    user_id = event["UserId"]
    cognito_id = event['CognitoId']

    # checkUser
    if not (util.check_user(user_id, cognito_id)):
        return []

    # MochiliSharesテーブルよりシェアされているMochiliIdを取得
    mochili_shares_table = dynamodb.Table('MochiliShares')
    mochili_shares_response = mochili_shares_table.query(
        IndexName='UserId-MochiliId-index',
        KeyConditionExpression=Key('UserId').eq(user_id)
    )

    # 取得したMochiliIdよりMochiliテーブルから各Mochili情報を取得
    mochilis_table = dynamodb.Table('Mochilis')
    mochilis = []
    for mochili_share in mochili_shares_response['Items']:
        mochili_id = mochili_share['MochiliId']
        mochili_response = mochilis_table.get_item(
            Key={
                'MochiliId': mochili_id
            }
        )
        mochili = mochili_response['Item']

        # mochiliMembersをMochiliSharesより取得
        mochili_members_response = mochili_shares_table.query(
            KeyConditionExpression=Key('MochiliId').eq(mochili['MochiliId'])
        )
        return_mochili_members = []
        for mochili_member in mochili_members_response['Items']:
            # mochiliIdよりmochiliNameを取得
            # Usersテーブルよりuserを取得
            users_table = dynamodb.Table('Users')
            users_response = users_table.get_item(
                Key={
                    'UserId': mochili_member['UserId']
                }
            )
            return_mochili_members.append({
                'MemberId': users_response['Item']['UserId'],
                'MemberName': users_response['Item']['UserName']
            })

        # mochilisに追加
        mochili['MochiliMember'] = return_mochili_members
        mochilis.append(mochili)

    # mochiliの配列であるmochilisを返す
    return mochilis
