# Image Label Detection Lambda

This AWS Lambda function processes images uploaded to an S3 bucket and uses Amazon Rekognition to detect labels (objects, scenes, etc.) in the images. It logs the process and returns the detected labels or an error if something goes wrong.

## Overview
- **Purpose**: Detects labels in JPG, JPEG, or PNG images uploaded to an S3 bucket.
- **AWS Services Used**: S3, Rekognition, Lambda.
- **Runtime**: Python 3.x (e.g., 3.9).

## How It Works
1. Triggered by an S3 upload event.
2. Checks if the uploaded file is a valid image (JPG, JPEG, or PNG).
3. Retrieves the image from S3.
4. Sends it to Rekognition to detect up to 10 labels with at least 70% confidence.
5. Returns the labels or an error message.

## Code
The main file is `lambda_function.py` (or adjust the name if yours differs). It includes:
- Logging for debugging and monitoring.
- Error handling for invalid formats or processing issues.
- Interaction with S3 and Rekognition via `boto3`.

### Example Output
- Success: `{"message": "Image processed successfully", "labels": [{"Name": "Dog", "Confidence": 95.3}, ...]}`
- Error: `{"error": "Invalid image format"}`

## AWS Setup
To recreate this in your AWS environment:

### Lambda Configuration
- **Runtime**: Python 3.9 (or your preferred version).
- **Memory**: 256 MB (adjust based on image size/performance needs).
- **Timeout**: 30 seconds (Rekognition calls might take a few seconds).
- **Handler**: `lambda_function.lambda_handler` (update if your file/function name differs).

### Trigger
- **S3 Bucket**: Create an S3 bucket (e.g., `my-image-bucket`).
- **Event**: Set an S3 trigger for `All object create events` (or filter to `*.jpg`, `*.jpeg`, `*.png`).
- Example: Trigger on uploads to `my-image-bucket/uploads/`.

### Permissions
- **IAM Role**: Attach a role to the Lambda with these policies:
  - `AmazonS3ReadOnlyAccess` (to get objects from S3).
  - `AmazonRekognitionFullAccess` (to call Rekognition).
- Example inline policy (if custom):
  ```json
  {
    "Version": "2012-10-17",
    "Statement": [
      {"Effect": "Allow", "Action": "s3:GetObject", "Resource": "arn:aws:s3:::my-image-bucket/*"},
      {"Effect": "Allow", "Action": "rekognition:DetectLabels", "Resource": "*"}
    ]
  }
