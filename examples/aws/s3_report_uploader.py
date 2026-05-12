#!/usr/bin/env python3
"""Sube reportes de pentest a S3 cifrado automáticamente"""

import boto3
import os
from pathlib import Path

s3 = boto3.client('s3')
BUCKET = 'kalighost-reports-secure'

def upload_report(local_path, client_id):
    """Upload report to encrypted S3 bucket"""
    
    filename = Path(local_path).name
    s3_key = f"reports/{client_id}/{filename}"
    
    s3.upload_file(
        local_path, BUCKET, s3_key,
        ExtraArgs={
            'ServerSideEncryption': 'AES256',
            'Metadata': {
                'client': client_id,
                'pentest-type': 'automated'
            }
        }
    )
    
    # Generate presigned URL (expires in 7 days)
    url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': BUCKET, 'Key': s3_key},
        ExpiresIn=604800
    )
    
    print(f"✅ Uploaded: {url}")
    return url

if __name__ == '__main__':
    upload_report('/root/work/reports/audit.pdf', 'client_acme_corp')