# ABS-simulation

## About

User Interface for reading csv & pdf files and converting them into a dashboard.

## To-do's

☑️ Clean up requirements.txt    
☑️ Create gradio UI  
☑️ Data generation: Create fake data **THAT MAKES SENSE**.  
☑️ Individual report: Layout & summary functionality.  
☑️ Yearly report: Layout & graphing functionality.

- [ ] Connect postgress to gradio
- [ ] Perform querying with postgress
- [ ] CSV extraction: Have functions to gain data from csv or pdf or png --> 2 types of csv format they work on.
- [ ] CSV extraction: Connect to a database or a centralised csv (if preferred).
- [ ] **Define new functions for noon-report**
- [ ] Deploy to cloud (if needed).

## Installation

### Download code

```shell
git clone https://github.com/FUELNG-x-SDS/OCR.git
cd OCR
git checkout gradio
```

### Install ImageMagick
At https://imagemagick.org/script/download.php#windows

### Install GhostScript
At https://www.ghostscript.com/releases/gsdnld.html  
<img src="readme_assets/ghostscriptinstallation.png" height=50%></img>

### Install PostgreSQL for data storing and management
At https://www.postgresql.org/download/

### Install Paddle
Note: [paddlex](https://github.com/PaddlePaddle/PaddleX) only works on python 3.8 - 3.12  
You can experience the [online demo](https://aistudio.baidu.com/community/app/91661/webUI) for free.  

Install paddle paddle via pip:
```shell
# CPU
python -m pip install paddlepaddle==3.0.0rc0 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/

# GPU, this command is only suitable for machines with CUDA version 11.8
python -m pip install paddlepaddle-gpu==3.0.0rc0 -i https://www.paddlepaddle.org.cn/packages/stable/cu118/

# GPU, this command is only suitable for machines with CUDA version 12.3
python -m pip install paddlepaddle-gpu==3.0.0rc0 -i https://www.paddlepaddle.org.cn/packages/stable/cu123/
```

After installation, you can verify via
```shell
python -c "import paddle; print(paddle.__version__)"
```
With the following output of `3.0.0-rc0`  

Install paddlex with the command below:
```shell
pip install paddlex==3.0rc0
```

### Python Environment Set Up
```shell
pip install requirement.txt
python gradio_app.py
```


## Possible Incompatibility Issues

> ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
> paddlenlp 3.0.0b4 requires tokenizers<0.22,>=0.21; python_version > "3.8", but you have tokenizers 0.19.1 which is incompatible.
> gradio 5.22.0 requires aiofiles<24.0,>=22.0, but you have aiofiles 24.1.0 which is incompatible.
