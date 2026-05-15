#!/bin/bash

# KaliGhost Partition Setup Script for macOS
# This script will partition your external drive for KaliGhost development

echo "KaliGhost External Drive Partition Setup"
echo "========================================"

# Check if a disk parameter was provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <disk_identifier>"
    echo "Example: $0 disk5"
    echo ""
    echo "Please identify your external disk using 'diskutil list' first."
    echo "WARNING: This will erase ALL data on the specified disk!"
    exit 1
fi

DISK=$1
echo "Setting up partitions on /dev/$DISK..."

# Confirm with user before proceeding
echo ""
echo "WARNING: This will completely erase ALL data on /dev/$DISK"
read -p "Are you sure you want to continue? (yes/no): " CONFIRM

if [[ ! "$CONFIRM" =~ ^[Yy][Ee][Ss]$ ]]; then
    echo "Operation cancelled."
    exit 1
fi

# Unmount the disk if it's mounted
echo "Unmounting disk..."
diskutil unmountDisk force /dev/$DISK

# Create two partitions:
# 1. 500GB exFAT partition named "KaliGhost" for the Kali Linux installation
# 2. Remaining space as exFAT partition named "KaliData" for general storage
echo "Creating partition map..."
sudo diskutil partitionDisk /dev/$DISK 2 GPT \
    exfat "KaliGhost" 500GB \
    exfat "KaliData" R

# Check if partitioning was successful
if [ $? -eq 0 ]; then
    echo "Partitions created successfully!"
    
    # Display the new partition layout
    echo ""
    echo "New partition layout:"
    diskutil list /dev/$DISK
    
    echo ""
    echo "Next steps for KaliGhost development:"
    echo "1. You can now install Kali Linux to the 'KaliGhost' partition"
    echo "2. The 'KaliData' partition can be used for storing your projects and data"
    echo "3. Both partitions use exFAT for maximum compatibility between macOS and Linux"
else
    echo "Failed to create partitions. Please check the error messages above."
    exit 1
fi

echo ""
echo "Setup complete!"
