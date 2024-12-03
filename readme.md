A simpletex api latex ocr client

# config guide
put the config.json at same folder of apps, set the appid and appsecret
```json
{
    "url": "https://server.simpletex.cn/api/latex_ocr_turbo",
    "appid": "xxxxxxxxxxxxxxxx",
    "appsecret": "xxxxxxxxxxxxxxx",
    "copywhich": 1
}
```
copywhich controls which latex you want copy when you press shortcut of copy , 
1 -> latex
2 -> $latex$
3 -> $$latex$$

# usage
use `control + v` to paste picture from clipboard and then ocr
use `control + c` to copy the latex

if some font error , make sure you installed the font `conslas`

# develop enviroment 

enviroment is in enviroment.yml 

create the conda enviroment by command 
```sh
conda env create -f environment.yml
```

then activate and develop 
```sh
conda activate myenv
```

# packaging/release the apps 

if qrimg is not exist , convert img to qrc resource before packaging, convert commands in terminal is  
```sh
pyrcc5 qrimg.qrd -o qrimg.py
```

```sh
pyinstaller --windowed --icon=./img/Simpletex.ico Slatexocr.py
```

or all in one file 
```sh
pyinstaller --onefile  --windowed --icon=./img/Simpletex.ico Slatexocr.py
```

# acknowledge
[img2latex](https://github.com/Joshua-li-yi/img2latex?tab=readme-ov-file)
[OCR math to latex from image annotations](https://github.com/windingwind/zotero-actions-tags/discussions/220)