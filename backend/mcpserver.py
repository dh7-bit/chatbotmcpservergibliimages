from mcp.server.fastmcp import FastMCP
import ast

mcp = FastMCP("CalculatorServer")

@mcp.tool()
def calculator(operation: str) -> str:
    print("RECEIVED OPERATION:", repr(operation))
    """
    Simple calculator tool.
    Args:
        operation: a math expression like 5*5, 10+3, (4+5)*2
    """
    try:
        result=eval(operation)
        return str(result)
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    mcp.run()