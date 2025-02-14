#!/bin/bash

# Function to check if a package is installed
package_installed() {
    dpkg -s "$1" > /dev/null 2>&1 || rpm -q "$1" > /dev/null 2>&1
}

# Function to check the OS version
get_os_version() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        echo "$VERSION_ID"
    fi
}

# Function to install packages based on OS version
install_packages() {
    local os_version=$1

    case $os_version in
        6*)
            echo "Installing policycoreutils-python on RHEL 6/CentOS 6/Oracle Linux 6..."
            sudo yum install -y policycoreutils-python
            ;;
        7*)
            echo "Installing policycoreutils-python and selinux-policy-devel on RHEL 7/CentOS 7/Oracle Linux 7..."
            sudo yum install -y policycoreutils-python selinux-policy-devel
            ;;
        8*|9*)
            echo "Installing policycoreutils-python-utils and selinux-policy-devel on RHEL 8/9, CentOS 8, Oracle Linux 8/9, Alma Linux 8/9, and Rocky Linux 8/9..."
            sudo yum install -y policycoreutils-python-utils selinux-policy-devel
            ;;
        *)
            echo "Unsupported or unknown version of Red Hat-based Linux. Exiting..."
            exit 1
            ;;
    esac
}

# Check and install package
os_version=$(get_os_version)

if [ -n "$os_version" ]; then
    echo "Detected Red Hat-based Linux version: $os_version"

    if ! package_installed policycoreutils-python && ! package_installed selinux-policy; then
        echo "policycoreutils-python and selinux-policy packages are not installed. Installing..."
        install_packages "$os_version"
    else
        echo "policycoreutils-python and selinux-policy packages are already installed."
    fi
else
    echo "Failed to detect Red Hat-based Linux version. Exiting..."
    exit 1
fi

# Install XDR Agent
echo "Installing Cortex XDR Agent"
tar -xvf XDRAgent*.gz
mkdir -p /etc/panw
cp cortex.conf /etc/panw
chmod +x cortex*.sh
./cortex-8.4.0.123787.sh --target /home/ec2-user

# Install XDR Collector
echo "Installing Cortex XDR Collector"
tar -xvf LogCollector*.gz
cp collector.conf /etc/panw
chmod +x collector*.sh
./collector-1.4.1.1089.sh --target /home/ec2-user
