#!/usr/bin/env python3
# ENV Secret Shame Revealer - Because your API keys deserve better than public humiliation

import os
import re
import sys
from pathlib import Path

def find_env_files(start_path='.'):
    """Find .env files like they're embarrassing photos from your past"""
    env_files = []
    for root, dirs, files in os.walk(start_path):
        # Skip virtual environments - they have enough problems already
        dirs[:] = [d for d in dirs if not re.match(r'^(venv|env|.venv|node_modules)$', d)]
        for file in files:
            if file == '.env' or file.endswith('.env'):
                env_files.append(Path(root) / file)
    return env_files

def scan_for_secrets(file_path):
    """Look for secrets that shouldn't be on a public stage"""
    secret_patterns = [
        (r'(?i)(api[_-]?key|secret|token|password|passwd|pwd)[\s=:"]*[\w\d]{10,}', 'API Key/Secret'),
        (r'(?i)(aws[_-]?(access[_-]?key|secret[_-]?key))[\s=:"]*[\w\d/+]{20,}', 'AWS Credentials'),
        (r'(?i)(database|db)[\s=:"]*(postgresql|mysql|mongodb)://[\w\d:]+@', 'Database URL'),
        (r'sk_[\w\d]{24,}', 'Stripe Secret Key'),
        (r'gh[pous]_[\w\d]{36,}', 'GitHub Token'),
    ]
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception:
        return []
    
    findings = []
    for pattern, label in secret_patterns:
        matches = re.findall(pattern, content)
        for match in matches:
            # Show just enough to identify, not enough to steal
            if isinstance(match, tuple):
                secret_preview = match[0][:20] + '...' if len(match[0]) > 20 else match[0]
            else:
                secret_preview = match[:20] + '...' if len(match) > 20 else match
            findings.append(f"  • {label}: {secret_preview}")
    
    return findings

def main():
    """Main function - the moment of truth (and shame)"""
    print("🔍 ENV Secret Shame Revealer - Finding your accidental public secrets\n")
    
    env_files = find_env_files()
    
    if not env_files:
        print("✅ No .env files found! You're either perfect or very good at hiding.")
        return 0
    
    shame_level = 0
    
    for env_file in env_files:
        print(f"📁 Checking: {env_file}")
        findings = scan_for_secrets(env_file)
        
        if findings:
            shame_level += 1
            print("🚨 SECRETS FOUND! Your .env file is oversharing:")
            for finding in findings:
                print(finding)
            print(f"\n💡 Tip: Add '{env_file}' to .gitignore before someone 'borrows' your API keys\n")
        else:
            print("  ✅ No obvious secrets found (but are you sure about that?)\n")
    
    if shame_level > 0:
        print(f"🎭 Shame Level: {shame_level}/10 - Time to git rm --cached those .env files!")
        return 1
    
    print("🌟 No secrets found! Your .env files are appropriately private.")
    return 0

if __name__ == '__main__':
    sys.exit(main())