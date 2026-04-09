import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


server_params = StdioServerParameters(
    command="python",
    args=["mcpserver.py"]
)


async def mcptesting(inputing):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # List available tools
            tools = await session.list_tools()
            print("\nAvailable Tools:")
            print(tools)

            # Call calculator tool
            result = await session.call_tool(
                "calculator",
                
                    {"operation": str(inputing)} 
                
            )

            return result
