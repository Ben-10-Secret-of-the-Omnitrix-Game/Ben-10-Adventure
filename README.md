# Ben-10-Adventure


## Requirements
### Python pip
```
coloredlogs==15.0
Pillow==8.1.0
pygame==2.0.1
```
### Custom Packages !

```
git clone https://github.com/Ben-10-Secret-of-the-Omnitrix-Game/hotreload.git
python3 setup.py install
```

## Running / Developing / Contributing 
This instructions for all pycharm, vscode and other IDEs'
```
cd Ben-10-Adventure
python3 -m ben_ten_adventure
```

## Combine images into single aka pack
> 1000 and 1000 is size for x and y respectively

> *You may need to increase the size depending on quantity of images*

> Script parses all directories inside!

_compiled.png - output image

manifest.json - tells where images are stored in _compiled.png. [More details](https://github.com/Ben-10-Secret-of-the-Omnitrix-Game/Ben-10-Adventure/blob/main/scripts/combine_images_into_single.py#L74-L80)
### Unix
```
cd Ben-10-Adventure
python3 scripts/combine_images_into_single.py ./resources 1000 1000
```
### Windows
```
cd .\Ben-10-Adventure
python .\scripts\combine_images_into_single.py .\ resources 1000 1000
```

