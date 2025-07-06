"""Simple Math Operations Server using FastMCP"""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP('Math', port=8000, host='0.0.0.0', stateless_http=True)

@mcp.tool(description="Add two numbers")
def add(a: int, b: int) -> str:
    """Add two numbers."""
    return f"Result: {a + b}"

@mcp.tool(description="Subtract two numbers")
def subtract(a: int, b: int) -> str:
    """Subtract two numbers."""
    return f"Result: {a - b}"

@mcp.tool(description="Multiply two numbers")
def multiply(a: int, b: int) -> str:    
    """Multiply two numbers."""
    return f"Result: {a * b}"

@mcp.tool(description="Divide two numbers")
def divide(a: int, b: int) -> str:
    """Divide two numbers."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return f"Result: {a / b}"


def main():
    """Run the FastMCP server."""
    mcp.run(transport='sse')


if __name__ == "__main__":
    main()
