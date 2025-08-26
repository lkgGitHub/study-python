"""
一个简单的 Todo 服务，仅用于演示。
使用内存列表存储待办事项。
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
import random
import string


class Todo:
    """待办事项实体"""

    def __init__(self, id: str, content: str, owner_id: str, created_at: str):
        self.id = id
        self.content = content
        self.owner_id = owner_id
        self.created_at = created_at

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典，便于 JSON 序列化"""
        return {
            "id": self.id,
            "content": self.content,
            "ownerId": self.owner_id,
            "createdAt": self.created_at
        }


class TodoService:
    """简单的 Todo 服务，仅用于演示"""

    def __init__(self):
        self._todos: List[Todo] = []

    def get_all_todos(self, owner_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        获取所有待办事项，可选按 owner_id 过滤

        Args:
            owner_id: 如提供，仅返回该用户的待办事项

        Returns:
            待办事项字典列表
        """
        if owner_id:
            filtered_todos = [todo for todo in self._todos if todo.owner_id == owner_id]
            return [todo.to_dict() for todo in filtered_todos]
        return [todo.to_dict() for todo in self._todos]

    def get_todo_by_id(self, todo_id: str) -> Optional[Todo]:
        """
        根据 ID 获取待办事项

        Args:
            todo_id: 待办事项 ID

        Returns:
            找到则返回 Todo 对象，否则返回 None
        """
        for todo in self._todos:
            if todo.id == todo_id:
                return todo
        return None

    def create_todo(self, content: str, owner_id: str) -> Dict[str, Any]:
        """
        创建新的待办事项

        Args:
            content: 待办事项内容
            owner_id: 用户 ID

        Returns:
            创建的待办事项字典
        """
        todo = Todo(
            id=self._generate_id(),
            content=content,
            owner_id=owner_id,
            created_at=datetime.now().isoformat()
        )
        self._todos.append(todo)
        return todo.to_dict()

    def delete_todo(self, todo_id: str) -> Optional[Dict[str, Any]]:
        """
        根据 ID 删除待办事项

        Args:
            todo_id: 待办事项 ID

        Returns:
            删除的待办事项字典，如未找到返回 None
        """
        for i, todo in enumerate(self._todos):
            if todo.id == todo_id:
                deleted_todo = self._todos.pop(i)
                return deleted_todo.to_dict()
        return None

    def _generate_id(self) -> str:
        """生成随机 ID"""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))