import boto3
import os
os.environ['AWS_PROFILE'] = "aws-cvent-sandbox"

DYNAMO_DB_CLIENT = boto3.resource('dynamodb', region_name="us-east-1")

ASSET_DB_NAME="ddb_table2"

items= [{'id': '1', 'Department': 'IT', 'Name': 'James Bond', 'Email': 'jbond@cvent.com'},
        {'id': '2', 'Department': 'Cloud', 'Name': 'Karuna Adhikari', 'Email': 'Karuna.Adhikari@cvent.com'}, 
        {'id': '3', 'Department': 'Sales', 'Name': 'Lexi Gomez', 'Email': 'lgomez@cvent.com'}, 
        {'id': '4', 'Department': 'Security', 'Name': 'Rachel Bank', 'Email': 'rbank@cvent.com'}]

# Create the DynamoDB table
def create_ddb_table(table_name):
    table = DYNAMO_DB_CLIENT.create_table(
        TableName= table_name,
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'Email',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'Email',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    print(table)
table_name='Users_table'


#list of tables
def list_dynamodb_table():
    print(list(DYNAMO_DB_CLIENT.tables.all()))

import datetime

import datetime

def put_items_in_dynamo_db(items):
    current_time = datetime.datetime.now().isoformat()
    
    table = DYNAMO_DB_CLIENT.Table(ASSET_DB_NAME)
    with table.batch_writer() as batch:
        for item in items:
            item['LastModified'] = current_time  # Add the last modified timestamp
            batch.put_item(Item=item)


# List items in the table
def list_items():
    table = DYNAMO_DB_CLIENT.Table(ASSET_DB_NAME)
    response = table.scan()
    items = response['Items']
    
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response['Items'])
    
    for item in items:
        print(item)
    
    return items


#get item
def get_item():
    table = DYNAMO_DB_CLIENT.Table(ASSET_DB_NAME)
    response=table.get_item(
        Key={
            'id': '2',
            'Email': 'Karuna.Adhikari@cvent.com'
        }
    )
    item = response.get('Item')
    print(item)

# Delete item
def delete_item():
    table = DYNAMO_DB_CLIENT.Table(ASSET_DB_NAME)
    response = table.delete_item(
        Key={
            'id': '1',
            'Email': 'jbond@cvent.com'
        }
    )
    print("Item deleted successfully")

# Update item
def update_item():
    table = DYNAMO_DB_CLIENT.Table(ASSET_DB_NAME)
    
    response = table.update_item(
        Key={
            'id': '5',
            'Email': 'stoner@cvent.com'
        },
        UpdateExpression='SET #nm = :new_name, #dep = :new_department',
        ExpressionAttributeNames={
            '#nm': 'Name',
            '#dep': 'Department'
        },
        ExpressionAttributeValues={
            ':new_name': 'Sarah Toner',
            ':new_department': 'SDT'
        }
    )
    
    print("Item updated successfully")




#create_ddb_table(ASSET_DB_NAME)
#list_dynamodb_table()
#put_items_in_dynamo_db(items)
#list_items()
get_item()
#delete_item()
#update_item()
