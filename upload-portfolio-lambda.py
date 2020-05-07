import json
import boto3
import StringIO
import zipfile
from botocore.client import Config

def lambda_handler(event, context):
    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-1:329079609737:deployPortfolioTopic')

    location = {
        "bucketName": 'portfoliobuild.robertlitchfield.info',
        "objectKey": 'portfoliobuild'
    }
    try:
        job = event.get('CodePipeline.job')

        if job:
            for artifact in job["data"]["inputArtifacts"]:
                if artifact['name'] == "MyAppBuild":
                    location = artifact["location"]["s3Location"]

        print "Building portfolio from " + str(location)

        s3 = boto3.resource('s3', config = Config(signature_version = 's3v4'))

        build_bucket = s3.Bucket(location["bucketName"])
        portfolio_bucket = s3.Bucket('portfolio.robertlitchfield.info')


        portfolio_zip = StringIO.StringIO()
        build_bucket.download_fileobj(location["objectKey"], portfolio_zip)

        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                portfolio_bucket.upload_fileobj(obj, nm)
                portfolio_bucket.Object(nm).Acl().put(ACL='public-read')

        topic.publish(Subject="Portfolio Deployed", Message="Portfolio deployed successfully!")
        if job:
            codepipline = boto3.client('codepipeline')
            codepipline.put_job_success_result(jobId=job["id"])
    except:
        topic.publish(Subject="Portfolio Deploy Failed", Message="The Portfolio was not deployed!")
        raise
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
