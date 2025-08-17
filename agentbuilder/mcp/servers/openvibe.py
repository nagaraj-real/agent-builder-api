from pathlib import Path
import shlex
from mcp.server.fastmcp import FastMCP,Context
import subprocess


mcp = FastMCP("openvibe")

current_dir = Path(__file__).resolve().parent


@mcp.resource("config://app")
def get_config() -> any:
    """Static configuration data"""
    return  {
        "project_path": "~/projects/app",
        "project_docs_path": "~/projects/app/docs"
    }

@mcp.prompt()
def code_prompt() -> str:
    with open(f"{current_dir}/vibe_agent_prompt.md", "r", encoding="utf-8") as f:
        _prompt_text = f.read()
    return _prompt_text

@mcp.tool()
async def get_project_path(ctx:Context) -> str:
    """
    Fetch project path inside container
    """
    data = await ctx.read_resource(f"config://app")
    ctx.log('info',data)
    return data

@mcp.tool()
async def get_project_info(ctx:Context) -> str:
    """
    Fetch project info
    """
    data = await ctx.read_resource(f"config://app")
    ctx.log('info',data)
    return data

@mcp.tool()
def execute_bash_command(command: str) -> str:
    """
    Execute bash command(s) inside a Docker container named alpine_runner.
    The tool uses the following statement to execute the command(s)
    `docker exec -it alpine_runner sh -c '<<command(s)>>'`

    Args:
        command: Bash command(s) to execute. 

    Returns:
        Output or error message from the command execution.
    """
    try:
        # Safely escape user input to avoid breaking the shell
        safe_command = shlex.quote(command)

        # Run the escaped command inside a shell with logging
        wrapped_command = (
            f'(echo "[INFO] Running: {command}"; eval {safe_command}) '
            f'2>&1 | tee /var/log/vibe.log'
        )

        result = subprocess.run(
            ["docker", "exec", "alpine_runner", "sh", "-c", wrapped_command],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            return f"[ERROR] Command failed with exit code {result.returncode}:\n{result.stdout or result.stderr}"
        return result.stdout or "[INFO] Command executed successfully, but produced no output."

    except subprocess.TimeoutExpired:
        return "[TIMEOUT] Command took too long to complete. Check container logs for progress."

    except Exception as exc:
        return f"[EXCEPTION] An error occurred: {str(exc)}"
    
@mcp.tool()
def fetch_bash_logs() -> str:
    """Fetches logs from /var/log/vibe.log inside the alpine_runner container."""
    try:
        result = subprocess.run(
            ["docker", "exec", "alpine_runner", "sh", "-c", "cat /var/log/vibe.log"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return f"[ERROR] Failed to fetch logs (exit code {result.returncode}):\n{result.stderr or 'No error message.'}"

        return result.stdout or "[INFO] Log file is empty."

    except Exception as exc:
        return f"[EXCEPTION] An error occurred while fetching logs: {str(exc)}"


if __name__ == "__main__":
    mcp.run(transport="stdio")