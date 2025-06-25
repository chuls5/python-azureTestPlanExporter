import requests
import json
import csv
import argparse
import base64
from datetime import datetime
from typing import List, Dict, Any, Optional
import sys
import xml.etree.ElementTree as ET
from html import unescape
import re
import logging
import os

class AzureTestPlanExporter:
    def __init__(self, organization: str, project: str, pat: str, debug: bool = False):
        self.organization = organization
        self.project = project
        self.pat = pat
        self.base_url = f"https://dev.azure.com/{organization}/{project}/_apis"
        
        # Set up logging
        self.debug = debug
        self.setup_logging()
        
        # Create authentication header
        credentials = f":{pat}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        self.headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/json'
        }
        
        self.logger.info(f"Initialized AzureTestPlanExporter for organization: {organization}, project: {project}")
        self.logger.debug(f"Base URL: {self.base_url}")
        
    def setup_logging(self):
        """Set up logging configuration"""
        # Create logger
        self.logger = logging.getLogger('AzureTestPlanExporter')
        self.logger.setLevel(logging.DEBUG if self.debug else logging.INFO)
        
        # Remove any existing handlers
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        
        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG if self.debug else logging.INFO)
        
        # Create formatter
        if self.debug:
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
            )
        else:
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # Create file handler for debug logs
        if self.debug:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            debug_filename = f"azure_exporter_debug_{timestamp}.log"
            file_handler = logging.FileHandler(debug_filename, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
            self.logger.info(f"Debug logging enabled. Debug file: {debug_filename}")
        
    def make_request(self, url: str) -> Dict[Any, Any]:
        """Make authenticated request to Azure DevOps API"""
        self.logger.debug(f"Making request to: {url}")
        
        try:
            response = requests.get(url, headers=self.headers)
            self.logger.debug(f"Response status code: {response.status_code}")
            
            if self.debug:
                self.logger.debug(f"Response headers: {dict(response.headers)}")
            
            response.raise_for_status()
            
            json_response = response.json()
            self.logger.debug(f"Response received. Data keys: {list(json_response.keys()) if isinstance(json_response, dict) else 'Non-dict response'}")
            
            if self.debug and isinstance(json_response, dict):
                # Log response size info
                if 'value' in json_response and isinstance(json_response['value'], list):
                    self.logger.debug(f"Response contains {len(json_response['value'])} items in 'value' array")
                
                # Log first few characters of response for debugging (truncated)
                response_str = json.dumps(json_response)[:500]
                self.logger.debug(f"Response preview: {response_str}...")
            
            return json_response
            
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP error for {url}: {e}")
            self.logger.error(f"Response status: {response.status_code}")
            self.logger.error(f"Response text: {response.text[:1000]}")
            return {}
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request error for {url}: {e}")
            return {}
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON decode error for {url}: {e}")
            self.logger.error(f"Response text: {response.text[:1000]}")
            return {}
    
    def get_test_plan(self, plan_id: str) -> Dict[Any, Any]:
        """Get test plan details"""
        self.logger.info(f"Fetching test plan details for ID: {plan_id}")
        url = f"{self.base_url}/testplan/plans/{plan_id}?api-version=7.1-preview.1"
        
        result = self.make_request(url)
        if result:
            self.logger.info(f"Successfully retrieved test plan: {result.get('name', 'Unknown')}")
            self.logger.debug(f"Test plan fields: {list(result.keys())}")
        else:
            self.logger.error(f"Failed to retrieve test plan {plan_id}")
            
        return result
    
    def get_test_suites(self, plan_id: str) -> List[Dict[Any, Any]]:
        """Get all test suites for a plan"""
        self.logger.info(f"Fetching test suites for plan ID: {plan_id}")
        url = f"{self.base_url}/testplan/Plans/{plan_id}/suites?api-version=7.1-preview.1"
        
        response = self.make_request(url)
        suites = response.get('value', [])
        
        self.logger.info(f"Found {len(suites)} test suites")
        if self.debug and suites:
            self.logger.debug(f"First suite structure: {list(suites[0].keys()) if suites else 'No suites'}")
            for i, suite in enumerate(suites[:3]):  # Log first 3 suites
                self.logger.debug(f"Suite {i+1}: ID={suite.get('id')}, Name='{suite.get('name')}', Type={suite.get('suiteType')}")
        
        return suites
    
    def get_test_cases_for_suite(self, plan_id: str, suite_id: str) -> List[Dict[Any, Any]]:
        """Get test cases for a specific suite"""
        self.logger.debug(f"Fetching test cases for suite ID: {suite_id}")
        url = f"{self.base_url}/testplan/Plans/{plan_id}/Suites/{suite_id}/TestCase?api-version=7.1-preview.3"
        
        response = self.make_request(url)
        test_cases = response.get('value', [])
        
        self.logger.debug(f"Found {len(test_cases)} test cases in suite {suite_id}")
        if self.debug and test_cases:
            self.logger.debug(f"First test case structure: {list(test_cases[0].keys()) if test_cases else 'No test cases'}")
            for i, tc in enumerate(test_cases[:2]):  # Log first 2 test cases
                tc_id = tc.get('workItem', {}).get('id', 'Unknown')
                self.logger.debug(f"Test Case {i+1}: ID={tc_id}, Keys={list(tc.keys())}")
        
        return test_cases
    
    def get_test_case_details(self, test_case_id: str) -> Dict[Any, Any]:
        """Get detailed test case information including test steps"""
        self.logger.debug(f"Fetching details for test case ID: {test_case_id}")
        url = f"{self.base_url}/wit/workitems/{test_case_id}?$expand=all&api-version=7.1"
        
        result = self.make_request(url)
        if result:
            fields = result.get('fields', {})
            title = fields.get('System.Title', 'Unknown')
            self.logger.debug(f"Retrieved test case '{title}' with {len(fields)} fields")
            
            # Check for test steps
            has_steps = 'Microsoft.VSTS.TCM.Steps' in fields
            self.logger.debug(f"Test case has steps: {has_steps}")
            if has_steps and self.debug:
                steps_xml = fields['Microsoft.VSTS.TCM.Steps']
                self.logger.debug(f"Steps XML length: {len(steps_xml) if steps_xml else 0}")
        else:
            self.logger.warning(f"Failed to retrieve details for test case {test_case_id}")
            
        return result
    
    def get_shared_steps_details(self, shared_steps_id: str) -> Dict[Any, Any]:
        """Get shared steps details"""
        self.logger.debug(f"Fetching shared steps details for ID: {shared_steps_id}")
        url = f"{self.base_url}/wit/workitems/{shared_steps_id}?$expand=all&api-version=7.1"
        
        result = self.make_request(url)
        if result:
            fields = result.get('fields', {})
            title = fields.get('System.Title', 'Unknown')
            self.logger.debug(f"Retrieved shared steps '{title}'")
        else:
            self.logger.warning(f"Failed to retrieve shared steps {shared_steps_id}")
            
        return result
    
    def get_test_points(self, plan_id: str, suite_id: str) -> List[Dict[Any, Any]]:
        """Get test points (execution status) for a suite"""
        self.logger.debug(f"Fetching test points for suite ID: {suite_id}")
        url = f"{self.base_url}/testplan/Plans/{plan_id}/Suites/{suite_id}/TestPoint?includePointDetails=true&api-version=7.1-preview.2"
        
        response = self.make_request(url)
        test_points = response.get('value', [])
        
        self.logger.debug(f"Found {len(test_points)} test points in suite {suite_id}")
        if self.debug and test_points:
            self.logger.debug(f"First test point structure: {list(test_points[0].keys()) if test_points else 'No test points'}")
            for i, tp in enumerate(test_points[:2]):  # Log first 2 test points
                tc_ref = tp.get('testCaseReference', {})
                tc_id = tc_ref.get('id', 'Unknown') if tc_ref else 'No reference'
                outcome = tp.get('outcome', 'Unknown')
                self.logger.debug(f"Test Point {i+1}: TestCase={tc_id}, Outcome={outcome}")
        
        return test_points
    
    def get_test_runs_for_plan(self, plan_id: str) -> List[Dict[Any, Any]]:
        """Get test runs for a specific test plan"""
        self.logger.info(f"Fetching test runs for plan ID: {plan_id}")
        url = f"{self.base_url}/test/runs?planId={plan_id}&api-version=7.1-preview.3"
        
        response = self.make_request(url)
        test_runs = response.get('value', [])
        
        self.logger.info(f"Found {len(test_runs)} test runs")
        if self.debug and test_runs:
            for i, run in enumerate(test_runs[:3]):  # Log first 3 runs
                run_id = run.get('id', 'Unknown')
                run_name = run.get('name', 'Unknown')
                state = run.get('state', 'Unknown')
                self.logger.debug(f"Test Run {i+1}: ID={run_id}, Name='{run_name}', State={state}")
        
        return test_runs
    
    def get_test_results_for_run(self, run_id: str) -> List[Dict[Any, Any]]:
        """Get test results for a specific test run"""
        self.logger.debug(f"Fetching test results for run ID: {run_id}")
        url = f"{self.base_url}/test/Runs/{run_id}/results?api-version=7.1-preview.6"
        
        response = self.make_request(url)
        results = response.get('value', [])
        
        self.logger.debug(f"Found {len(results)} test results in run {run_id}")
        if self.debug and results:
            outcomes = {}
            for result in results:
                outcome = result.get('outcome', 'Unknown')
                outcomes[outcome] = outcomes.get(outcome, 0) + 1
            self.logger.debug(f"Results breakdown for run {run_id}: {outcomes}")
        
        return results
    
    def get_latest_test_result_for_case(self, test_case_id: str, plan_id: str) -> Dict[Any, Any]:
        """Get the latest test result for a specific test case"""
        self.logger.debug(f"Finding latest test result for test case: {test_case_id}")
        
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
                        self.logger.debug(f"Found newer result for TC {test_case_id}: {completed_date}")
        
        if latest_result:
            self.logger.debug(f"Latest result for TC {test_case_id}: outcome={latest_result.get('outcome')}, date={latest_date}")
        else:
            self.logger.debug(f"No test results found for test case {test_case_id}")
        
        return latest_result or {}
    
    def clean_html_text(self, html_text: str) -> str:
        """Clean HTML text and convert to plain text"""
        if not html_text:
            return ""
        
        original_length = len(html_text)
        
        # Remove HTML tags
        clean_text = re.sub(r'<[^>]+>', '', html_text)
        # Unescape HTML entities
        clean_text = unescape(clean_text)
        # Remove extra whitespace
        clean_text = ' '.join(clean_text.split())
        clean_text = clean_text.strip()
        
        if self.debug and original_length > 0:
            self.logger.debug(f"Cleaned HTML: {original_length} -> {len(clean_text)} chars")
            if len(clean_text) > 100:
                self.logger.debug(f"Cleaned text preview: {clean_text[:100]}...")
        
        return clean_text
    
    def parse_test_steps(self, test_steps_xml: str) -> List[Dict[str, str]]:
        """Parse test steps XML and return list of steps with actions and expected results"""
        if not test_steps_xml:
            return []
        
        steps = []
        try:
            # Parse the XML
            root = ET.fromstring(test_steps_xml)
            
            # Find all step elements
            for step_elem in root.findall('.//step'):
                step_id = step_elem.get('id', '')
                step_type = step_elem.get('type', '')
                
                # Debugging output: Log the XML of the current step being parsed
                if self.debug:
                    self.logger.debug(f"Parsing step: {ET.tostring(step_elem, encoding='unicode')}")
                
                if step_type == 'ValidateStep':
                    # For ValidateStep, extract both action and expected result
                    parameterized_strings = step_elem.findall('parameterizedString')
                    if len(parameterized_strings) >= 2:
                        action = self.clean_html_text(parameterized_strings[0].text)
                        expected = self.clean_html_text(parameterized_strings[1].text)
                    else:
                        action = ''
                        expected = ''
                else:  # For ActionStep
                    # Get action (parameterizedString)
                    action_elem = step_elem.find('.//parameterizedString')
                    action = self.clean_html_text(action_elem.text if action_elem is not None else "")
                    expected = ''  # No expected result for ActionStep
                
                # Debugging output: Log the extracted action and expected result
                if self.debug:
                    self.logger.debug(f"Action: '{action}', Expected: '{expected}'")
                
                # Include steps that have either an action OR an expected result
                if action or expected:  # Changed this condition
                    steps.append({
                        'step_id': step_id,
                        'action': action,
                        'expected_result': expected
                    })
        
        except ET.ParseError as e:
            self.logger.error(f"Error parsing test steps XML: {e}")
            return []
        
        return steps
    
    def flatten_shared_steps(self, test_steps: List[Dict[str, str]], test_case_id: str) -> List[Dict[str, str]]:
        """Flatten shared steps by fetching their details and replacing references"""
        self.logger.debug(f"Flattening shared steps for test case {test_case_id}")
        
        flattened_steps = []
        shared_steps_found = 0
        
        for i, step in enumerate(test_steps):
            action = step.get('action', '')
            
            # Check if this step references shared steps (typically contains @SharedStepId)
            shared_step_match = re.search(r'@(\d+)', action)
            if shared_step_match:
                shared_step_id = shared_step_match.group(1)
                shared_steps_found += 1
                self.logger.info(f"  Fetching shared steps {shared_step_id} for test case {test_case_id}")
                
                # Get shared steps details
                shared_steps_details = self.get_shared_steps_details(shared_step_id)
                if shared_steps_details:
                    shared_steps_xml = shared_steps_details.get('fields', {}).get('Microsoft.VSTS.TCM.Steps', '')
                    if shared_steps_xml:
                        shared_steps = self.parse_test_steps(shared_steps_xml)
                        self.logger.debug(f"Parsed {len(shared_steps)} steps from shared steps {shared_step_id}")
                        
                        # Recursively flatten in case shared steps contain other shared steps
                        shared_steps = self.flatten_shared_steps(shared_steps, shared_step_id)
                        flattened_steps.extend(shared_steps)
                        self.logger.debug(f"Added {len(shared_steps)} flattened shared steps")
                    else:
                        self.logger.warning(f"No steps XML found in shared steps {shared_step_id}")
                        flattened_steps.append(step)
                else:
                    self.logger.warning(f"Could not retrieve shared steps {shared_step_id}")
                    flattened_steps.append(step)
            else:
                # Regular step, add as-is
                flattened_steps.append(step)
        
        if shared_steps_found > 0:
            self.logger.info(f"Processed {shared_steps_found} shared step references, result: {len(flattened_steps)} total steps")
        
        return flattened_steps
    
    def build_suite_hierarchy(self, suite: Dict[Any, Any], all_suites: List[Dict[Any, Any]]) -> List[str]:
        """Build hierarchical path for a test suite as a list"""
        suite_id = str(suite.get('id', ''))
        suite_name = suite.get('name', '')
        self.logger.debug(f"Building hierarchy for suite: {suite_name} (ID: {suite_id})")
        
        path_parts = []
        current_suite = suite
        depth = 0
        max_depth = 10  # Prevent infinite loops
        
        # Build path from current suite up to root
        while current_suite and depth < max_depth:
            suite_name = current_suite.get('name', '')
            if suite_name:
                path_parts.insert(0, suite_name)
                self.logger.debug(f"  Added to path: {suite_name}")
            
            # Move to parent
            parent_id = current_suite.get('parentSuite', {}).get('id') if current_suite.get('parentSuite') else None
            if parent_id:
                self.logger.debug(f"  Looking for parent suite ID: {parent_id}")
                current_suite = next((s for s in all_suites if str(s.get('id')) == str(parent_id)), None)
                if not current_suite:
                    self.logger.warning(f"  Parent suite {parent_id} not found in suite list")
            else:
                current_suite = None
            
            depth += 1
        
        if depth >= max_depth:
            self.logger.warning(f"Maximum hierarchy depth reached for suite {suite_id}")
        
        hierarchy_path = ' > '.join(path_parts)
        self.logger.debug(f"Final hierarchy path: {hierarchy_path}")
        return path_parts
    
    def extract_test_data_hierarchical(self, plan_id: str) -> List[Dict[str, Any]]:
        """Extract all test data from a test plan in hierarchical format"""
        self.logger.info(f"Starting hierarchical extraction for Test Plan ID: {plan_id}")
        
        # Get test plan details
        test_plan = self.get_test_plan(plan_id)
        if not test_plan:
            self.logger.error(f"Could not retrieve test plan {plan_id}")
            return []
        
        plan_name = test_plan.get('name', 'Unknown')
        self.logger.info(f"Test Plan: {plan_name}")
        
        # Get all test suites
        test_suites = self.get_test_suites(plan_id)
        if not test_suites:
            self.logger.error(f"No test suites found for plan {plan_id}")
            return []
        
        self.logger.info(f"Found {len(test_suites)} test suites")
        
        # Get test runs for this plan to build execution history
        self.logger.info("Fetching test execution history...")
        test_runs = self.get_test_runs_for_plan(plan_id)
        self.logger.info(f"Found {len(test_runs)} test runs")
        
        # Build a comprehensive test results map
        self.logger.info("Building test results map...")
        test_results_map = {}
        total_results = 0
        
        for run in test_runs:
            run_id = str(run.get('id', ''))
            if not run_id:
                continue
            
            results = self.get_test_results_for_run(run_id)
            total_results += len(results)
            
            for result in results:
                test_case_id = str(result.get('testCase', {}).get('id', ''))
                if test_case_id:
                    completed_date = result.get('completedDate', '')
                    # Keep only the latest result for each test case
                    if (test_case_id not in test_results_map or 
                        completed_date > test_results_map[test_case_id].get('completedDate', '')):
                        test_results_map[test_case_id] = result
        
        self.logger.info(f"Processed {total_results} total results, {len(test_results_map)} unique test cases with results")
        
        # Organize suites by hierarchy
        self.logger.info("Building suite hierarchy...")
        suite_hierarchy = {}
        for suite in test_suites:
            hierarchy_path = self.build_suite_hierarchy(suite, test_suites)
            suite_hierarchy[str(suite.get('id', ''))] = {
                'suite': suite,
                'hierarchy_path': hierarchy_path,
                'full_path': ' > '.join(hierarchy_path)
            }
        
        # Sort suites by hierarchy path for better organization
        sorted_suites = sorted(suite_hierarchy.values(), key=lambda x: x['full_path'])
        self.logger.info(f"Organized {len(sorted_suites)} suites by hierarchy")
        
        all_hierarchical_data = []
        total_test_cases = 0
        total_test_steps = 0
        
        for suite_info in sorted_suites:
            suite = suite_info['suite']
            suite_id = str(suite.get('id', ''))
            suite_name = suite.get('name', '')
            suite_path = suite_info['full_path']
            
            self.logger.info(f"Processing suite: {suite_name} (ID: {suite_id})")
            
            # Get test cases for this suite
            test_cases = self.get_test_cases_for_suite(plan_id, suite_id)
            self.logger.info(f"  Found {len(test_cases)} test cases in suite {suite_name}")
            
            if not test_cases:
                self.logger.debug(f"  Skipping suite {suite_name} - no test cases")
                continue
            
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
            
            self.logger.debug(f"  Created test point mapping for {len(test_point_map)} test cases")
            
            # Add suite header row
            all_hierarchical_data.append({
                'Type': 'Suite',
                'Test Plan ID': plan_id,
                'Suite Path': suite_path,
                'Suite ID': suite_id,
                'Test Case ID': '',
                'Title': f"SUITE: {suite_name}",
                'Step Number': '',
                'Step Action': '',
                'Expected Result': '',
                'Execution Status': '',
                'Execution Outcome': '',
                'Last Run Date': '',
                'Last Run By': '',
                'Assigned To': '',
                'Created Date': '',
                'Created By': '',
                'Area Path': '',
                'Iteration': '',
                'Automated': ''
            })
            
            suite_test_cases = 0
            suite_test_steps = 0
            
            for test_case in test_cases:
                # Extract test case ID from workItem.id
                tc_id = str(test_case.get('workItem', {}).get('id', ''))
                
                # Skip if no valid test case ID
                if not tc_id or tc_id == '':
                    self.logger.warning(f"    No valid test case ID found in suite {suite_name}")
                    continue
                
                self.logger.debug(f"    Processing test case {tc_id}")
                
                # Get detailed test case information including test steps
                test_case_details = self.get_test_case_details(tc_id)
                if not test_case_details:
                    self.logger.warning(f"    Could not get details for test case {tc_id}")
                    continue
                
                # Extract test case fields
                fields = test_case_details.get('fields', {})
                
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
                    self.logger.debug(f"    Test case {tc_id} has execution result: {execution_outcome}")
                elif test_point_info.get('lastResultOutcome'):
                    execution_outcome = test_point_info.get('lastResultOutcome', '')
                    execution_status = test_point_info.get('lastResultState', 'Not Executed')
                    self.logger.debug(f"    Test case {tc_id} has test point result: {execution_outcome}")
                else:
                    self.logger.debug(f"    Test case {tc_id} has no execution results")
                
                # Extract assigned to from point assignments if available
                assigned_to = test_point_info.get('assignedTo', '')
                if not assigned_to and test_case.get('pointAssignments'):
                    first_assignment = test_case['pointAssignments'][0]
                    tester = first_assignment.get('tester') if first_assignment else None
                    if tester:
                        assigned_to = tester.get('displayName', '')
                
                # Extract and parse test steps
                test_steps_xml = fields.get('Microsoft.VSTS.TCM.Steps', '')
                test_steps = self.parse_test_steps(test_steps_xml)
                
                # Flatten shared steps
                if test_steps:
                    original_step_count = len(test_steps)
                    test_steps = self.flatten_shared_steps(test_steps, tc_id)
                    if len(test_steps) != original_step_count:
                        self.logger.debug(f"    Flattened {original_step_count} -> {len(test_steps)} steps for TC {tc_id}")
                
                # Add test case header row
                test_case_data = {
                    'Type': 'Test Case',
                    'Test Plan ID': plan_id,
                    'Suite Path': suite_path,
                    'Suite ID': suite_id,
                    'Test Case ID': tc_id,
                    'Title': fields.get('System.Title', ''),
                    'Step Number': '',
                    'Step Action': '',
                    'Expected Result': '',
                    'Execution Status': execution_status,
                    'Execution Outcome': execution_outcome,
                    'Last Run Date': last_run_date,
                    'Last Run By': last_run_by,
                    'Assigned To': assigned_to,
                    'Created Date': fields.get('System.CreatedDate', ''),
                    'Created By': fields.get('System.CreatedBy', {}).get('displayName', ''),
                    'Area Path': fields.get('System.AreaPath', ''),
                    'Iteration': fields.get('System.IterationPath', ''),
                    'Automated': 'Yes' if fields.get('Microsoft.VSTS.TCM.AutomatedTestName') else 'No'
                }
                
                all_hierarchical_data.append(test_case_data)
                suite_test_cases += 1
                total_test_cases += 1
                
                # Add test steps as sub-rows
                for i, step in enumerate(test_steps, 1):
                    step_data = {
                        'Type': 'Test Step',
                        'Test Plan ID': plan_id,
                        'Suite Path': suite_path,
                        'Suite ID': suite_id,
                        'Test Case ID': tc_id,
                        'Title': '',
                        'Step Number': str(i),
                        'Step Action': step.get('action', ''),
                        'Expected Result': step.get('expected_result', ''),
                        'Execution Status': '',
                        'Execution Outcome': '',
                        'Last Run Date': '',
                        'Last Run By': '',
                        'Assigned To': '',
                        'Created Date': '',
                        'Created By': '',
                        'Area Path': '',
                        'Iteration': '',
                        'Automated': ''
                    }
                    all_hierarchical_data.append(step_data)
                    suite_test_steps += 1
                    total_test_steps += 1
            
            self.logger.info(f"  Suite {suite_name} processed: {suite_test_cases} test cases, {suite_test_steps} test steps")
            
            # Add blank row after each suite for better readability
            all_hierarchical_data.append({
                'Type': 'Separator',
                'Test Plan ID': '',
                'Suite Path': '',
                'Suite ID': '',
                'Test Case ID': '',
                'Title': '',
                'Step Number': '',
                'Step Action': '',
                'Expected Result': '',
                'Execution Status': '',
                'Execution Outcome': '',
                'Last Run Date': '',
                'Last Run By': '',
                'Assigned To': '',
                'Created Date': '',
                'Created By': '',
                'Area Path': '',
                'Iteration': '',
                'Automated': ''
            })
        
        self.logger.info(f"Extraction complete: {total_test_cases} test cases, {total_test_steps} test steps")
        self.logger.info(f"Total hierarchical data rows: {len(all_hierarchical_data)}")
        return all_hierarchical_data
    
    def export_hierarchical_to_csv(self, hierarchical_data: List[Dict[str, Any]], filename: str = None):
        """Export hierarchical test data to CSV file"""
        if not hierarchical_data:
            self.logger.error("No test data to export")
            return
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_plan_hierarchical_export_{timestamp}.csv"
        
        self.logger.info(f"Exporting {len(hierarchical_data)} rows to {filename}")
        
        fieldnames = [
            'Type', 'Test Plan ID', 'Suite Path', 'Suite ID', 'Test Case ID', 
            'Title', 'Step Number', 'Step Action', 'Expected Result',
            'Execution Status', 'Execution Outcome', 'Last Run Date',
            'Last Run By', 'Assigned To', 'Created Date', 
            'Created By', 'Area Path', 'Iteration', 'Automated'
        ]
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(hierarchical_data)
            
            self.logger.info(f"Successfully exported hierarchical test data to {filename}")
            
            # Log file size
            file_size = os.path.getsize(filename)
            self.logger.info(f"Output file size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
            
        except Exception as e:
            self.logger.error(f"Error writing CSV file: {e}")
            raise

def main():
    parser = argparse.ArgumentParser(description='Export Azure DevOps Test Plan data with hierarchical structure and test steps')
    parser.add_argument('--organization', required=True, help='Azure DevOps organization name')
    parser.add_argument('--project', required=True, help='Azure DevOps project name')
    parser.add_argument('--pat', required=True, help='Personal Access Token')
    parser.add_argument('--test-plan-id', required=True, help='Test Plan ID to export')
    parser.add_argument('--output', help='Output CSV filename (optional)')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    
    args = parser.parse_args()
    
    # Create exporter instance
    exporter = AzureTestPlanExporter(args.organization, args.project, args.pat, debug=args.debug)
    
    try:
        # Extract hierarchical test data
        hierarchical_data = exporter.extract_test_data_hierarchical(args.test_plan_id)
        
        if hierarchical_data:
            # Export to CSV
            exporter.export_hierarchical_to_csv(hierarchical_data, args.output)
            
            # Print summary
            suites = [row for row in hierarchical_data if row['Type'] == 'Suite']
            test_cases = [row for row in hierarchical_data if row['Type'] == 'Test Case']
            test_steps = [row for row in hierarchical_data if row['Type'] == 'Test Step']
            
            print(f"\n" + "="*50)
            print(f"EXPORT SUMMARY")
            print(f"="*50)
            print(f"Total suites: {len(suites)}")
            print(f"Total test cases: {len(test_cases)}")
            print(f"Total test steps: {len(test_steps)}")
            print(f"Total rows exported: {len(hierarchical_data)}")
            
            # Status breakdown for test cases only
            if test_cases:
                outcome_counts = {}
                status_counts = {}
                automation_counts = {'Yes': 0, 'No': 0}
                
                for item in test_cases:
                    outcome = item['Execution Outcome'] or 'Not Executed'
                    status = item['Execution Status'] or 'Not Executed'
                    automated = item['Automated']
                    
                    outcome_counts[outcome] = outcome_counts.get(outcome, 0) + 1
                    status_counts[status] = status_counts.get(status, 0) + 1
                    automation_counts[automated] = automation_counts.get(automated, 0) + 1
                
                print(f"\nExecution Outcome breakdown:")
                for outcome, count in sorted(outcome_counts.items()):
                    percentage = (count / len(test_cases)) * 100
                    print(f"  {outcome}: {count} ({percentage:.1f}%)")
                    
                print(f"\nExecution Status breakdown:")
                for status, count in sorted(status_counts.items()):
                    percentage = (count / len(test_cases)) * 100
                    print(f"  {status}: {count} ({percentage:.1f}%)")
                
                print(f"\nAutomation breakdown:")
                for automated, count in automation_counts.items():
                    percentage = (count / len(test_cases)) * 100
                    print(f"  {automated}: {count} ({percentage:.1f}%)")
                
                # Calculate average steps per test case
                if test_steps:
                    avg_steps = len(test_steps) / len(test_cases)
                    print(f"\nAverage test steps per test case: {avg_steps:.1f}")
            
        else:
            print("No test data found or extraction failed")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\nExport interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Export failed with error: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
