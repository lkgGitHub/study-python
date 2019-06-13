"""
83. 给定一个排序链表，删除所有重复的元素，使得每个元素只出现一次。

示例 1:

输入: 1->1->2
输出: 1->2
示例 2:

输入: 1->1->2->3->3
输出: 1->2->3

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/remove-duplicates-from-sorted-list
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""


# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


def deleteDuplicates(head: ListNode) -> ListNode:
    if head is None or head.next is None:
        return head
    h = head
    while True:
        if h.val == h.next.val:
            h.next = h.next.next
        else:
            h = h.next
        if h.next is None:
            break
    return head


# 有序列表删除
def print_listNode(heads: ListNode):
    print(heads.val, end='->')
    while heads.next:
        heads = heads.next
        if heads.next:
            print(heads.val, end='->')
        else:
            print(heads.val)


if __name__ == '__main__':
    head = ListNode(1)
    h1 = ListNode(1)
    h2 = ListNode(2)
    head.next = h1
    h1.next = h2
    print_listNode(head)

    listNode = deleteDuplicates(head)
    print_listNode(listNode)
