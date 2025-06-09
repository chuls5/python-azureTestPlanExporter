import requests
import json
import csv
import argparse
import base64
from datetime import datetime
from typing import List, Dict, Any
import sys

class AzureTestPlanExporter:
    def __init__(self, organization: str, project: str, pat: str):
        self.organization = organization
        self.project = project
        self.pat = pat
        self.base_url = f"https://dev.azure.com/{organization}/{project}/_apis"
        
        # Create authentication header
        credentials = f":{pat}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        self.headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/json'
        }
        
    def make_request(self, url: str) -> Dict[Any, Any]:
        """Make authenticated request to Azure DevOps API"""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making request to {url}: {e}")
            return {}
    
    def get_test_plan(self, plan_id: str) -> Dict[Any, Any]:
        """Get test plan details"""
        url = f"{self.base_url}/testplan/plans/{plan_id}?api-version=7.1-preview.1"
        return self.make_request(url)
    
    def get_test_suites(self, plan_id: str) -> List[Dict[Any, Any]]:
        """Get all test suites for a plan"""
        url = f"{self.base_url}/testplan/Plans/{plan_id}/suites?api-version=7.1-preview.1"
        response = self.make_request(url)
        return response.get('value', [])
    
    def get_test_cases_for_suite(self, plan_id: str, suite_id: str) -> List[Dict[Any, Any]]:
        """Get test cases for a specific suite"""
        url = f"{self.base_url}/testplan/Plans/{plan_id}/Suites/{suite_id}/TestCase?api-version=7.1-preview.3"
        response = self.make_request(url)
        return response.get('value', [])
    
    def get_test_case_details(self, test_case_id: str) -> Dict[Any, Any]:
        """Get detailed test case information"""
        url = f"{self.base_url}/wit/workitems/{test_case_id}?api-version=7.1"
        return self.make_request(url)
    
    def get_test_points(self, plan_id: str, suite_id: str) -> List[Dict[Any, Any]]:
        """Get test points (execution status) for a suite"""
        url = f"{self.base_url}/testplan/Plans/{plan_id}/Suites/{suite_id}/TestPoint?includePointDetails=true&api-version=7.1-preview.2"
        response = self.make_request(url)
        return response.get('value', [])
    
    def get_test_runs_for_plan(self, plan_id: str) -> List[Dict[Any, Any]]:
        """Get test runs for a specific test plan"""
        url = f"{self.base_url}/test/runs?planId={plan_id}&api-version=7.1-preview.3"
        response = self.make_request(url)
        return response.get('value', [])
    
    def get_test_results_for_run(self, run_id: str) -> List[Dict[Any, Any]]:
        """Get test results for a specific test run"""
        url = f"{self.base_url}/test/Runs/{run_id}/results?api-version=7.1-preview.6"
        response = self.make_request(url)
        return response.get('value', [])
    
    def get_latest_test_result_for_case(self, test_case_id: str, plan_id: str) -> Dict[Any, Any]:
        """Get the latest test result for a specific test case"""
        # First, get all test runs for the plan
        test_runs = self.get_test_runs_for_plan(plan_id)
        
        latest_result = None
        latest_date = None
        
        for run in test_runs:
            run_id = str(run.get('id', ''))
            if not run_id:
                continue
                
            # Get results for this run
            results = self.get_test_results_for_run(run_id)
            
            for result in results:
                # Check if this result is for our test case
                result_test_case_id = str(result.get('testCase', {}).get('id', ''))
                if result_test_case_id == test_case_id:
                    completed_date = result.get('completedDate')
                    if completed_date and (latest_date is None or completed_date > latest_date):
                        latest_date = completed_date
                        latest_result = result
        
        return latest_result or {}
    
    def build_suite_path(self, suite: Dict[Any, Any], all_suites: List[Dict[Any, Any]]) -> str:
        """Build hierarchical path for a test suite"""
        path_parts = [suite.get('name', '')]
        current_suite = suite
        
        # Traverse up the parent hierarchy
        while current_suite.get('parentSuite') and current_suite.get('parentSuite', {}).get('id'):
            parent_id = current_suite['parentSuite']['id']
            parent_suite = next((s for s in all_suites if str(s.get('id')) == str(parent_id)), None)
            if parent_suite and parent_suite.get('name'):
                path_parts.insert(0, parent_suite['name'])
                current_suite = parent_suite
            else:
                break
        
        return ' > '.join(path_parts)
    
    def extract_test_data(self, plan_id: str) -> List[Dict[str, Any]]:
        """Extract all test data from a test plan"""
        print(f"Starting extraction for Test Plan ID: {plan_id}")
        
        # Get test plan details
        test_plan = self.get_test_plan(plan_id)
        if not test_plan:
            print(f"Could not retrieve test plan {plan_id}")
            return []
        
        print(f"Test Plan: {test_plan.get('name', 'Unknown')}")
        
        # Get all test suites
        test_suites = self.get_test_suites(plan_id)
        print(f"Found {len(test_suites)} test suites")
        
        # Get test runs for this plan to build execution history
        print("Fetching test execution history...")
        test_runs = self.get_test_runs_for_plan(plan_id)
        print(f"Found {len(test_runs)} test runs")
        
        # Build a comprehensive test results map
        test_results_map = {}
        for run in test_runs:
            run_id = str(run.get('id', ''))
            if not run_id:
                continue
            
            results = self.get_test_results_for_run(run_id)
            for result in results:
                test_case_id = str(result.get('testCase', {}).get('id', ''))
                if test_case_id:
                    completed_date = result.get('completedDate', '')
                    # Keep only the latest result for each test case
                    if (test_case_id not in test_results_map or 
                        completed_date > test_results_map[test_case_id].get('completedDate', '')):
                        test_results_map[test_case_id] = result
        
        all_test_data = []
        
        for suite in test_suites:
            suite_id = str(suite.get('id', ''))
            suite_name = suite.get('name', '')
            suite_path = self.build_suite_path(suite, test_suites)
            
            print(f"Processing suite: {suite_name} (ID: {suite_id})")
            
            # Get test cases for this suite
            test_cases = self.get_test_cases_for_suite(plan_id, suite_id)
            print(f"  Found {len(test_cases)} test cases in suite {suite_name}")
            
            # Get test points (execution status) for this suite
            test_points = self.get_test_points(plan_id, suite_id)
            
            # Create a mapping of test case ID to test point status
            test_point_map = {}
            for point in test_points:
                # Try different possible locations for test case ID in test points
                tc_id = str(point.get('testCaseReference', {}).get('id', ''))
                if not tc_id:
                    tc_id = str(point.get('testCase', {}).get('id', ''))
                if not tc_id:
                    tc_id = str(point.get('workItem', {}).get('id', ''))
                
                if tc_id:
                    test_point_map[tc_id] = {
                        'status': point.get('outcome', 'Not Executed'),
                        'lastResultOutcome': point.get('lastResultOutcome', ''),
                        'lastResultState': point.get('lastResultState', ''),
                        'assignedTo': point.get('assignedTo', {}).get('displayName', ''),
                    }
            
            for test_case in test_cases:
                # Extract test case ID from workItem.id
                tc_id = str(test_case.get('workItem', {}).get('id', ''))
                
                # Skip if no valid test case ID
                if not tc_id or tc_id == '':
                    print(f"Warning: No valid test case ID found in suite {suite_name}")
                    continue
                
                # Extract test case information directly from the API response
                work_item = test_case.get('workItem', {})
                work_item_fields = {field.get('key', ''): field.get('value', '') for field in work_item.get('workItemFields', [])}
                
                # Get test point status for this test case
                test_point_info = test_point_map.get(tc_id, {})
                
                # Get latest test result for this test case
                latest_test_result = test_results_map.get(tc_id, {})
                
                # Determine the actual execution status
                execution_status = 'Not Executed'
                execution_outcome = ''
                last_run_date = ''
                last_run_by = ''
                
                if latest_test_result:
                    execution_outcome = latest_test_result.get('outcome', '')
                    execution_status = latest_test_result.get('state', 'Not Executed')
                    last_run_date = latest_test_result.get('completedDate', '')
                    last_run_by = latest_test_result.get('runBy', {}).get('displayName', '')
                elif test_point_info.get('lastResultOutcome'):
                    execution_outcome = test_point_info.get('lastResultOutcome', '')
                    execution_status = test_point_info.get('lastResultState', 'Not Executed')
                
                # Extract assigned to from point assignments if available
                assigned_to = test_point_info.get('assignedTo', '')
                if not assigned_to and test_case.get('pointAssignments'):
                    first_assignment = test_case['pointAssignments'][0]
                    tester = first_assignment.get('tester') if first_assignment else None
                    if tester:
                        assigned_to = tester.get('displayName', '')
                
                test_data = {
                    'Test Plan ID': plan_id,
                    'Suite Path': suite_path,
                    'Suite ID': suite_id,
                    'Test Case ID': tc_id,
                    'Title': work_item.get('name', ''),
                    'Execution Status': execution_status,
                    'Execution Outcome': execution_outcome,
                    'Last Run Date': last_run_date,
                    'Last Run By': last_run_by,
                    'Assigned To': assigned_to,
                    'Created Date': work_item_fields.get('System.CreatedDate', ''),
                    'Created By': work_item_fields.get('System.CreatedBy', ''),
                    'Area Path': work_item_fields.get('System.AreaPath', ''),
                    'Iteration': work_item_fields.get('System.IterationPath', ''),
                    'Automated': 'Yes' if work_item_fields.get('Microsoft.VSTS.TCM.AutomatedTestName') else 'No'
                }
                
                all_test_data.append(test_data)
        
        print(f"Extracted {len(all_test_data)} test cases")
        return all_test_data
    
    def export_to_csv(self, test_data: List[Dict[str, Any]], filename: str = None):
        """Export test data to CSV file"""
        if not test_data:
            print("No test data to export")
            return
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_plan_export_{timestamp}.csv"
        
        fieldnames = [
            'Test Plan ID', 'Suite Path', 'Suite ID', 'Test Case ID', 
            'Title', 'Execution Status', 'Execution Outcome', 'Last Run Date',
            'Last Run By', 'Assigned To', 'Created Date', 
            'Created By', 'Area Path', 'Iteration', 'Automated'
        ]
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(test_data)
            
            print(f"Test data exported to {filename}")
            
        except Exception as e:
            print(f"Error writing CSV file: {e}")

