# bilibili_win
一个bilibili的抽奖程序

函数参数​​

def get_winners(min_n, max_n, num_win, block_num, notin):

​​min_n​​: 中奖编号的最小值（包含）。

​​max_n​​: 中奖编号的最大值（包含）。

​​num_win​​: 需要选出的中奖者数量。

​​block_num​​: 区块链的区块号，用于获取交易数据。

​​notin​​: 一个集合或列表，包含不允许被选中的编号（黑名单）。

​​步骤解析​​


​​1. 获取区块链区块数据​​

data = {"jsonrpc": "2.0", "method": "condenser_api.get_block", "params": [block_num], "id": 1}

r = requests.post(url=nodes, json=data)

rjson = r.json()

通过 JSON-RPC 调用 condenser_api.get_block 方法，请求指定 block_num 的区块数据。

nodes 是区块链节点的URL（未在代码中定义，可能是全局变量）。

返回的响应解析为 JSON 格式。

​​2. 提取交易ID并拼接哈希字符串​​

transaction_ids = rjson["result"]['transaction_ids']

hash = ""

for i in transaction_ids:

    hash += i
    
print(hash)

res = hash

从区块数据中提取所有交易ID（transaction_ids）。

将所有交易ID拼接成一个字符串 hash（例如："id1id2id3..."）。

打印拼接后的字符串（调试用），并将其赋值给 res 作为初始哈希值。

​​3. 生成中奖编号​​

winners = set()

while len(winners) < num_win:

    res = hashlib.sha256(res.encode('utf-8')).hexdigest()
    
    lucky = int(res, 16) % (max_n - min_n + 1) + min_n
    
    if lucky in notin:
    
        continue
        
    else:
    
        winners.add(lucky)
        
​​初始化空集合 winners​​：用于存储不重复的中奖编号。

​​循环直到选出足够的中奖者​​：

​​生成SHA-256哈希​​：对当前 res 字符串进行哈希计算，得到新的十六进制哈希值。

​​计算候选编号​​：

将哈希值转换为十进制整数（int(res, 16)）。

通过取模运算将整数映射到 [min_n, max_n] 范围内的随机值。

​​检查黑名单​​：

如果 lucky 在 notin 中，跳过此次循环。

否则，将 lucky 加入 winners 集合。

​​返回结果​​：当 winners 的数量达到 num_win 时，退出循环并返回集合。

​​关键逻辑​​

​​确定性随机性​​：

中奖结果完全由区块的交易ID决定，因此同一区块和参数会生成相同的结果。

通过多次哈希迭代（res = sha256(res)）确保每次计算的随机性独立。

​​避免重复和黑名单​​：
使用 set 自动去重。
通过 notin 过滤不允许的编号。
​​均匀分布​​：
int(res, 16) % (max_n - min_n + 1) + min_n 确保编号在范围内均匀分布。
