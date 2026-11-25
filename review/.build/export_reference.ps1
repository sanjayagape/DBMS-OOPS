$ErrorActionPreference = 'Stop'
$wordApp = New-Object -ComObject Word.Application
$wordApp.Visible = $false
$wordApp.DisplayAlerts = 0
try {
  $refDoc = $wordApp.Documents.Open('C:\Users\HOME\Downloads\EMPLOYEE DETAILS AND PAYROLL MANAGEMENT SYSTEM (2)-3 (1).docx', $false, $true)
  $refDoc.ExportAsFixedFormat('E:\Projects\DBMS OOPS\review\.build\reference.pdf', 17)
  $refDoc.Close(0)
} finally { $wordApp.Quit() }
