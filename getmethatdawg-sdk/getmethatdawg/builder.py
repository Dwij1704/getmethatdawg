#!/usr/bin/env python3
"""
GetMeThatDawg Builder - Generates Flask app and deployment files from Python source
"""

import os
import sys
import ast
import importlib.util
import tempfile
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional, NamedTuple
from dataclasses import dataclass
import json

from . import get_endpoints, Endpoint


@dataclass
class AutoDetectedEndpoint:
    """Represents an auto-detected endpoint"""
    func_name: str
    path: str
    method: str
    params: List[str]
    return_type: str
    docstring: str

class GetMeThatDawgBuilder:
    """Builder that processes Python files and generates deployment artifacts"""
    
    def __init__(self, source_file: str, output_dir: str = "/tmp/out", original_name: str = None, auto_detect: bool = False):
        self.source_file = Path(source_file)
        self.output_dir = Path(output_dir)
        self.original_name = original_name or self.source_file.stem
        self.auto_detect = auto_detect
        self.endpoints: List[Endpoint] = []
        self.auto_detected_endpoints: List[AutoDetectedEndpoint] = []
        
        # Check if WANDB/weave observability is enabled
        self.wandb_enabled = self._is_wandb_enabled()
        if self.wandb_enabled:
            print("🐝 WANDB observability enabled - functions will be automatically tracked with weave")
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _is_wandb_enabled(self) -> bool:
        """Check if WANDB observability is enabled via environment variables"""
        # Check for WANDB_API_KEY in .env file or environment
        env_vars = self._read_env_file()
        return bool(env_vars.get('WANDB_API_KEY') or os.getenv('WANDB_API_KEY'))

    def auto_detect_endpoints(self):
        """Auto-detect functions that should be exposed as web endpoints"""
        print("🔍 Auto-detecting endpoints...")
        
        # Parse the AST to find function definitions
        with open(self.source_file, 'r') as f:
            source_code = f.read()
        
        try:
            tree = ast.parse(source_code)
        except SyntaxError as e:
            print(f"❌ Syntax error in {self.source_file}: {e}")
            return
        
        # Find all function definitions
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                endpoint = self._analyze_function_for_endpoint(node, source_code)
                if endpoint:
                    self.auto_detected_endpoints.append(endpoint)
                    print(f"✅ Auto-detected: {endpoint.method} {endpoint.path} -> {endpoint.func_name}")
        
        print(f"🎯 Found {len(self.auto_detected_endpoints)} potential endpoints")
    
    def _analyze_function_for_endpoint(self, node: ast.FunctionDef, source_code: str) -> Optional[AutoDetectedEndpoint]:
        """Analyze a function to determine if it should be an endpoint"""
        func_name = node.name
        
        # Skip private functions
        if func_name.startswith('_'):
            return None
        
        # Skip some common non-endpoint functions
        skip_patterns = [
            'main', 'setup', 'init', 'test_', 'validate', 'parse', 'format',
            'print', 'log', 'debug', 'error', 'warn'
        ]
        
        if any(pattern in func_name.lower() for pattern in skip_patterns):
            return None
        
        # Get function signature
        args = []
        for arg in node.args.args:
            if arg.arg != 'self':  # Skip self parameter
                args.append(arg.arg)
        
        # Get return type from annotation if available
        return_type = "Any"
        if node.returns:
            if isinstance(node.returns, ast.Name):
                return_type = node.returns.id
            elif isinstance(node.returns, ast.Subscript):
                if isinstance(node.returns.value, ast.Name):
                    return_type = node.returns.value.id
        
        # Get docstring
        docstring = ""
        if (node.body and isinstance(node.body[0], ast.Expr) and 
            isinstance(node.body[0].value, ast.Constant) and 
            isinstance(node.body[0].value.value, str)):
            docstring = node.body[0].value.value
        
        # Determine HTTP method and path based on function characteristics
        method, path = self._determine_http_method_and_path(func_name, args, return_type, docstring)
        
        # Only include functions that look like web endpoints
        if method and path:
            return AutoDetectedEndpoint(
                func_name=func_name,
                path=path,
                method=method,
                params=args,
                return_type=return_type,
                docstring=docstring
            )
        
        return None
    
    def _determine_http_method_and_path(self, func_name: str, args: List[str], return_type: str, docstring: str) -> tuple[str, str]:
        """Determine HTTP method and path for a function"""
        func_lower = func_name.lower()
        
        # Functions that return data without side effects -> GET
        if (len(args) <= 1 and 
            (func_lower.startswith(('get', 'list', 'show', 'find', 'search', 'select', 'load')) or
             'get' in func_lower or 'search' in func_lower or 'select' in func_lower)):
            path = f"/{func_name.lower().replace('_', '-')}"
            return "GET", path
        
        # Functions that modify state or take multiple parameters -> POST
        if (len(args) > 1 or 
            func_lower.startswith(('create', 'add', 'save', 'update', 'delete', 'generate', 'process', 'handle', 'execute')) or
            'save' in func_lower or 'generate' in func_lower or 'process' in func_lower):
            path = f"/{func_name.lower().replace('_', '-')}"
            return "POST", path
        
        # Functions that return structured data (Dict, List) -> likely endpoints
        if return_type in ['Dict', 'List', 'dict', 'list'] or 'Dict' in return_type:
            # Choose method based on parameter count
            method = "GET" if len(args) <= 1 else "POST"
            path = f"/{func_name.lower().replace('_', '-')}"
            return method, path
        
        # Functions with meaningful names that take parameters
        if len(args) > 0 and len(func_name) > 3:
            method = "GET" if len(args) == 1 else "POST"
            path = f"/{func_name.lower().replace('_', '-')}"
            return method, path
        
        return None, None
    
    def _read_env_file(self) -> Dict[str, str]:
        """Read environment variables from .env file"""
        env_vars = {}
        
        # Look for .env file in source file directory and parent directories
        search_paths = [
            Path('/tmp/.env'),  # Mounted .env file in Docker container
            self.source_file.parent / '.env',
            Path('.env'),  # Current working directory
            Path.cwd() / '.env',  # Explicit current working directory
        ]
        
        for env_path in search_paths:
            if env_path.exists():
                try:
                    with open(env_path, 'r') as f:
                        for line in f:
                            line = line.strip()
                            # Skip comments and empty lines
                            if line and not line.startswith('#'):
                                # Handle KEY=VALUE format
                                if '=' in line:
                                    key, value = line.split('=', 1)
                                    key = key.strip()
                                    value = value.strip().strip('"').strip("'")  # Remove quotes
                                    if key and value:
                                        env_vars[key] = value
                    print(f"✅ Loaded {len(env_vars)} environment variables from {env_path}")
                    break
                except Exception as e:
                    print(f"⚠️  Failed to read {env_path}: {e}")
                    continue
        
        if not env_vars:
            print("ℹ No .env file found - deploying without custom environment variables")
        
        return env_vars

    def _categorize_env_vars(self, env_vars: Dict[str, str]) -> tuple[Dict[str, str], Dict[str, str]]:
        """Categorize environment variables into secrets and regular env vars"""
        secrets = {}
        regular_env = {}
        
        # Patterns that indicate sensitive data (should be secrets)
        secret_patterns = [
            'API_KEY', 'TOKEN', 'SECRET', 'PASSWORD', 'PRIVATE_KEY', 'CREDENTIAL',
            'CLIENT_SECRET', 'AUTH_KEY', 'ACCESS_TOKEN', 'REFRESH_TOKEN'
        ]
        
        for key, value in env_vars.items():
            key_upper = key.upper()
            is_secret = any(pattern in key_upper for pattern in secret_patterns)
            
            if is_secret:
                secrets[key] = value
            else:
                regular_env[key] = value
        
        return secrets, regular_env

    def generate_secrets_file(self, env_vars: Dict[str, str]) -> Optional[Path]:
        """Generate a secrets file for flyctl to use"""
        secrets, _ = self._categorize_env_vars(env_vars)
        
        if not secrets:
            return None
        
        secrets_file = self.output_dir / "secrets.json"
        secrets_data = {
            "secrets": secrets,
            "instructions": "Run 'flyctl secrets set' for each secret listed above"
        }
        
        with open(secrets_file, 'w') as f:
            json.dump(secrets_data, f, indent=2)
        
        print(f"✅ Generated secrets file with {len(secrets)} secrets")
        return secrets_file

    def generate_deployment_script(self, env_vars: Dict[str, str]) -> Path:
        """Generate a deployment script that sets secrets automatically"""
        secrets, _ = self._categorize_env_vars(env_vars)
        
        script_content = """#!/bin/bash
# Auto-generated deployment script for setting secrets
set -euo pipefail

echo "🔐 Setting up secrets for deployment..."

"""
        
        for key, value in secrets.items():
            # Escape single quotes in the value
            escaped_value = value.replace("'", "'\"'\"'")
            script_content += f"flyctl secrets set {key}='{escaped_value}' --stage\n"
        
        if secrets:
            script_content += """
echo "✅ All secrets staged. Deploying with secrets..."
flyctl deploy --remote-only
"""
        else:
            script_content += """
echo "ℹ No secrets to set. Proceeding with normal deployment..."
flyctl deploy --remote-only
"""
        
        script_path = self.output_dir / "deploy-with-secrets.sh"
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # Make script executable
        import stat
        script_path.chmod(script_path.stat().st_mode | stat.S_IEXEC)
        
        print(f"✅ Generated deployment script: {script_path}")
        return script_path
    
    def analyze_source(self):
        """Analyze the Python source file to extract endpoints"""
        if self.auto_detect:
            self.auto_detect_endpoints()
            # Convert auto-detected endpoints to regular endpoints
            for auto_endpoint in self.auto_detected_endpoints:
                # Create a mock function for the endpoint
                def mock_func():
                    pass
                mock_func.__name__ = auto_endpoint.func_name
                
                endpoint = Endpoint(
                    func=mock_func,
                    path=auto_endpoint.path,
                    method=auto_endpoint.method
                )
                self.endpoints.append(endpoint)
        else:
            # Import the module to trigger endpoint registration
            spec = importlib.util.spec_from_file_location("user_module", self.source_file)
            if spec is None or spec.loader is None:
                raise RuntimeError(f"Could not load module from {self.source_file}")
            
            module = importlib.util.module_from_spec(spec)
            
            # Execute the module to register endpoints
            spec.loader.exec_module(module)
            
            # Get registered endpoints
            self.endpoints = get_endpoints()
            
            if not self.endpoints:
                raise RuntimeError("No endpoints found! Make sure to use @getmethatdawg.expose decorator or enable auto-detection with --auto-detect.")
        
        print(f"✓ Detected {len(self.endpoints)} endpoint(s)")
    
    def generate_flask_app(self):
        """Generate the Flask application file"""
        weave_init = ""
        if self.wandb_enabled:
            weave_init = """
# 🐝 Initialize weave for observability (getmethatdawg auto-generated)
try:
    import weave
    weave.init('getmethatdawg')
    print("🐝 Weave observability initialized for project 'getmethatdawg'")
except ImportError:
    print("⚠️ Weave not available - install with: pip install weave")
except Exception as e:
    print(f"⚠️ Failed to initialize weave: {e}")
"""
        
        template = '''#!/usr/bin/env python3
"""
Generated Flask app by getmethatdawg builder
"""

import os
import sys
import inspect
from flask import Flask, request, jsonify
from pathlib import Path

# Add the source directory to Python path
sys.path.insert(0, '/app')

# Import the user's module
import user_module
''' + weave_init + '''
app = Flask(__name__)

def extract_args_from_request(func, method):
    """Extract function arguments from HTTP request"""
    sig = inspect.signature(func)
    args = {}
    
    for param_name, param in sig.parameters.items():
        if method == 'GET':
            # Get from query parameters
            value = request.args.get(param_name)
        else:
            # Get from JSON body or form data
            if request.is_json:
                value = request.json.get(param_name) if request.json else None
            else:
                value = request.form.get(param_name)
        
        # Use default value if not provided
        if value is None and param.default != inspect.Parameter.empty:
            value = param.default
        elif value is None:
            # Required parameter is missing
            return None, f"Missing required parameter: {param_name}"
        
        # Basic type conversion
        if param.annotation != inspect.Parameter.empty:
            try:
                if param.annotation == int:
                    value = int(value)
                elif param.annotation == float:
                    value = float(value)
                elif param.annotation == bool:
                    value = value.lower() in ('true', '1', 'yes', 'on')
            except (ValueError, TypeError):
                return None, f"Invalid type for parameter {param_name}: expected {param.annotation.__name__}"
        
        args[param_name] = value
    
    return args, None

'''

        # Generate routes for each endpoint
        for endpoint in self.endpoints:
            route_code = f'''
@app.route('{endpoint.path}', methods=['{endpoint.method}'])
def {endpoint.func_name}_route():
    """Route for {endpoint.func_name}"""
    try:
        args, error = extract_args_from_request(user_module.{endpoint.func_name}, '{endpoint.method}')
        if error:
            return jsonify({{"error": error}}), 400
        
        result = user_module.{endpoint.func_name}(**args)
        
        # Ensure result is JSON serializable
        if isinstance(result, dict):
            return jsonify(result)
        else:
            return jsonify({{"result": result}})
    
    except Exception as e:
        return jsonify({{"error": str(e)}}), 500
'''
            template += route_code
        
        template += '''
@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "getmethatdawg-deployed-app",
        "endpoints": [
'''
        
        # Add endpoint info to health check
        for i, endpoint in enumerate(self.endpoints):
            comma = "," if i < len(self.endpoints) - 1 else ""
            template += f'            {{"method": "{endpoint.method}", "path": "{endpoint.path}"}}{comma}\n'
        
        template += '''        ]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
'''
        
        # Write the Flask app
        flask_app_path = self.output_dir / "flask_app.py"
        with open(flask_app_path, 'w') as f:
            f.write(template)
        
        return flask_app_path
    
    def generate_dockerfile(self):
        """Generate Dockerfile"""
        dockerfile_content = '''FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source file and generated Flask app
COPY user_module.py .
COPY flask_app.py .

# Expose port
EXPOSE 5000

# Run the Flask app
CMD ["python", "flask_app.py"]
'''
        
        dockerfile_path = self.output_dir / "Dockerfile"
        with open(dockerfile_path, 'w') as f:
            f.write(dockerfile_content)
        
        return dockerfile_path
    
    def generate_requirements(self):
        """Generate requirements.txt, using custom requirements if available"""
        
        # Look for custom requirements.txt in multiple locations
        possible_requirements_paths = [
            Path("/tmp/requirements.txt"),  # Mounted from host during Docker run
            self.source_file.parent / "requirements.txt",  # In source directory
        ]
        
        custom_requirements_path = None
        for path in possible_requirements_paths:
            if path.exists():
                custom_requirements_path = path
                break
        
        if custom_requirements_path:
            print(f"✅ Found custom requirements.txt at {custom_requirements_path}")
            # Copy the custom requirements file
            requirements_path = self.output_dir / "requirements.txt"
            with open(custom_requirements_path, 'r') as src:
                custom_reqs = src.read()
            
            # Add essential Flask requirements if not present
            essential_reqs = ["flask>=2.0.0", "gunicorn>=20.0.0"]
            
            # Add weave for observability if WANDB is enabled
            if self.wandb_enabled:
                essential_reqs.append("weave")
                print("🐝 Adding weave to requirements for WANDB observability")
            
            lines = custom_reqs.strip().split('\n')
            existing_packages = {line.split('>=')[0].split('==')[0].split('<')[0].lower().strip() 
                               for line in lines if line.strip() and not line.strip().startswith('#')}
            
            # Add missing essential requirements
            for req in essential_reqs:
                package_name = req.split('>=')[0].lower()
                if package_name not in existing_packages:
                    custom_reqs += f"\n{req}"
            
            with open(requirements_path, 'w') as f:
                f.write(custom_reqs)
            
            print(f"✅ Using custom requirements with {len(lines)} packages")
            
        else:
            # Use default requirements
            print("ℹ No custom requirements.txt found, using default Flask requirements")
            requirements = [
                "flask>=2.0.0",
                "gunicorn>=20.0.0",
            ]
            
            # Add weave for observability if WANDB is enabled
            if self.wandb_enabled:
                requirements.append("weave")
                print("🐝 Adding weave to default requirements for WANDB observability")
            
            requirements_path = self.output_dir / "requirements.txt"
            with open(requirements_path, 'w') as f:
                f.write('\n'.join(requirements))
        
        return requirements_path
    
    def generate_fly_toml(self):
        """Generate fly.toml configuration"""
        app_name = self.original_name.replace('_', '-')
        
        # Read environment variables from .env file if it exists
        env_vars = self._read_env_file()
        
        # Generate secrets file
        secrets_file_path = self.generate_secrets_file(env_vars)
        
        # Generate deployment script
        deployment_script_path = self.generate_deployment_script(env_vars)
        
        # Categorize env vars
        secrets, regular_env = self._categorize_env_vars(env_vars)
        
        # Build environment section with only non-sensitive variables
        env_section = '  PORT = "5000"\n'
        for key, value in regular_env.items():
            # Include non-sensitive environment variables
            if key.upper() not in ['PORT']:  # Skip PORT as it's already set
                env_section += f'  {key} = "{value}"\n'
        
        fly_toml_content = f'''# fly.toml - Generated by getmethatdawg
app = "{app_name}"
primary_region = "iad"

[build]

[env]
{env_section}

[http_service]
  internal_port = 5000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0
  processes = ["app"]

[[http_service.checks]]
  interval = "10s"
  grace_period = "5s"
  method = "GET"
  path = "/"
  protocol = "http"
  timeout = "5s"
  tls_skip_verify = false

[[vm]]
  memory = '512mb'
  cpu_kind = 'shared'
  cpus = 1
'''
        
        fly_toml_path = self.output_dir / "fly.toml"
        with open(fly_toml_path, 'w') as f:
            f.write(fly_toml_content)
        
        return fly_toml_path
    
    def copy_source_file(self):
        """Copy the source file to output directory, removing getmethatdawg imports and decorators"""
        dest_path = self.output_dir / "user_module.py"
        
        # Read the source file
        with open(self.source_file, 'r') as f:
            lines = f.readlines()
        
        # Process lines to remove getmethatdawg imports and decorators, and add weave decorators
        processed_lines = []
        skip_next_function = False
        
        # Add weave import at the top if WANDB is enabled
        if self.wandb_enabled:
            processed_lines.append("import weave  # 🐝 Added by getmethatdawg for observability\n")
        
        for i, line in enumerate(lines):
            # Skip getmethatdawg imports (only if not auto-detect mode)
            if not self.auto_detect and ('import getmethatdawg' in line or 'from getmethatdawg' in line):
                continue
            
            # Skip getmethatdawg decorators (only if not auto-detect mode)
            if not self.auto_detect and line.strip().startswith('@getmethatdawg.expose'):
                skip_next_function = True
                continue
            
            # Add @weave.op() decorator before function definitions if WANDB is enabled
            if (self.wandb_enabled and 
                line.strip().startswith('def ') and 
                not line.strip().startswith('def _') and  # Skip private functions
                not line.strip().startswith('def __')):    # Skip magic methods
                
                # Check if this function is in our endpoints (auto-detected or explicit)
                func_name = line.strip().split('(')[0].replace('def ', '')
                is_endpoint = False
                
                # Check auto-detected endpoints
                for endpoint in self.auto_detected_endpoints:
                    if endpoint.func_name == func_name:
                        is_endpoint = True
                        break
                
                # Check explicit endpoints
                for endpoint in self.endpoints:
                    if endpoint.func_name == func_name:
                        is_endpoint = True
                        break
                
                if is_endpoint:
                    # Add the decorator with proper indentation
                    indent = len(line) - len(line.lstrip())
                    processed_lines.append(' ' * indent + "@weave.op()  # 🐝 Added by getmethatdawg for observability\n")
            
            # Add the line
            processed_lines.append(line)
        
        # Write the processed file
        with open(dest_path, 'w') as f:
            f.writelines(processed_lines)
        
        return dest_path
    
    def build(self):
        """Build all deployment artifacts"""
        self.analyze_source()
        
        # Generate all files
        self.copy_source_file()
        self.generate_flask_app()
        self.generate_dockerfile()
        self.generate_requirements()
        self.generate_fly_toml()
        
        print(f"✓ Generated deployment files in {self.output_dir}")
        
        # Show deployment instructions
        if (self.output_dir / "deploy-with-secrets.sh").exists():
            print("\n🔐 Secrets detected! Use the generated deployment script:")
            print(f"   cd {self.output_dir}")
            print(f"   ./deploy-with-secrets.sh")
        
        return self.output_dir


def main():
    """Main entry point for the builder"""
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print("Usage: python -m getmethatdawg.builder <source_file> [original_name] [--auto-detect]")
        sys.exit(1)
    
    source_file = sys.argv[1]
    original_name = None
    auto_detect = False
    
    # Parse additional arguments
    for i in range(2, len(sys.argv)):
        arg = sys.argv[i]
        if arg == '--auto-detect':
            auto_detect = True
        elif not original_name:
            original_name = arg
    
    if not os.path.exists(source_file):
        print(f"Error: Source file '{source_file}' not found")
        sys.exit(1)
    
    try:
        builder = GetMeThatDawgBuilder(source_file, original_name=original_name, auto_detect=auto_detect)
        builder.build()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 