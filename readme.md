# A simpletex api latex ocr client
without implement any screenshot method, just get pics from clipboard, you can use any software to save screenshot to clipboard then do ocr
# config guide
put the config.json at same folder of executable, set the appid and appsecret
```json
{
    "url": "https://server.simpletex.cn/api/latex_ocr_turbo",
    "appid": "xxxxxxxxxxxxxxxx",
    "appsecret": "xxxxxxxxxxxxxxx",
    "copywhich": 1
}
```
copywhich controls which latex you want copy when you press shortcut of copy , 
```
1 -> latex
2 -> $latex$
3 -> $$latex$$
```

# usage
use `control + v` to paste picture from clipboard and then ocr
use `control + c` to copy the latex

if some font error , make sure you installed the font `conslas`

# develop enviroment     

use conda enviroment config `enviroment.yml` to create a conda vritual enviroment 
```sh
conda env create -f environment.yml
```

# packaging/release

if qrimg is not exist , convert img to qrc resource before packaging by command
```sh
pyrcc5 qrimg.qrc -o qrimg.py
```
generate executable file
```sh
pyinstaller --onefile  --windowed --icon=./img/Simpletex.ico Slatexocr.py
```

# acknowledge
[img2latex](https://github.com/Joshua-li-yi/img2latex?tab=readme-ov-file)

[OCR math to latex from image annotations](https://github.com/windingwind/zotero-actions-tags/discussions/220)
