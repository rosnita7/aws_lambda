import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('StudentRecords')

def lambda_handler(event, context):
    if event['httpMethod'] == 'POST':
        #Create new student record
        student = json.loads(event['body'])
        table.put_item(Item=student)
        return {
            'statusCode': 200,
            'body': json.dumps('Student record added successfully')
        }
    elif event['httpMethod'] == 'GET':
        #Fetch student record by ID
        student_id = event['queryStringParameters']['student_id']
        response = table.get_item(Key={'student_id': student_id})
        return {
            'statusCode': 200,
            'body': json.dumps(response['Item'])
        }
    elif event['httpMethod'] == 'PUT':
        #Update student record
        student = json.loads(event['body'])
        table.update_item(
            Key={'student_id': student['student_id']},
            UpdateExpression='SET #n = :val1, #c = :val2',
            ExpressionAttributeNames={'#n': 'name', '#c': 'course'},
            ExpressionAttributeValues={':val1': student['name'], ':val2': student['course']}
        )
        return {
            'statusCode': 200,
            'body': json.dumps('Student record updated successfully')
        }
    elif event['httpMethod'] == 'DELETE':
        #Delete student record
        student_id = event['queryStringParameters']['student_id']
        table.delete_item(Key={'student_id': student_id})
        return {
            'statusCode': 200,
            'body': json.dumps('Student record deleted successfully')
        }
