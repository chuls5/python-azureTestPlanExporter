# 🧪 Azure DevOps Test Plan Exporter

> 🚀 Extract ALL the juicy details from your Azure DevOps test plans with hierarchical structure and execution history!

This comprehensive Python tool doesn't just export test cases - it captures the complete testing story! Get hierarchical test suite structures, detailed test steps, shared steps resolution, execution history, and so much more. Perfect for deep test analysis, reporting, and quality insights! 📊✨

## 🚀 Quick Start

### 📋 What You Need

- 🐍 **Python 3.6+** installed on your machine
- 🏢 **Azure DevOps organization** with test plans
- 🔑 **Personal Access Token (PAT)** with Test Management and Work Items read permissions
- 💻 **Git** (to download the tool)

---

If you already have Python installed, skip to Step:4

Otherwise, please follow along to install Python globally on your machine. 

---

This section will guide users who do not have Python or VS Code installed.

## 🛠️ Installing Python and Visual Studio Code

### 📥 Step 1: Install Python

1. **Download Python**:
   - Go to the [official Python website](https://www.python.org/downloads/).
   - Click on the "Download Python" button (the latest version is recommended).

2. **Run the Installer**:
   - Open the downloaded installer.
   - **Important**: Check the box that says "Add Python to PATH".
   - Click "Install Now" and follow the prompts.

3. **Verify Installation**:
   - Open Command Prompt (Windows) or Terminal (Mac/Linux).
   - Type the following command and press Enter:
     ```bash
     python --version
     ```
   - You should see the installed Python version.

### 💻 Step 2: Install Visual Studio Code

1. **Download VS Code**:
   - Go to the [Visual Studio Code website](https://code.visualstudio.com/).
   - Click on the "Download" button for your operating system.

2. **Run the Installer**:
   - Open the downloaded installer.
   - Follow the installation prompts.

3. **Install Python Extension**:
   - Open VS Code.
   - Go to the Extensions view by clicking on the Extensions icon in the Activity Bar on the left side of the window.
   - Search for "Python" and install the official Python extension by Microsoft.

### 🔍 Step 3: Verify VS Code Setup

1. **Open a New Terminal in VS Code**:
   - Go to the menu and select `Terminal` > `New Terminal`.

2. **Check Python Installation in VS Code terminal**:
   - In the terminal, type:
     ```bash
     python --version
     ```
   - Ensure it shows the correct Python version.


If you are having trouble, make sure you installed the official Microsoft Python VScode extension in Step: 2.3

---

### 📥 Step 4: Set Up Your Projects Folder

1. **Create a Folder on Your Desktop**:
   - Right-click on your desktop and select `New` > `Folder`.
   - Name the folder **"projects"**.

2. **Open Visual Studio Code**:
   - Launch VS Code from your applications or start menu.

3. **Open the Projects Folder in VS Code**:
   - In VS Code, go to the menu and select `File` > `Open Folder...`.
   - Navigate to your desktop and select the **"projects"** folder you just created.

4. **Verify the Folder is Open**:
   - Ensure that the **"projects"** folder is displayed in the Explorer pane on the left side of VS Code.

---

### 📥 Step 5: Get the Tool

**Option A: Download with Git (Recommended)**
1. **Open a New Terminal in VS Code**:
   - Go to the menu and select `Terminal` > `New Terminal`.
```bash
# Clone the repository to your computer
git clone https://github.com/chuls5/python-azureTestPlanExporter.git

# Go into the folder
cd python-azureTestPlanExporter
```

---

**Option B: Manual Download**

1. 🌐 **Go to the GitHub Repository Page**:
   - Open your web browser and navigate to the [Azure DevOps Test Plan Exporter GitHub repository](https://github.com/chuls5/python-azureTestPlanExporter).

2. 💚 **Click the Green "Code" Button**:
   - On the repository page, locate the green button labeled **"Code"** and click on it.

3. 📦 **Download the ZIP File**:
   - In the dropdown menu, click on **"Download ZIP"**. This will download a compressed file containing the project files to your computer.

4. 📁 **Extract the ZIP File**:
   - Navigate to your **Downloads** folder (or wherever the ZIP file was saved).
   - Right-click on the downloaded ZIP file and select **"Extract All..."** (or use your preferred extraction tool).
   - Choose a destination folder (you can extract it to the **"projects"** folder you created earlier) and click **"Extract"**.

5. 💻 **Open Command Prompt/Terminal**:
   - Open Command Prompt (Windows) or Terminal (Mac/Linux).

6. **Navigate to the Extracted Folder**:
   - Use the `cd` command to change to the directory where you extracted the files. For example:
   ```bash
   cd path/to/your/extracted/folder
   ```
   - Make sure to replace `path/to/your/extracted/folder` with the actual path to the folder where you extracted the ZIP file.

7. **Verify the Files**:
   - Once in the folder, you can list the files to ensure everything is extracted correctly by running:
   ```bash
   ls  # For Mac/Linux
   dir # For Windows
   ```

---

### 📦 Step 6: Install Dependencies

Use the Python installer "pip", also known as, "python install package" to install the required packages for the project.

Since this Python script is interacting with Microsoft Azure API, install the following package:

```bash
# Install the required Python package
pip install requests
```

The **requests** package in Python is a popular and widely used library for making HTTP requests. It provides a simple and elegant API for interacting with web services, APIs, and web pages.

**💡 Beginner Tip**: If you get a "pip not found" error, you might need to use `python -m pip install requests` instead.

### 🔑 Step 6: Get Your Personal Access Token (PAT)

**Don't skip this step! You need this token to connect to Azure DevOps.**

1. 🌐 Go to your Azure DevOps in your web browser
2. 👤 Click your profile picture in the top right corner
3. ⚙️ Click "Personal access tokens"
4. 🆕 Click "New Token"
5. 📝 Fill out the form:
   - **Name**: `Test Plan Exporter` (or any name you like)
   - **Expiration**: Choose how long it should work (90 days is fine for testing)
   - **Scopes**: Click "Custom defined" and check these boxes:
     - ✅ **Test Management** → **Read**
     - ✅ **Work Items** → **Read**
6. 🔵 Click "Create"
7. 📋 **IMPORTANT**: Copy the token that appears (you won't see it again!)

### 🎯 Step 7: Run the Tool

**Basic command structure:**
```bash
python azureTestPlanExporter.py --organization "your-org" --project "your-project" --pat "your-token" --test-plan-id "12345"
```

**Real example (replace with your actual values):**
```bash
python azureTestPlanExporter.py --organization "contoso" --project "MyAwesomeApp" --pat "abcd1234efgh5678ijkl" --test-plan-id "42"
```

**🔍 Where to find your information:**
- **Organization**: In your Azure DevOps URL → `https://dev.azure.com/ORGANIZATION-NAME`
- **Project**: The project name you see in Azure DevOps
- **Test Plan ID**: Open your test plan in Azure DevOps, look at the URL → `.../_testManagement/execute?planId=TEST-PLAN-ID...`

### 🎉 Step 8: Check Your Results!

After running the command, you'll see:
- ✅ Progress messages as it works
- 📊 A summary of what it exported
- 📁 A new CSV file in the same folder (like `test_plan_12345_export.csv`)

**Open the CSV file in Excel or Google Sheets to see your test data!**

## 🆘 Complete Beginner Example

**Let's say you have:**
- Organization: `mycompany`
- Project: `WebApp`
- Test Plan ID: `100`
- PAT: `abc123def456ghi789`

**Step-by-step:**

1. **Open Command Prompt (Windows) or Terminal (Mac/Linux)**
2. **Navigate to your downloaded folder:**
   ```bash
   cd Downloads/azure-devops-test-plan-exporter
   ```
3. **Run the command:**
   ```bash
   python azureTestPlanExporter.py --organization "mycompany" --project "WebApp" --pat "abc123def456ghi789" --test-plan-id "100"
   ```
4. **Wait for it to finish** (you'll see progress messages)
5. **Find your CSV file** in the same folder!

## 🔧 Troubleshooting for Beginners

**❌ "python is not recognized" or "command not found"**
- Solution: Install Python from python.org and make sure to check "Add Python to PATH"

**❌ "No module named 'requests'"**
- Solution: Run `pip install requests` (or `python -m pip install requests`)

**❌ "Authentication failed"**
- Solution: Double-check your PAT token and make sure it has the right permissions

**❌ "Test plan not found"**
- Solution: Verify the test plan ID is correct and you have access to it

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

### 📁 More Usage Examples

**Save to a custom filename:**
```bash
python azureTestPlanExporter.py --organization "your-org" --project "your-project" --pat "your-pat-token" --test-plan-id "12345" --output "my_test_results.csv"
```

**Get detailed debug information:**
```bash
python azureTestPlanExporter.py --organization "your-org" --project "your-project" --pat "your-pat-token" --test-plan-id "12345" --debug
```

## ✨ Features

- 🏗️ **Complete Test Plan Export**: Extracts test plans, suites, test cases, and individual test steps
- 📊 **Hierarchical Structure**: Maintains suite hierarchy with full path navigation (no more guessing where tests belong!)
- 🎯 **Execution History**: Includes latest test results, outcomes, and execution dates
- 🔗 **Shared Steps Resolution**: Automatically flattens shared steps into individual test cases (magic! ✨)
- 📋 **Rich Metadata**: Captures created dates, assigned testers, area paths, and automation status
- 🐛 **Debug Logging**: Comprehensive logging with optional debug mode and file output
- 💾 **CSV Export**: Clean, structured CSV output for analysis and reporting
- 📈 **Smart Analytics**: Execution breakdowns, automation stats, and step counting

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

The file structure is initially going to look like a lot.

Those of us who know Excel will have no problem "wrapping text" from the 'Step Action' and 'Expected Result' columns.

```csv
Type,Suite Path,Title,Step Number,Step Action,Expected Result,...
Suite,Smoke Tests > Login,SUITE: Login Tests,,,,,...
Test Case,Smoke Tests > Login,Valid User Login,,,,,...
Test Step,Smoke Tests > Login,,1,Navigate to login page,Login page displays,...
Test Step,Smoke Tests > Login,,2,Enter valid credentials,User is authenticated,...
Test Step,Smoke Tests > Login,,3,Click login button,User redirected to dashboard,...
Separator,,,,,,...
```

## 🔐 Setting Up Your Personal Access Token (Detailed Guide)

### 🤔 What is a Personal Access Token?
Think of it as a special password that lets this tool talk to your Azure DevOps account safely. It's like giving the tool a visitor badge to your building.

### 📝 Step-by-Step PAT Creation

1. **🌐 Open Azure DevOps** in your web browser
2. **👤 Click your profile picture** (top right corner)
3. **⚙️ Click "Personal access tokens"**
4. **🆕 Click "New Token"** (blue button)
5. **📝 Fill out the form:**
   - **Name**: Type something like `Test Plan Exporter Tool`
   - **Organization**: Select your organization (or leave as "All accessible organizations")
   - **Expiration**: Pick a date (30-90 days is good for testing)
   - **Scopes**: Click "Custom defined" and find these sections:
     - 📊 **Test Management** - check the "Read" box
     - 🎯 **Work Items** - check the "Read" box
     - 👥 **Project and Team** - check the "Read" box
6. **🔵 Click "Create"**
7. **📋 COPY THE TOKEN!** It will show a long string of letters and numbers - copy this somewhere safe (like Notepad). You won't be able to see it again!

### ⚠️ Important Notes About Your Token
- 🔒 **Keep it secret** - don't share it with others or post it online
- ⏰ **It expires** - you'll need to create a new one when it expires
- 🗑️ **You can delete it** anytime by going back to Personal Access Tokens and clicking "Revoke"

## 🎉 Example Output Summary

```
==================================================
🎯 EXPORT SUMMARY
==================================================
Total suites: 5 
Total test cases: 42 
Total test steps: 156 
Total rows exported: 208 

Execution Outcome breakdown:
  Failed: 3 (7.1%)
  Not Executed: 25 (59.5%)
  Passed: 14 (33.3%)

Execution Status breakdown:
  Completed: 17 (40.5%)
  Not Executed: 25 (59.5%)

Automation breakdown:
  Manual: 38 (90.5%)
  Automated: 4 (9.5%)

Average test steps per test case: 3.7
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

## 🚨 Troubleshooting

### 🔧 Common Issues & Solutions

#### 🔐 Authentication Errors
- ✅ Verify your PAT is valid and not expired
- 🔍 Ensure PAT has required permissions
- 📝 Double-check organization and project names are spelled correctly
- 🔄 Try regenerating your PAT if issues persist, or granting "Full Access"

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
- 📧 Send me a message on LinkedIn! 

---

## 🎊 Final Words

**Happy Testing, Data Warriors! 🧪📊✨**

_Made with ❤️, ☕, and countless hours of debugging for Azure DevOps users who believe that great testing deserves great tools!_

**Remember**: Great test data leads to great products. You're not just exporting data - you're enabling better software! 🚀

---

*P.S. - If this tool saves you time, consider giving it a ⭐ star on GitHub! It makes our day! 😊*
