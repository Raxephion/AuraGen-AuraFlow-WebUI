@echo off
title AuraGen AuraFlow Web-UI app

echo Checking for existing virtual environment (venv)...
IF EXIST "venv\Scripts\activate.bat" GOTO VENV_EXISTS
GOTO CREATE_VENV

:VENV_EXISTS
echo Virtual environment (venv) already exists. Skipping creation.
GOTO ACTIVATE_VENV

:CREATE_VENV
echo Creating Python virtual environment (venv)...
python -m venv venv
IF ERRORLEVEL 1 (
    echo Failed to create virtual environment. Please ensure Python is installed and in PATH.
    pause
    GOTO :EOF
)

:ACTIVATE_VENV
echo Activating virtual environment...
call "venv\Scripts\activate.bat"
IF ERRORLEVEL 1 (
    echo Failed to activate virtual environment.
    pause
    GOTO :EOF
)

echo Upgrading pip...
python -m pip install --upgrade pip
IF ERRORLEVEL 1 (
    echo Failed to upgrade pip.
    pause
    GOTO :EOF
)

echo.
echo Checking for existing PyTorch with CUDA support...
python -c "import torch; import sys; sys.exit(0) if torch.cuda.is_available() else sys.exit(1)"
IF ERRORLEVEL 1 GOTO INSTALL_PYTORCH
GOTO PYTORCH_EXISTS

:INSTALL_PYTORCH
echo Attempting to install PyTorch with CUDA 12.1 support...
echo This is a common version for many modern NVIDIA GPUs like the RTX 3060.
echo If this fails, or if you have a different GPU/CUDA setup (e.g., older CUDA, AMD, or CPU only),
echo you may need to install PyTorch manually first by following instructions at:
echo https://pytorch.org/get-started/locally/
echo After manual PyTorch installation, you can re-run this script.
echo.
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
IF ERRORLEVEL 1 (
    echo Failed to install PyTorch with CUDA 12.1. 
    pause
    GOTO :EOF
)
echo PyTorch (CUDA 12.1) installation attempted.
GOTO INSTALL_DEPS

:PYTORCH_EXISTS
echo PyTorch with CUDA support already detected. Skipping PyTorch installation.

:INSTALL_DEPS
echo.
echo Installing other dependencies from requirements.txt...
pip install --upgrade -r requirements.txt
IF ERRORLEVEL 1 (
    echo Failed to install other dependencies. Please check requirements.txt and your internet connection.
    pause
    GOTO :EOF
)

echo.
echo Installation complete.
pause
GOTO :EOF

:EOF
echo Script finished or exited due to an error.
