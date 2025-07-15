"""
Test suite for project structure validation.
Tests that all required directories and files exist as per the architecture.
"""
import os
import pytest
from pathlib import Path


class TestProjectStructure:
    """Test project directory structure and essential files."""
    
    @pytest.fixture
    def project_root(self):
        """Get the project root directory."""
        return Path(__file__).parent.parent
    
    def test_main_directories_exist(self, project_root):
        """Test that all main directories exist."""
        required_dirs = [
            "src",
            "alembic", 
            "tests",
            "docs",
            "tasks"
        ]
        
        for dir_name in required_dirs:
            dir_path = project_root / dir_name
            assert dir_path.exists(), f"Directory {dir_name} should exist"
            assert dir_path.is_dir(), f"{dir_name} should be a directory"
    
    def test_src_subdirectories_exist(self, project_root):
        """Test that all src subdirectories exist."""
        src_subdirs = [
            "api",
            "api/endpoints",
            "core", 
            "models",
            "schemas",
            "crud",
            "worker"
        ]
        
        src_path = project_root / "src"
        for subdir in src_subdirs:
            subdir_path = src_path / subdir
            assert subdir_path.exists(), (
                f"Src subdirectory {subdir} should exist"
            )
            assert subdir_path.is_dir(), (
                f"Src subdirectory {subdir} should be a directory"
            )
    
    def test_python_init_files_exist(self, project_root):
        """Test that all __init__.py files exist in Python packages."""
        init_files = [
            "src/__init__.py",
            "src/api/__init__.py",
            "src/api/endpoints/__init__.py",
            "src/core/__init__.py",
            "src/models/__init__.py", 
            "src/schemas/__init__.py",
            "src/crud/__init__.py",
            "src/worker/__init__.py"
        ]
        
        for init_file in init_files:
            init_path = project_root / init_file
            assert init_path.exists(), f"Init file {init_file} should exist"
            assert init_path.is_file(), f"{init_file} should be a file"
    
    def test_config_files_exist(self, project_root):
        """Test that configuration files exist."""
        config_files = [
            ".env",
            "requirements.txt", 
            "run_worker.sh"
        ]
        
        for config_file in config_files:
            config_path = project_root / config_file
            assert config_path.exists(), (
                f"Config file {config_file} should exist"
            )
            assert config_path.is_file(), f"{config_file} should be a file"
    
    def test_worker_script_is_executable(self, project_root):
        """Test that the worker script has execute permissions."""
        script_path = project_root / "run_worker.sh"
        assert os.access(script_path, os.X_OK), (
            "run_worker.sh should be executable"
        )
    
    def test_requirements_file_content(self, project_root):
        """Test that requirements.txt contains expected dependencies."""
        requirements_path = project_root / "requirements.txt"
        content = requirements_path.read_text()
        
        # Production dependencies
        production_packages = [
            "fastapi",
            "uvicorn", 
            "sqlalchemy",
            "asyncmy",
            "alembic",
            "arq",
            "redis",
            "pydantic",
            "pydantic-settings"
        ]
        
        # Development dependencies
        development_packages = [
            "pytest",
            "pytest-asyncio",
            "pytest-cov",
            "httpx",
            "black",
            "isort", 
            "flake8",
            "mypy",
            "python-dotenv",
            "pre-commit"
        ]
        
        all_packages = production_packages + development_packages
        
        for package in all_packages:
            assert package in content, (
                f"Package {package} should be in requirements.txt"
            )
        
        # Test that content is well organized
        assert "生产环境依赖" in content, (
            "Should have production dependencies section"
        )
        assert "开发环境依赖" in content, (
            "Should have development dependencies section"
        ) 