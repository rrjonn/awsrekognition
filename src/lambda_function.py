import logging
import boto3
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("Lambda function started")
    logger.info(f"Received event: {event}")
    try:
        s3 = boto3.client('s3')
        rekognition = boto3.client('rekognition')

        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']

        logger.info(f"Processing image from S3: {bucket}/{key}")
        if key.endswith('.jpg') or key.endswith('.jpeg') or key.endswith('.png'):
            logger.info("Image format is valid")
        else:
            logger.error("Invalid image format")
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid image format'})
            }

        s3_response = s3.get_object(Bucket=bucket, Key=key)
        logger.info(f"S3 object retrieved: {s3_response['ContentLength']} bytes")

        response = rekognition.detect_labels(
            Image={'S3Object': {'Bucket': bucket, 'Name': key}},
            MaxLabels=10,
            MinConfidence=70
        )
        logger.info("Rekognition request sent")
        logger.info(f"Rekognition response: {response}")

        labels = response['Labels']
        logger.info(f"Rekognition output - Labels: {json.dumps(labels)}")

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Image processed successfully',
                'labels': labels
            })
        }
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }