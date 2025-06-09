# 🧪 Azure DevOps Test Plan Exporter

> 📊 Export your Azure DevOps test plans with execution results to CSV format

This Python script extracts comprehensive test case information from Azure DevOps test plans, including execution status (Pass/Fail), assigned testers, and test case details. Perfect for reporting, analysis, and tracking test progress!

## ✨ Features

- 🔍 **Complete Test Data Extraction**: Pulls all test cases from every suite in a test plan
- ✅ **Execution Results**: Captures actual Pass/Fail status and execution history
- 👥 **Assignment Tracking**: Shows who's assigned to run each test and who last executed it
- 📅 **Date Tracking**: Includes creation dates and last execution dates
- 🤖 **Automation Detection**: Identifies which tests are automated vs manual
- 📈 **Summary Statistics**: Provides execution outcome breakdowns
- 💾 **CSV Export**: Clean, organized output ready for Excel or data analysis

## 📋 Prerequisites

Before you start, make sure you have:

- 🐍 **Python 3.6+** installed
- 🔑 **Azure DevOps Personal Access Token (PAT)** with Test Management permissions
- 📦 **Required Python packages**: `requests` (install with `pip install requests`)

## 🚀 Quick Start

### 1️⃣ Clone or Download the Script

Save the Python script as `azure_test_exporter.py`

### 2️⃣ Install Dependencies

```bash
pip install requests
```

### 3️⃣ Get Your Azure DevOps Information

You'll need:

- 🏢 **Organization Name**: From your Azure DevOps URL (`https://dev.azure.com/YOUR_ORG`)
- 📁 **Project Name**: Your Azure DevOps project name
- 🔑 **Personal Access Token**: Create one in Azure DevOps User Settings
- 🧪 **Test Plan ID**: Found in the URL when viewing your test plan

### 4️⃣ Create a Personal Access Token

1. Go to Azure DevOps → User Settings → Personal Access Tokens
2. Click "New Token"
3. Give it a name like "Test Plan Exporter"
4. Set expiration as needed
5. Under Scopes, select:
   - ✅ **Test Management** (Read & Execute)
   - ✅ **Work Items** (Read)
6. Copy the generated token 🔐

## 🎯 Usage

### Basic Command

```bash
python azure_test_exporter.py --organization YOUR_ORG --project YOUR_PROJECT --pat YOUR_PAT --test-plan-id YOUR_PLAN_ID
```

### With Custom Output File

```bash
python azure_test_exporter.py --organization YOUR_ORG --project YOUR_PROJECT --pat YOUR_PAT --test-plan-id YOUR_PLAN_ID --output my_test_results.csv
```

### 📝 Example

```bash
python azure_test_exporter.py --organization globalmeddev --project GlobalMed --pat ghp_1234567890abcdef --test-plan-id 102149
```

## 📊 Output Format

The script generates a CSV file with the following columns:

| Column                   | Description                    | Example                        |
| ------------------------ | ------------------------------ | ------------------------------ |
| 🆔 **Test Plan ID**      | ID of the test plan            | `102149`                       |
| 📝 **Title**             | Test case title/name           | `Login with valid credentials` |
| 🗂️ **Suite ID**          | ID of the test suite           | `102150`                       |
| 🎯 **Test Case ID**      | Unique test case ID            | `1234`                         |
| ⚡ **Execution Status**  | Current execution state        | `Completed`, `NotExecuted`     |
| 🎭 **Execution Outcome** | Pass/Fail result               | `Passed`, `Failed`, `Blocked`  |
| 📅 **Last Run Date**     | When test was last executed    | `2024-01-15T10:30:00Z`         |
| 👤 **Last Run By**       | Who executed the test          | `John Doe`                     |
| 👥 **Assigned To**       | Who's assigned to run the test | `Jane Smith`                   |
| 🏗️ **Created Date**      | When test case was created     | `2024-01-01T09:00:00Z`         |
| 👨‍💻 **Created By**        | Who created the test case      | `Test Manager`                 |
| 🏷️ **Area Path**         | Project area path              | `MyProject\\Features\\Login`   |
| 🔄 **Iteration**         | Sprint/iteration               | `Sprint 1`                     |
| 🤖 **Automated**         | Is test automated?             | `Yes`, `No`                    |

## 📈 Sample Output

```
Test Plan ID,Title,Suite ID,Test Case ID,Execution Status,Execution Outcome,...
102149,User Login Test,102150,1234,Completed,Passed,...
102149,Password Reset,102150,1235,Completed,Failed,...
102149,User Registration,102151,1236,NotExecuted,,...
```

## 🔧 Command Line Arguments

| Argument         | Required | Description                       |
| ---------------- | -------- | --------------------------------- |
| `--organization` | ✅       | Azure DevOps organization name    |
| `--project`      | ✅       | Azure DevOps project name         |
| `--pat`          | ✅       | Personal Access Token             |
| `--test-plan-id` | ✅       | Test Plan ID to export            |
| `--output`       | ❌       | Custom output filename (optional) |

## 🎉 Example Console Output

```
Starting extraction for Test Plan ID: 102149
Test Plan: Release 1.0 Test Plan
Found 3 test suites
Fetching test execution history...
Found 15 test runs
Processing suite: Login Tests (ID: 102150)
  Found 25 test cases in suite Login Tests
Processing suite: Registration Tests (ID: 102151)
  Found 12 test cases in suite Registration Tests
Extracted 37 test cases
Test data exported to test_plan_export_20240315_143022.csv

Summary:
Total test cases: 37
Execution Outcome breakdown:
  Passed: 28
  Failed: 5
  Blocked: 2
  Not Executed: 2
Execution Status breakdown:
  Completed: 35
  NotExecuted: 2
```

## 🚨 Troubleshooting

### Common Issues

**🔐 Authentication Error**

- Double-check your PAT has the right permissions
- Ensure the PAT hasn't expired
- Verify organization and project names are correct

**📊 No Execution Results**

- Tests might not have been executed yet
- Check if you're looking at the right test plan
- Verify the test plan has test runs associated with it

**🔍 No Test Cases Found**

- Confirm the test plan ID is correct
- Check if test suites contain test cases
- Verify you have read permissions on the test plan

**🌐 Network Issues**

- Check your internet connection
- Verify Azure DevOps service is accessible
- Try increasing timeout if needed

## 🛡️ Security Notes

- 🔒 Keep your Personal Access Token secure and never commit it to version control
- 🔄 Regularly rotate your PATs
- 🎯 Use the minimum required permissions for your PAT
- 🗑️ Delete unused PATs

## 🤝 Contributing

Found a bug or want to add a feature?

1. 🍴 Fork the project
2. 🌟 Create a feature branch
3. 💻 Make your changes
4. 🧪 Test thoroughly
5. 📬 Submit a pull request

## 📞 Support

Having issues? Here are some helpful resources:

- 📚 [Azure DevOps REST API Documentation](https://docs.microsoft.com/en-us/rest/api/azure/devops/)
- 🎫 [Azure DevOps Test Management](https://docs.microsoft.com/en-us/azure/devops/test/)
- 💬 Create an issue in this repository

## 📄 License

This project is open source and available under the MIT License.

---

**Happy Testing! 🎯✨**

_Made with ❤️ for Azure DevOps users who love data-driven testing_
