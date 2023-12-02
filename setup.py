import subprocess
import sys

REQUIRED_PYTHON_VERSION_MAJOR = 3
REQUIRED_PYTHON_VERSION_MINOR = 7


def setup_environment(requirements_path):
    # Checking Python version
    python_version = sys.version_info
    print("Python Version Installed: {0}.{1}".format(python_version.major, python_version.minor))

    if python_version.major < REQUIRED_PYTHON_VERSION_MAJOR or \
       (python_version.major == REQUIRED_PYTHON_VERSION_MAJOR and python_version.minor < REQUIRED_PYTHON_VERSION_MINOR):
        raise SystemError(
            "Your Python version must be at least {0}.{1}"
                .format(REQUIRED_PYTHON_VERSION_MAJOR, REQUIRED_PYTHON_VERSION_MINOR)
        )

    def install_packages(package):
        print("Installing {}" .format(package))
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

    with open(requirements_path, 'r') as requirements_file:
        for dep in requirements_file:
            install_packages(dep.strip())

    print("All the packages are installed successfully.")