def main():
    parser = argparse.ArgumentParser(description='Export Azure DevOps Test Plan data with execution results')
    parser.add_argument('--organization', required=True, help='Azure DevOps organization name')
    parser.add_argument('--project', required=True, help='Azure DevOps project name')
    parser.add_argument('--pat', required=True, help='Personal Access Token')
    parser.add_argument('--test-plan-id', required=True, help='Test Plan ID to export')
    parser.add_argument('--output', help='Output CSV filename (optional)')
    
    args = parser.parse_args()
    
    # Create exporter instance
    exporter = AzureTestPlanExporter(args.organization, args.project, args.pat)
    
    # Extract test data
    test_data = exporter.extract_test_data(args.test_plan_id)
    
    if test_data:
        # Export to CSV
        exporter.export_to_csv(test_data, args.output)
        
        # Print summary
        print(f"\nSummary:")
        print(f"Total test cases: {len(test_data)}")
        
        # Status breakdown
        outcome_counts = {}
        status_counts = {}
        for item in test_data:
            outcome = item['Execution Outcome'] or 'Not Executed'
            status = item['Execution Status'] or 'Not Executed'
            outcome_counts[outcome] = outcome_counts.get(outcome, 0) + 1
            status_counts[status] = status_counts.get(status, 0) + 1
        
        print("Execution Outcome breakdown:")
        for outcome, count in outcome_counts.items():
            print(f"  {outcome}: {count}")
            
        print("Execution Status breakdown:")
        for status, count in status_counts.items():
            print(f"  {status}: {count}")
    else:
        print("No test data found or extraction failed")

if __name__ == "__main__":
    main()
