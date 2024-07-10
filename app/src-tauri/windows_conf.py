import json


def get_package_json():
    with open('app/package.json') as file:
        return json.loads(file.read())


def save_package_json(content: dict):
    with open('app/package.json', 'w+') as file:
        file.write(json.dumps(content))


if __name__ == '__main__':
    print("Making changes for Windows MSI build...")
    package = get_package_json()
    version = package.get('version', '')
    valid_version = version.split('-')[0]
    print(f"Changing {version} to {valid_version}...")
    package['version'] = valid_version
    save_package_json(package)

