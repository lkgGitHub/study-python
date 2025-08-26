# server.py

import contextlib

from typing import Any, List, Optional
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.middleware import Middleware

from mcpauth import MCPAuth
from mcpauth.config import AuthServerType
from mcpauth.exceptions import (
    MCPAuthBearerAuthException,
    BearerAuthExceptionCode,
)
from mcpauth.types import AuthInfo, ResourceServerConfig, ResourceServerMetadata
from mcpauth.utils import fetch_server_config
from service import TodoService

# 初始化 FastMCP 服务器
mcp = FastMCP(name="Todo Manager", stateless_http=True, streamable_http_path='/')

# 创建 TodoService 实例
todo_service = TodoService()


# 步骤 1：获取授权服务器元数据
issuer_url = ""

# 获取授权服务器配置
auth_server_config = fetch_server_config(issuer_url, AuthServerType.OIDC)  # 或 AuthServerType.OAUTH

# 步骤 2：配置受保护资源元数据
# 定义 MCP 服务器的资源标识符
resource_id = ""

mcp_auth = MCPAuth(
    protected_resources=ResourceServerConfig(
        metadata=ResourceServerMetadata(
            resource=resource_id,
            # 上一步获取的授权服务器元数据
            authorization_servers=[auth_server_config],
            # MCP 服务器支持的权限 (Scope)
            scopes_supported=[
                "create:todos",
                "read:todos",
                "delete:todos"
            ]
        )
    )
)


def assert_user_id(auth_info: Optional[AuthInfo]) -> str:
    """断言 auth_info 包含有效用户 ID 并返回。"""
    if not auth_info or not auth_info.subject:
        raise Exception("Invalid auth info")
    return auth_info.subject


def has_required_scopes(user_scopes: List[str], required_scopes: List[str]) -> bool:
    """检查用户是否拥有所有必需权限 (Scope)。"""
    return all(scope in user_scopes for scope in required_scopes)


@mcp.tool()
def create_todo(content: str) -> dict[str, Any]:
    """创建新的待办事项。需要 'create:todos' 权限 (Scope)。"""
    auth_info = mcp_auth.auth_info
    user_id = assert_user_id(auth_info)

    # 只有拥有 'create:todos' 权限 (Scope) 的用户才能创建
    user_scopes = auth_info.scopes if auth_info else []
    if not has_required_scopes(user_scopes, ["create:todos"]):
        raise MCPAuthBearerAuthException(BearerAuthExceptionCode.MISSING_REQUIRED_SCOPES)

    created_todo = todo_service.create_todo(content=content, owner_id=user_id)
    return created_todo


@mcp.tool()
def get_todos() -> dict[str, Any]:
    """
    列出待办事项。拥有 'read:todos' 权限 (Scope) 的用户可查看所有待办事项，
    否则只能查看自己的。
    """
    auth_info = mcp_auth.auth_info
    user_id = assert_user_id(auth_info)

    # 有 'read:todos' 权限 (Scope) 可访问所有待办事项，否则只能访问自己的
    user_scopes = auth_info.scopes if auth_info else []
    todo_owner_id = None if has_required_scopes(user_scopes, ["read:todos"]) else user_id

    todos = todo_service.get_all_todos(todo_owner_id)
    return {"todos": todos}


@mcp.tool()
def delete_todo(id: str) -> dict[str, Any]:
    """
    根据 id 删除待办事项。用户可删除自己的待办事项。
    拥有 'delete:todos' 权限 (Scope) 的用户可删除任意待办事项。
    """
    auth_info = mcp_auth.auth_info
    user_id = assert_user_id(auth_info)

    todo = todo_service.get_todo_by_id(id)

    if not todo:
        return {"error": "Failed to delete todo"}

    # 用户只能删除自己的待办事项
    # 拥有 'delete:todos' 权限 (Scope) 可删除任意待办事项
    user_scopes = auth_info.scopes if auth_info else []
    if todo.owner_id != user_id and not has_required_scopes(user_scopes, ["delete:todos"]):
        return {"error": "Failed to delete todo"}

    deleted_todo = todo_service.delete_todo(id)

    if deleted_todo:
        return {
            "message": f"Todo {id} deleted",
            "details": deleted_todo
        }
    else:
        return {"error": "Failed to delete todo"}


@contextlib.asynccontextmanager
async def lifespan(app: Starlette):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(mcp.session_manager.run())
        yield


# Create the middleware and app
# 更新 MCP 服务器。快完成了！现在需要更新 MCP 服务器，应用 MCP Auth 路由和中间件函数，并基于用户权限 (Scope) 实现待办事项工具的权限控制。
# 接下来，应用 MCP Auth 中间件到 MCP 服务器。该中间件将处理所有请求的认证 (Authentication) 和授权 (Authorization)，确保只有被授权用户才能访问待办事项工具。
bearer_auth = Middleware(mcp_auth.bearer_auth_middleware('jwt', resource=resource_id))
app = Starlette(
    routes=[
        # Protect the MCP server with the Bearer auth middleware
        *mcp_auth.resource_metadata_router().routes,
        Mount("/", app=mcp.streamable_http_app(), middleware=[bearer_auth]),
    ],
    lifespan=lifespan,
)


# 使用 uvicorn 启动 Todo Manager 服务器
# uvicorn server:app --host 127.0.0.1 --port 3001

# 或使用 uv:
# uv run uvicorn server:app --host 127.0.0.1 --port 3001
