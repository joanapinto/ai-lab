#!/usr/bin/env python3
"""
Command-line interface for Focus Companion database insights
"""

import sys
import os
import argparse
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.insights import DatabaseInsights, print_insights

def main():
    parser = argparse.ArgumentParser(description='Focus Companion Database Insights')
    parser.add_argument('--user', '-u', help='User email to analyze (optional)')
    parser.add_argument('--days', '-d', type=int, default=30, help='Number of days to analyze (default: 30)')
    parser.add_argument('--export', '-e', help='Export user data to JSON file')
    parser.add_argument('--global-insights', '-g', action='store_true', help='Show global insights only')
    parser.add_argument('--costs', '-c', action='store_true', help='Show cost analysis')
    parser.add_argument('--adoption', '-a', action='store_true', help='Show feature adoption analysis')
    
    args = parser.parse_args()
    
    # Restrict access to admin email only
    ADMIN_EMAIL = "joanapnpinto@gmail.com"
    
    # Check if user is trying to access insights
    if args.user and args.user != ADMIN_EMAIL:
        print("🔒 Access Restricted: Database insights are only available to administrators during beta testing.")
        return
    
    if args.global_insights or args.costs or args.adoption:
        print("🔒 Access Restricted: Global insights are only available to administrators during beta testing.")
        return
    
    insights = DatabaseInsights()
    
    print("🔍 Focus Companion Database Insights")
    print("=" * 60)
    
    if args.export:
        if not args.user:
            print("❌ Error: --export requires --user email")
            return
        filename = insights.export_user_data(args.user)
        print(f"✅ User data exported to: {filename}")
        return
    
    if args.global_insights or not args.user:
        # Show global insights
        print("🌍 Global Insights:")
        global_insights = insights.get_user_activity_summary(days=args.days)
        print_insights(global_insights)
        
        if args.adoption:
            print("📊 Feature Adoption Analysis:")
            adoption = insights.get_feature_adoption_analysis(days=args.days)
            if 'message' not in adoption:
                print(f"   Total Users: {adoption['total_users']}")
                for feature, data in adoption['feature_adoption'].items():
                    print(f"   • {feature}: {data['adoption_rate']}% adoption ({data['users']} users)")
            else:
                print(f"   {adoption['message']}")
        
        if args.costs:
            print("\n💰 Cost Analysis:")
            costs = insights.get_cost_analysis(days=args.days)
            if 'message' not in costs:
                print(f"   Total Cost: ${costs['total_cost']:.4f}")
                print(f"   Total Calls: {costs['total_calls']}")
                print(f"   Total Tokens: {costs['total_tokens']:,}")
                print(f"   Average Cost per Call: ${costs['average_cost_per_call']:.6f}")
                print(f"   Highest Cost User: {costs['highest_cost_user']}")
                print(f"   Costliest Feature: {costs['costliest_feature']}")
            else:
                print(f"   {costs['message']}")
    
    if args.user:
        # Show user-specific insights
        print(f"\n👤 User Insights for: {args.user}")
        user_insights = insights.get_user_activity_summary(args.user, days=args.days)
        print_insights(user_insights)

if __name__ == "__main__":
    main() 