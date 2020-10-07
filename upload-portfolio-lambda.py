import StringIO
import zipfile
import mimetypes

import boto3
from botocore.client import Config




def lambda_handler(event, context):
    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-2:394994090208:deployPortfolioTopic')
    
    location = {
        "bucketName": 'portfoliobuild.blualism.com',
        "objectKey": 'portfoliobuild.zip'
    }
    
    job = event.get('CodePipeline.job')
    if job:
        for artifact in job["data"]["inputArtifacts"]:
            if artifact["name"] == "MyAppBuild":
                location = artifact["location"]["s3Location"]
    
    print "Building portfolio from " + str(location)
    
    
    
    try:
        s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))
        
        portfolio_bucket = s3.Bucket('portfolio.blualism.com')
        build_bucket = s3.Bucket(location["bucketName"])
        
        portfolio_zip = StringIO.StringIO()
        build_bucket.download_fileobj(location["objectKey"], portfolio_zip)
        
        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                portfolio_bucket.upload_fileobj(obj, nm,
                ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
                portfolio_bucket.Object(nm).Acl().put(ACL='public-read')
        
        
        print "Job done"
        topic.publish(Subject='Portfolio Deployed', Message="Portfolio deployed successfully.")
        if job:
            codepipeline = boto3.client('codepipeline')
            codepipeline.put_job_success_result(jobId=job["id"])
    except:
        topic.publish(Subject='Portfolio Deployed Failed', Message="The portfolio was not deployed successfully.")
        raise
    
    return "Hello from lambda"