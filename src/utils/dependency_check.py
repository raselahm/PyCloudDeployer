import subprocess
import pkg_resources

REQUIRED_DEPENDENCIES = [
    'boto3',
    'botocore',
    'certifi',
    'charset-normalizer',
    'click',
    'colorama',
    'idna',
    'jmespath',
    'python-dateutil',
    'pytz',
    'requests',
    's3transfer',
    'six',
    'urllib3'
]

def check_dependencies():
    installed_packages = {pkg.key for pkg in pkg_resources.working_set}
    missing_packages = [pkg for pkg in REQUIRED_DEPENDENCIES if pkg not in installed_packages]

    if missing_packages:
        print(f"Missing packages: {', '.join(missing_packages)}")
        print("Installing required packages...")
        subprocess.check_call(["python", "-m", "pip", "install", *missing_packages])
        print("All required packages are now installed.")
    else:
        print("All required dependencies are already installed.")

    return not missing_packages

if __name__ == '__main__':
    check_dependencies()

