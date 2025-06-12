# 🧪 Azure DevOps Test Plan Exporter

> 🚀 Extract ALL the juicy details from your Azure DevOps test plans with hierarchical structure and execution history!

This comprehensive Python tool doesn't just export test cases - it captures the complete testing story! Get hierarchical test suite structures, detailed test steps, shared steps resolution, execution history, and so much more. Perfect for deep test analysis, reporting, and quality insights! 📊✨

## ✨ Features

- 🏗️ **Complete Test Plan Export**: Extracts test plans, suites, test cases, and individual test steps
- 📊 **Hierarchical Structure**: Maintains suite hierarchy with full path navigation (no more guessing where tests belong!)
- 🎯 **Execution History**: Includes latest test results, outcomes, and execution dates
- 🔗 **Shared Steps Resolution**: Automatically flattens shared steps into individual test cases (magic! ✨)
- 📋 **Rich Metadata**: Captures created dates, assigned testers, area paths, and automation status
- 🐛 **Debug Logging**: Comprehensive logging with optional debug mode and file output
- 💾 **CSV Export**: Clean, structured CSV output for analysis and reporting
- 📈 **Smart Analytics**: Execution breakdowns, automation stats, and step counting

## 📋 Prerequisites

Before you dive in, make sure you have:

- 🐍 **Python 3.6+** installed on your machine
- 🏢 **Azure DevOps organization** with test plans (obviously! 😄)
- 🔑 **Personal Access Token (PAT)** with the right permissions
- 📦 **Python requests library** (we'll show you how to install it)

### 🔐 Required Azure DevOps Permissions

Your Personal Access Token needs these superpowers:
- ✅ **Test Management**: Read
- ✅ **Work Items**: Read  
- ✅ **Project and Team**: Read

## 🚀 Installation

### 1️⃣ Get the Script
Clone or download this awesome script to your local machine! 📥

### 2️⃣ Install Required Packages
```bash
pip install requests
```
That's it! All other dependencies are built into Python! 🎉

### 3️⃣ Create Your Personal Access Token

1. 🌐 Go to Azure DevOps → User Settings → Personal Access Tokens
2. 🆕 Click "New Token"
3. 📛 Give it a memorable name like "Test Plan Exporter"
4. ⏰ Set appropriate expiration date
5. 🎯 Select scopes:
   - ✅ Test Management (Read)
   - ✅ Work Items (Read)
   - ✅ Project and Team (Read)
6. 📋 Copy the generated token (you won't see it again!) 🔒

## 🎯 Usage

### 🚀 Basic Usage

```bash
python azure_test_plan_exporter.py --organization "your-org" --project "your-project" --pat "your-pat-token" --test-plan-id "12345"
```

### 📁 With Custom Output File

```bash
python azure_test_plan_exporter.py --organization "your-org" --project "your-project" --pat "your-pat-token" --test-plan-id "12345" --output "my_awesome_test_export.csv"
```

### 🐛 With Debug Mode (For the Curious!)

```bash
python azure_test_plan_exporter.py --organization "your-org" --project "your-project" --pat "your-pat-token" --test-plan-id "12345" --debug
```

### 💡 Real Example

```bash
python azure_test_plan_exporter.py --organization "contoso" --project "MyAwesomeApp" --pat "ghp_1234567890abcdef" --test-plan-id "42"
```

## 🎛️ Command Line Arguments

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| 🏢 `--organization` | ✅ | Azure DevOps organization name | `"contoso"` |
| 📁 `--project` | ✅ | Azure DevOps project name | `"MyProject"` |
| 🔑 `--pat` | ✅ | Personal Access Token | `"your-secret-token"` |
| 🧪 `--test-plan-id` | ✅ | Test Plan ID to export | `"12345"` |
| 📄 `--output` | ❌ | Custom filename for CSV output | `"my_export.csv"` |
| 🐛 `--debug` | ❌ | Enable detailed debug logging | (flag only) |

### 🔍 Finding Your Information

- 🏢 **Organization**: Found in your Azure DevOps URL: `https://dev.azure.com/{organization}`
- 📁 **Project**: The project name visible in your Azure DevOps interface
- 🧪 **Test Plan ID**: Found in the test plan URL or the test plan details page

## 📊 Output Format Magic

The script generates a super-detailed hierarchical CSV file! Here's what you get:

### 📋 Column Definitions

| Column | Description | Example Values |
|--------|-------------|----------------|
| 🏷️ **Type** | Row type identifier | `Suite`, `Test Case`, `Test Step`, `Separator` |
| 🧪 **Test Plan ID** | Source test plan identifier | `12345` |
| 🗂️ **Suite Path** | Full hierarchical path | `Smoke Tests > Login > Authentication` |
| 🆔 **Suite ID** | Unique suite identifier | `67890` |
| 🎯 **Test Case ID** | Work item ID for test case | `11111` |
| 📝 **Title** | Name/title of suite or test case | `Valid User Login Test` |
| 🔢 **Step Number** | Sequential test step number | `1`, `2`, `3`... |
| ⚡ **Step Action** | What to do in this step | `Navigate to login page` |
| ✅ **Expected Result** | What should happen | `Login page displays correctly` |
| 🎭 **Execution Status** | Current execution state | `Completed`, `Not Executed` |
| 🏆 **Execution Outcome** | Test result | `Passed`, `Failed`, `Blocked` |
| 📅 **Last Run Date** | Most recent execution date | `2024-03-15T14:30:22Z` |
| 👤 **Last Run By** | Who executed the test | `Jane Doe` |
| 👥 **Assigned To** | Currently assigned tester | `John Smith` |
| 🗓️ **Created Date** | Test case creation date | `2024-01-01T09:00:00Z` |
| 👨‍💻 **Created By** | Test case creator | `Test Manager` |
| 🏷️ **Area Path** | Azure DevOps area path | `MyProject\\Features\\Auth` |
| 🔄 **Iteration** | Sprint/iteration path | `Sprint 1` |
| 🤖 **Automated** | Automation status | `Yes`, `No` |

### 📁 File Structure Example

```csv
Type,Suite Path,Title,Step Number,Step Action,Expected Result,...
Suite,Smoke Tests > Login,SUITE: Login Tests,,,,,...
Test Case,Smoke Tests > Login,Valid User Login,,,,,...
Test Step,Smoke Tests > Login,,1,Navigate to login page,Login page displays,...
Test Step,Smoke Tests > Login,,2,Enter valid credentials,User is authenticated,...
Test Step,Smoke Tests > Login,,3,Click login button,User redirected to dashboard,...
Separator,,,,,,...
```

## 📊 Logging & Output

### 📢 Standard Output
- 🚀 Progress updates for major operations
- 📈 Summary statistics upon completion  
- ❌ Error messages for failed operations
- 🎉 Celebration when everything works!

### 🐛 Debug Mode Magic
When you use the `--debug` flag, you get:
- 🔍 Detailed API request/response logging
- 👣 Step-by-step processing information
- 📄 Debug log file: `azure_exporter_debug_YYYYMMDD_HHMMSS.log`
- 🩺 Enhanced error diagnostics
- 🕵️ All the behind-the-scenes action!

## 🌟 Features in Detail

### 🏗️ Hierarchical Suite Organization
- 🔗 Builds complete suite hierarchy with parent-child relationships
- 📍 Generates human-readable suite paths like `"Regression > API > Authentication"`
- 🎯 Maintains original test plan structure in export
- 🗺️ No more getting lost in complex test structures!

### 🔗 Shared Steps Resolution (The Cool Stuff!)
- 🔍 Automatically detects shared step references in test cases
- 📥 Fetches shared step details and expands them inline
- 🎯 Supports nested shared steps (shared steps containing other shared steps!)
- 🔢 Preserves step numbering after expansion
- ✨ It's like magic, but with code!

### 📊 Execution History Integration
- 🔗 Correlates test cases with their latest execution results
- 🔍 Searches across ALL test runs in the test plan
- 📅 Provides execution outcome, date, and executor information
- 🛡️ Falls back to test point data when direct results aren't available
- 📈 Complete execution story, not just current status!

### 🛡️ Error Handling & Resilience
- 🚨 Robust API error handling with detailed logging
- 🔄 Graceful handling of missing or inaccessible test data
- ⚡ Continues processing even if individual items fail
- 📋 Comprehensive error reporting in debug mode
- 💪 Built to handle real-world messiness!

## 🎉 Example Output Summary

```
==================================================
🎯 EXPORT SUMMARY
==================================================
Total suites: 5 📊
Total test cases: 42 🧪
Total test steps: 156 📝
Total rows exported: 208 📈

🏆 Execution Outcome breakdown:
  ❌ Failed: 3 (7.1%)
  ⏸️ Not Executed: 25 (59.5%)
  ✅ Passed: 14 (33.3%)

📊 Execution Status breakdown:
  ✅ Completed: 17 (40.5%)
  ⏸️ Not Executed: 25 (59.5%)

🤖 Automation breakdown:
  📱 Manual: 38 (90.5%)
  🔧 Automated: 4 (9.5%)

📊 Average test steps per test case: 3.7
```

## 🚨 Troubleshooting

### 🔧 Common Issues & Solutions

#### 🔐 Authentication Errors
- ✅ Verify your PAT is valid and not expired
- 🔍 Ensure PAT has required permissions
- 📝 Double-check organization and project names are spelled correctly
- 🔄 Try regenerating your PAT if issues persist

#### 🕵️ Test Plan Not Found
- 🆔 Verify the test plan ID exists and is correct
- 🔐 Ensure you have read permissions to the test plan
- 📁 Check that the test plan is in the specified project
- 🌐 Confirm you're connected to the right organization

#### 📭 Empty Export Results
- 🔍 Verify the test plan contains test suites and test cases
- ✅ Check if test cases have been properly added to suites
- 🐛 Enable debug mode to see detailed processing information
- 📊 Some test plans might have test cases but no execution history

#### ⚡ Performance Issues
- ⏰ Large test plans may take several minutes to process (be patient!)
- 🐛 Enable debug mode to monitor progress
- 🔄 Consider exporting smaller test plans if timeout occurs
- 📊 Check your internet connection stability

### 🐛 Debug Information

Use the `--debug` flag to get insider information about:
- 🌐 API requests and responses
- 🔍 Test step parsing details  
- 🔗 Shared steps resolution process
- 📊 Execution history correlation
- 💾 File I/O operations
- 🕵️ Everything happening under the hood!

## ⚠️ Limitations (The Fine Print)

- 🌐 Requires internet connection to Azure DevOps (obviously!)
- ⏰ Processing time increases with test plan size (bigger = slower)
- 📊 Some advanced test case fields may not be included
- 🖼️ Attachments and images in test steps are not exported
- 🎛️ Test case parameters are not currently extracted
- 💡 But hey, we're constantly improving!

## 🤝 Contributing

Want to make this tool even more awesome? 

1. 🍴 Fork the project
2. 🌟 Create a feature branch (`git checkout -b feature/amazing-feature`)
3. 💻 Make your changes
4. 🧪 Test thoroughly (we love tests!)
5. 📬 Submit a pull request
6. 🎉 Celebrate your contribution!

### 💡 Ideas for Contributions
- 📊 Additional export formats (JSON, Excel, etc.)
- 🎨 Better CSV formatting options
- 🔍 More detailed test step analysis
- 🚀 Performance optimizations
- 🌐 Support for other Azure DevOps features

## 📞 Need Help?

Having trouble? We've got your back! 💪

- 📚 [Azure DevOps REST API Documentation](https://docs.microsoft.com/en-us/rest/api/azure/devops/)
- 🧪 [Azure DevOps Test Management Docs](https://docs.microsoft.com/en-us/azure/devops/test/)
- 🐛 Create an issue in this repository
- 💬 Join our community discussions
- 📧 Reach out to the maintainers

## 🎖️ License

This project is open source and available under the MIT License. Use it, modify it, share it - spread the testing love! ❤️

---

## 🎊 Final Words

**Happy Testing, Data Warriors! 🧪📊✨**

_Made with ❤️, ☕, and countless hours of debugging for Azure DevOps users who believe that great testing deserves great tools!_

**Remember**: Great test data leads to great products. You're not just exporting data - you're enabling better software! 🚀

---

*P.S. - If this tool saves you time, consider giving it a ⭐ star on GitHub! It makes our day! 😊*
