$ErrorActionPreference = 'Stop'
$reviewWord = New-Object -ComObject Word.Application
$reviewWord.Visible = $false
$reviewWord.DisplayAlerts = 0
try {
  $reviewDoc = $reviewWord.Documents.Open('E:\Projects\DBMS OOPS\review\FoodBridge_Project_Review.docx', $false, $true)
  $reviewDoc.Repaginate()
  $reviewDoc.ExportAsFixedFormat('E:\Projects\DBMS OOPS\review\.build\FoodBridge_Project_Review.pdf', 17)
  $reviewDoc.Close(0)
} finally { $reviewWord.Quit() }
