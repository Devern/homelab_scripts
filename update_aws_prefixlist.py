import boto3
import requests

client = boto3.client('ec2')
PREFIX_LIST_ID = "santizedfortheweb"


def get_current_ip():
    request = requests.get('https://canhazip.com')
    wan_ip = f"{request.text.strip()}/32"
    return wan_ip


def query_prefix_list():
    response = client.get_managed_prefix_list_entries(
        PrefixListId=PREFIX_LIST_ID
    )
    prefix = response['Entries'][0]['Cidr']
    return prefix


def update_prefix_list():
    new_prefix = get_current_ip()
    old_prefix = query_prefix_list()
    if not old_prefix == new_prefix:
        response = client.modify_managed_prefix_list(
            PrefixListId=PREFIX_LIST_ID,
            AddEntries=[
                {
                    'Cidr': f'{new_prefix}',
                    'Description': 'home-ip'
                },
            ],
            RemoveEntries=[
                {
                    'Cidr': f'{old_prefix}'
                },
            ]
        )
        return response
    else:
        print("The IP is already up to date")
        print(f"Current prefix in AWS: {old_prefix}")
        print(f"New prefix from canhazip.com: {new_prefix}")
        return False


update_prefix_list()
