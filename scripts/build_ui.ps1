Set-Location ./ui

$dest_folder = "../src/main/python/etr/qt_interface/auto_generated/"

$files = Get-ChildItem -File -Filter "*.ui"

foreach($file in $files){
    pyuic5 $file.Name -o ($dest_folder + $file.BaseName + "_auto.py")
}

Set-Location ..
