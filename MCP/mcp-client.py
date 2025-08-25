import asyncio

from fastmcp import Client


async def main():
    # 测试 mcp 客户端的功能
    async with Client("http://127.0.0.1:8001/sse") as mcp_client:
        tools = await mcp_client.list_tools()
        resource = await mcp_client.list_resources()
        prompts = await mcp_client.list_prompts()
        print(f"Available tools: {tools}")
        print(f"Available resource: {resource}")
        print(f"Available prompts: {prompts}")
        result = await mcp_client.call_tool("add", {"a": 5, "b": 3})
        if result.is_error:
            print("has error")
        else:
            print(f"tool {result.data} added")

if __name__ == "__main__":
    asyncio.run(main())