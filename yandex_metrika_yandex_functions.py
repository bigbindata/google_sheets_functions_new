import requests
import datetime


def create_file_with_id(data_str, id_type="ClientId"):
    """Ожидает строку 1,33591247640966E+017,test,1694362637,123.45,RUB"""

    return f"{id_type},Target,DateTime,Price,Currency\n" + data_str +"\n"


def handler(event, context):
    params=event['queryStringParameters']

    id_types = {"USER_ID":"UserId",
     "CLIENT_ID":"ClientId",
     "YCLID":"Yclid"}

    id_type = params[ "id_type" ] #"CLIENT_ID"
    id_visitor = params[id_type]
    timestamp_now = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    price = params.get('price',0.0)
    currency = params.get('currency','RUB')

    data = (id_visitor, params['target'], timestamp_now, price, currency )
    data_str = ",".join(map(str,data))

    headers = {
              "Authorization": f"OAuth {params['token']}",
            }

    url_upload_offline_conversion=f"https://api-metrika.yandex.net/management/v1/counter/{params['counterId']}/offline_conversions/upload?client_id_type={id_type}"

    string_file = create_file_with_id(data_str,id_type=id_types[id_type])
    response = requests.post(url_upload_offline_conversion, headers=headers, files={"file":string_file})


    return {
        'statusCode': response.status_code,
        'body': response.text,
    }