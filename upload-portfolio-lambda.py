import json
import boto3
import StringIO
import zipfile
from botocore.client import Config

def lambda_handler(event, context):
    s3 = boto3.resource('s3', config = Config(signature_version = 's3v4'))

    build_bucket = s3.Bucket('portfoliobuild.robertlitchfield.info')
    portfolio_bucket = s3.Bucket('portfolio.robertlitchfield.info')

    portfolio_zip = StringIO.StringIO()
    build_bucket.download_fileobj('portfoliobuild', portfolio_zip)

    with zipfile.ZipFile(portfolio_zip) as myzip:
    for nm in myzip.namelist():
        obj = myzip.open(nm)
        portfolio_bucket.upload_fileobj(obj, nm)
        portfolio_bucket.Object(nm).Acl().put(ACL='public-read')

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
