def fetch_data_from_dynamo_db():
    
    table = DYNAMO_DB_CLIENT.Table(ASSET_DB_NAME)
    dynamodb_items = []
    
    kwargs = {
        'FilterExpression': AttributeExists(Attr("id")),
    }

    response = table.scan()

    isDbDataPending = True
    
    while isDbDataPending:
        isDbDataPending = True if 'LastEvaluatedKey' in response else False
        
        if response['Count'] > 0:
            dynamodb_items.extend(response['Items'])
        if isDbDataPending:
            kwargs['ExclusiveStartKey'] = response['LastEvaluatedKey']
            response = table.scan(**kwargs)        
    
    return dynamodb_items