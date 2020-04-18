import boto3
import json
import decimal
import botocore.exceptions


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


db = boto3.resource('dynamodb', region_name='us-west-1',
                    endpoint_url='http://localhost:8888')


def fetch_all(table):
    try:
        table = db.Table(table)
        response = table.scan()

        for item in response['Items']:
            print(json.dumps(item, indent=4, cls=DecimalEncoder))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    fetch_all('unknown')
