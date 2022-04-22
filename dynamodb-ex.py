import boto3


def sync_tables(event, context):
    source_ddb = boto3.client('dynamodb', 'us-east-1')
    destination_ddb = boto3.client('dynamodb', 'us-west-2')
    sync_ddb_table(source_ddb, destination_ddb)


# Scan returns paginated results, so only partial data will be copied
def sync_ddb_table(source_ddb, destination_ddb):
    table = source_ddb.Table("<FMI1>")
    scan_kwargs = {
        'ProjectionExpression': "Artist, SongTitle"
    }
    done = False
    start_key = None
    while not done:
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key
        response = table.scan(**scan_kwargs)
        for item in response['Items']:
            new_item = {'Artist': {}, 'SongTitle': {}}
            new_item['Artist']['S'] = item['Artist']
            new_item['SongTitle']['S'] = item['SongTitle']
            destination_ddb.put_item(TableName="CodeGuru-MusicCollection", Item=new_item)
            print(item)
        start_key = response.get('LastEvaluatedKey', None)
        done = start_key is None
