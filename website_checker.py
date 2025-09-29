#!/usr/bin/env python3
"""
Website Status Checker Tool
Author: Your Name
GitHub: himalhma-ship-timohammad
"""

import requests
import time
import socket
from datetime import datetime
import os
import sys

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Print tool banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║    ██╗    ██╗███████╗██████╗ ███████╗██████╗ ████████╗      ║
    ║    ██║    ██║██╔════╝██╔══██╗██╔════╝██╔══██╗╚══██╔══╝      ║
    ║    ██║ █╗ ██║█████╗  ██████╔╝█████╗  ██████╔╝   ██║         ║
    ║    ██║███╗██║██╔══╝  ██╔══██╗██╔══╝  ██╔══██╗   ██║         ║
    ║    ╚███╔███╔╝███████╗██████╔╝███████╗██║  ██║   ██║         ║
    ║     ╚══╝╚══╝ ╚══════╝╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝         ║
    ║                                                              ║
    ║                📡 WEBSITE STATUS CHECKER TOOL               ║
    ║                   GitHub Learning Project                   ║
    ║                                                              ║
    ║        [ CCS Team - Cyber Security Learning Tool ]          ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_single_website(url):
    """Check single website status"""
    try:
        # Add https:// if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        start_time = time.time()
        response = requests.get(url, timeout=10, allow_redirects=True)
        end_time = time.time()
        
        response_time = round((end_time - start_time) * 1000, 2)
        status_code = response.status_code
        
        if 200 <= status_code < 300:
            return "🟢 ONLINE", status_code, response_time
        elif 300 <= status_code < 400:
            return "🟡 REDIRECT", status_code, response_time
        elif 400 <= status_code < 500:
            return "🔴 CLIENT ERROR", status_code, response_time
        else:
            return "🔴 SERVER ERROR", status_code, response_time
            
    except requests.exceptions.RequestException as e:
        return "🔴 OFFLINE", "N/A", "N/A"

def check_multiple_websites(websites):
    """Check multiple websites"""
    print("\n" + "🔍 CHECKING WEBSITES STATUS".center(60, "="))
    print(f"\n{'Website':<25} {'Status':<15} {'Code':<8} {'Response Time'}")
    print("-" * 65)
    
    results = []
    
    for website in websites:
        status, code, response_time = check_single_website(website)
        print(f"{website:<25} {status:<15} {str(code):<8} {str(response_time) + ' ms' if response_time != 'N/A' else 'N/A'}")
        results.append({
            'website': website,
            'status': status,
            'code': code,
            'response_time': response_time
        })
        time.sleep(1)  # Delay between checks
    
    return results

def get_ip_address(domain):
    """Get IP address of a domain"""
    try:
        # Remove http:// or https://
        clean_domain = domain.replace('https://', '').replace('http://', '').split('/')[0]
        ip = socket.gethostbyname(clean_domain)
        return ip
    except socket.gaierror:
        return "Not found"

def save_report(results):
    """Save results to file"""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    report = f"""
╔══════════════════════════════════════════════════════════════╗
║                    WEBSITE STATUS REPORT                    ║
║                      CCS Team Tool                          ║
╚══════════════════════════════════════════════════════════════╝

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

📊 SUMMARY:
• Websites Checked: {len(results)}
• Online: {len([r for r in results if 'ONLINE' in r['status']])}
• Offline: {len([r for r in results if 'OFFLINE' in r['status']])}
• Errors: {len([r for r in results if 'ERROR' in r['status']])}

📋 DETAILED RESULTS:
"""
    
    for i, result in enumerate(results, 1):
        report += f"""
{'='*60}
[{i}] Website: {result['website']}
    Status: {result['status']}
    HTTP Code: {result['code']}
    Response Time: {result['response_time']}
    IP Address: {get_ip_address(result['website'])}
"""
    
    filename = f"website_report_{timestamp}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)
    
    return filename

