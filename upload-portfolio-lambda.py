import json
import boto3
from botocore.client import Config
import StringIO
import zipfile
import mimetypes
def lambda_handler(event, context):
    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:ap-south-1:871283926265:deploy-portfolio-topic')
    try:
        s3 = boto3.resource('s3',config=Config(signature_version='s3v4'))
        
        portfolio_bucket = s3.Bucket('portfolio.harshitshukla.live')
        build_bucket = s3.Bucket('portfoliobuild.harshitshukla.live')
        
        portfolio_zip = StringIO.StringIO()
        build_bucket.download_fileobj('portfoliobuild.zip',portfolio_zip)
        
        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                portfolio_bucket.upload_fileobj(obj,nm)
                portfolio_bucket.Object(nm).Acl().put(ACL='public-read')
        topic.publish(Subject="Portfolio Deployed!",Message="Portfolio deployed succesfully!")
    except:
        topic.publish(Subject="Portfolio Deployment Unsuccessful!",Message="Portfolio NOT deployed succesfully!")
        raise
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
