@echo off

echo Creating Python environment...
call "C:\Users\%USERNAME%\miniconda3\Scripts\conda" create -n story_creator python=3.10 -y
pause

echo Activating environment...
call "C:\Users\%USERNAME%\miniconda3\Scripts\activate.bat" story_creator
pause

echo Installing requirements...
python -m pip install --upgrade pip
pip install -r "C:\story_creator\requirements.txt" -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
pip install -U "qwen-agent[rag,code_interpreter,python_executor,gui]==0.0.7"
pause

echo Checking installed packages...
conda list


echo Installation complete!
pause
