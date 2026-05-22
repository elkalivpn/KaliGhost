#!/usr/bin/env python3
"""
YouTube Content Creator for KaliGhost Pro
Automates the creation of tutorial content for YouTube
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

class YouTubeContentCreator:
    def __init__(self):
        self.content_dir = Path("~/KaliGhost/video_scripts").expanduser()
        self.output_dir = Path("~/KaliGhost/youtube_content").expanduser()
        self.output_dir.mkdir(exist_ok=True)
        
    def list_available_tutorials(self):
        """List all available tutorial scripts"""
        tutorials = []
        for file in self.content_dir.glob("*.md"):
            if file.name != "getting_started_tutorial.md":  # Skip intro since we're building from scratch
                tutorials.append(file.stem)
        return tutorials
    
    def create_video_metadata(self, tutorial_title):
        """Create metadata for YouTube video"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        metadata = {
            "title": f"[Tutorial] How to {tutorial_title} with KaliGhost Pro",
            "description": f"Learn how to {tutorial_title} efficiently using KaliGhost Pro's advanced features. This comprehensive tutorial covers all essential steps for cybersecurity professionals. Perfect for ethical hackers and penetration testers.\n\n✅ What you'll learn:\n- [Key point 1]\n- [Key point 2]\n- [Key point 3]\n\n🔗 Related Resources:\n- Official Documentation: kalighost.pro/docs\n- Download KaliGhost Pro: kalighost.pro/download\n- Community Forum: kalighost.pro/forum\n\n🔔 Don't forget to LIKE, COMMENT, and SUBSCRIBE for more cybersecurity content!",
            "tags": ["kali", "kalighost", "penetration testing", "hacking", "cybersecurity", "pentest", "tutorial", "ethical hacking", "bug bounty"],
            "publish_date": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "thumbnail_description": f"KaliGhost Pro - {tutorial_title} tutorial"
        }
        return metadata
    
    def prepare_video_files(self, tutorial_script):
        """Prepare all necessary files for video creation"""
        # This would typically:
        # 1. Convert markdown script to storyboard
        # 2. Generate voiceover script
        # 3. Prepare screen capture instructions
        # 4. Create metadata file
        print(f"Preparing files for tutorial: {tutorial_script}")
        print("This would normally involve:")
        print("1. Parsing markdown to storyboard")
        print("2. Generating voiceover script")
        print("3. Creating screen capture documentation")
        print("4. Generating metadata files")
        return True
    
    def main(self):
        """Main execution function"""
        print("=== KaliGhost YouTube Content Automator ===")
        print("1. List available tutorials") 
        print("2. Prepare content for new tutorial")
        print("3. Generate YouTube metadata")
        print("4. Exit")
        
        choice = input("Select an option (1-4): ").strip()
        
        if choice == "1":
            tutorials = self.list_available_tutorials()
            print("\nAvailable tutorials:")
            for i, tut in enumerate(tutorials, 1):
                print(f"{i}. {tut}")
                
        elif choice == "2":
            tutorial = input("Enter tutorial title: ").strip()
            if self.prepare_video_files(tutorial):
                print(f"Successfully prepared content for '{tutorial}'")
            else:
                print("Failed to prepare content")
                
        elif choice == "3":
            title = input("Enter tutorial title for metadata: ").strip()
            metadata = self.create_video_metadata(title)
            metadata_file = self.output_dir / f"metadata_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            print(f"Metadata saved to {metadata_file}")
            
        elif choice == "4":
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid option")

if __name__ == "__main__":
    creator = YouTubeContentCreator()
    creator.main()