def main_menu():
    """Display main menu"""
    print("\n" + "📱 MAIN MENU".center(50, "="))
    print("\n1. 🚀 Check Default Websites")
    print("2. 📝 Check Custom Websites")
    print("3. 📖 Load Websites from File")
    print("4. ℹ️  Tool Information")
    print("5. 🚪 Exit")
    
    while True:
        try:
            choice = input("\n👉 Enter your choice (1-5): ").strip()
            if choice in ['1', '2', '3', '4', '5']:
                return choice
            else:
                print("❌ Please enter a number between 1-5")
        except KeyboardInterrupt:
            print("\n\n👋 Thanks for using Website Status Checker!")
            sys.exit(0)

def check_default_websites():
    """Check default list of websites"""
    default_websites = [
        'google.com',
        'github.com',
        'youtube.com',
        'facebook.com',
        'twitter.com',
        'instagram.com',
        'linkedin.com',
        'wikipedia.org',
        'amazon.com',
        'netflix.com'
    ]
    
    results = check_multiple_websites(default_websites)
    return results

def check_custom_websites():
    """Check custom websites from user input"""
    print("\n" + "📝 CUSTOM WEBSITES CHECK".center(50, "="))
    print("\nEnter websites (one per line). Press Enter twice to finish:")
    
    websites = []
    while True:
        try:
            website = input().strip()
            if website == "":
                if len(websites) > 0:
                    break
                else:
                    print("❌ Please enter at least one website")
                    continue
            if website:
                websites.append(website)
        except KeyboardInterrupt:
            print("\n\n👋 Operation cancelled!")
            return []
    
    if websites:
        results = check_multiple_websites(websites)
        return results
    else:
        print("❌ No websites entered!")
        return []

def show_tool_info():
    """Show tool information"""
    print("\n" + "ℹ️  TOOL INFORMATION".center(50, "="))
    print("""
🔧 Website Status Checker Tool
📅 Version: 1.0
👨‍💻 Author: CCS Team
📧 GitHub: himalhma-ship-timohammad

🌟 Features:
• Check website status (Online/Offline)
• Measure response time
• Get IP addresses
• Generate detailed reports
• Support custom website lists

🛠️ Technologies:
• Python 3
• Requests library
• Socket programming

📊 Status Codes:
🟢 ONLINE (200-299) - Website is working
🟡 REDIRECT (300-399) - Website redirected
🔴 CLIENT ERROR (400-499) - Bad request
🔴 SERVER ERROR (500-599) - Server issue
🔴 OFFLINE - Cannot connect
""")

def main():
    """Main function"""
    try:
        clear_screen()
        print_banner()
        
        while True:
            choice = main_menu()
            
            if choice == '1':  # Check Default Websites
                print("\n" + "🚀 CHECKING DEFAULT WEBSITES".center(50, "="))
                results = check_default_websites()
                
            elif choice == '2':  # Check Custom Websites
                results = check_custom_websites()
                
            elif choice == '3':  # Load from file
                print("\n📁 This feature will be available in next version!")
                input("\nPress Enter to continue...")
                clear_screen()
                print_banner()
                continue
                
            elif choice == '4':  # Tool Info
                show_tool_info()
                input("\nPress Enter to continue...")
                clear_screen()
                print_banner()
                continue
                
            elif choice == '5':  # Exit
                print("\n🎉 Thanks for using Website Status Checker!")
                print("👋 Goodbye!")
                break
            
            # Save report if we have results
            if 'results' in locals() and results:
                print("\n" + "💾 SAVING REPORT".center(50, "="))
                filename = save_report(results)
                print(f"✅ Report saved as: {filename}")
                
                # Show quick summary
                online_count = len([r for r in results if 'ONLINE' in r['status']])
                offline_count = len([r for r in results if 'OFFLINE' in r['status']])
                print(f"\n📊 Quick Summary: {online_count} Online, {offline_count} Offline")
            
            input("\nPress Enter to continue...")
            clear_screen()
            print_banner()
            
    except KeyboardInterrupt:
        print("\n\n👋 Thanks for using Website Status Checker!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("🔧 Please check your internet connection and try again.")

if __name__ == "__main__":
    # Check if requests is installed
    try:
        import requests
    except ImportError:
        print("❌ Requests library is not installed!")
        print("💡 Install it using: pip install requests")
        sys.exit(1)
    
    main()
