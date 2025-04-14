#!/usr/bin/env python3

import os
import sys
import datetime
import argparse
from slugify import slugify

def create_post(title, tags=None):
    """
    Create a new draft post with the given title and optional tags.
    
    Args:
        title (str): The title of the post
        tags (list): Optional list of tags
    """
    if not title:
        print("Error: Title is required")
        sys.exit(1)
    
    # Create slugified filename
    slug = slugify(title)
    filepath = os.path.join('drafts', f"{slug}.md")
    
    # Check if file already exists
    if os.path.exists(filepath):
        print(f"Error: A draft with title '{title}' already exists at {filepath}")
        sys.exit(1)
    
    # Format tags for frontmatter
    formatted_tags = ""
    if tags:
        formatted_tags = "tags:\n"
        for tag in tags:
            formatted_tags += f"  - {tag}\n"
    
    # Create frontmatter
    frontmatter = f"""---
title: {title}
date_published: {datetime.date.today().strftime('%Y-%m-%d')}
{formatted_tags}---

"""
    
    # Write the file
    with open(filepath, 'w') as f:
        f.write(frontmatter)
    
    print(f"Created draft post: {filepath}")
    return filepath

def main():
    parser = argparse.ArgumentParser(description='Create a new draft post')
    parser.add_argument('title', type=str, nargs='?', help='Title of the post (defaults to today\'s date in friendly format)')
    parser.add_argument('--tags', '-t', nargs='+', help='Tags for the post')
    
    args = parser.parse_args()
    
    title = args.title
    if not title:
        today = datetime.date.today()
        title = today.strftime("%B %d, %Y")
        
    create_post(title, args.tags)

if __name__ == "__main__":
    main() 